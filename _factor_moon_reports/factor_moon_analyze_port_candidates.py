from __future__ import annotations

import csv
import json
import zipfile
from pathlib import Path

import factor_moon_audit as audit


SCRIPT_DIR = Path(__file__).resolve().parent
FACTOR_MOON = SCRIPT_DIR.parent
INSTANCES = FACTOR_MOON.parent


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def find_fabric_file(file_name: str) -> Path | None:
    candidates = [
        INSTANCES / "cobblemon-extra" / "mods" / file_name,
        FACTOR_MOON / "_cobblemon_extra_reference" / "custom_mods_fabric_original" / file_name,
    ]
    for path in candidates:
        if path.exists():
            return path
    hits = list((INSTANCES / "cobblemon-extra").glob(f"**/{file_name}"))
    return hits[0] if hits else None


def text_or_empty(zf: zipfile.ZipFile, name: str) -> str:
    try:
        return zf.read(name).decode("utf-8", errors="replace")
    except KeyError:
        return ""


def analyze(path: Path, row: dict) -> dict:
    record = audit.parse_jar(path).__dict__
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        class_files = [name for name in names if name.endswith(".class")]
        java_like = [name for name in names if name.endswith((".java", ".kt"))]
        mixin_files = [name for name in names if name.endswith(".mixins.json") or "mixin" in name.lower() and name.endswith(".json")]
        lang_files = [name for name in names if "/lang/" in name and name.endswith(".json")]
        data_files = [name for name in names if name.startswith("data/")]
        asset_files = [name for name in names if name.startswith("assets/")]
        fabric_json = text_or_empty(zf, "fabric.mod.json")
        fabric = {}
        if fabric_json:
            try:
                fabric = json.loads(fabric_json)
            except json.JSONDecodeError:
                fabric = {}
        deps = fabric.get("depends", {})
        entrypoints = fabric.get("entrypoints", {})
        provides = ";".join(fabric.get("provides", []) or [])
    risk = "resource_or_datapack_only"
    if class_files:
        risk = "code"
    if mixin_files:
        risk = "mixin_code"
    if "fabric-api" in deps or "fabricloader" in deps:
        risk = f"{risk}+fabric_api"
    return {
        **row,
        "source_path": audit.safe_rel(path),
        "size": path.stat().st_size,
        "mod_ids": record.get("mod_ids", ""),
        "display_names": record.get("display_names", ""),
        "loaders": record.get("loaders", ""),
        "metadata": record.get("metadata", ""),
        "class_count": len(class_files),
        "java_or_kt_sources_inside": len(java_like),
        "mixin_files": ";".join(mixin_files),
        "lang_count": len(lang_files),
        "data_count": len(data_files),
        "asset_count": len(asset_files),
        "fabric_depends": json.dumps(deps, ensure_ascii=False, sort_keys=True),
        "fabric_entrypoints": json.dumps(entrypoints, ensure_ascii=False, sort_keys=True),
        "fabric_provides": provides,
        "port_risk": risk,
    }


def main() -> int:
    rows = []
    for row in read_csv(SCRIPT_DIR / "cobblemon_needs_port_or_skip_no_link.csv"):
        path = find_fabric_file(row["fabric_file"])
        if not path:
            rows.append({**row, "source_path": "", "port_risk": "missing_source_jar"})
            continue
        rows.append(analyze(path, row))
    fieldnames = [
        "mod_id",
        "name",
        "fabric_file",
        "source_path",
        "size",
        "mod_ids",
        "display_names",
        "loaders",
        "metadata",
        "class_count",
        "java_or_kt_sources_inside",
        "mixin_files",
        "lang_count",
        "data_count",
        "asset_count",
        "fabric_depends",
        "fabric_entrypoints",
        "fabric_provides",
        "port_risk",
        "reason",
        "next_action",
    ]
    with (SCRIPT_DIR / "port_candidate_analysis.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    summary: dict[str, int] = {}
    for row in rows:
        summary[row["port_risk"]] = summary.get(row["port_risk"], 0) + 1
    (SCRIPT_DIR / "port_candidate_analysis_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
