from __future__ import annotations

import csv
import shutil
import zipfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
FACTOR_MOON = SCRIPT_DIR.parent
INSTANCES = FACTOR_MOON.parent
COBBLE_EXTRA = INSTANCES / "cobblemon-extra"


def safe_rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(INSTANCES.resolve()))
    except ValueError:
        return str(path)


def ensure_inside_factor_moon(path: Path) -> None:
    resolved = path.resolve()
    root = FACTOR_MOON.resolve()
    if not (resolved == root or root in resolved.parents):
        raise RuntimeError(f"Refusing to write outside FactorMoon: {path}")


def copy_file(src: Path, dst: Path) -> str:
    if not src.exists():
        return "missing_source"
    ensure_inside_factor_moon(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and src.stat().st_size == dst.stat().st_size:
        return "already_present"
    shutil.copy2(src, dst)
    return "copied"


def copy_tree(src: Path, dst: Path, ignore=None) -> str:
    if not src.exists():
        return "missing_source"
    ensure_inside_factor_moon(dst)
    if dst.exists():
        return "already_present"
    shutil.copytree(src, dst, ignore=ignore)
    return "copied"


def read_custom_manifest() -> list[Path]:
    csv_path = SCRIPT_DIR / "custom_or_personal_mods_to_preserve.csv"
    paths = []
    if not csv_path.exists():
        return paths
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            source_file = row.get("source_file", "")
            if source_file:
                paths.append(INSTANCES / source_file)
    return paths


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def preserve_custom_files() -> list[dict]:
    rows = []
    dst_dir = FACTOR_MOON / "_cobblemon_extra_reference" / "custom_mods_fabric_original"
    candidates = read_custom_manifest()
    candidates.extend(
        [
            COBBLE_EXTRA / "COBBLEVERSE - Pokemon Adventure [Cobblemon] COBBLEVERSE-1.7.30-CF.jar",
            COBBLE_EXTRA / "COBBLEVERSE - Pokemon Adventure [Cobblemon] COBBLEVERSE-1.7.30-CF.json",
            COBBLE_EXTRA / "COBBLEVERSE - Third-Party Licenses.pdf",
            COBBLE_EXTRA / "build" / "cobblemon-extra-ride-compat-repacked.jar",
        ]
    )
    seen = set()
    for src in candidates:
        resolved = src.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        dst = dst_dir / src.name
        status = copy_file(src, dst)
        rows.append({"kind": "custom_file", "status": status, "source": safe_rel(src), "target": safe_rel(dst)})

    source_root = FACTOR_MOON / "_cobblemon_extra_reference" / "custom_sources"
    source_dirs = [
        (COBBLE_EXTRA / "build" / "cobblemon-extra-ride-compat", source_root / "cobblemon-extra-ride-compat"),
        (COBBLE_EXTRA / "build" / "code-src", source_root / "cobblemon-extra-ride-compat-code-src"),
        (COBBLE_EXTRA / "build" / "stardew-original-assets", source_root / "stardew-original-assets"),
        (
            COBBLE_EXTRA / "build" / "stardew-fishing-fabric" / "fabric-example-mod-1.21",
            source_root / "stardew-fishing-fabric-source",
        ),
    ]

    def ignore_gradle_build(_dir: str, names: list[str]) -> set[str]:
        return {name for name in names if name in {".gradle", "build", ".idea"}}

    for src, dst in source_dirs:
        status = copy_tree(src, dst, ignore=ignore_gradle_build)
        rows.append({"kind": "custom_source", "status": status, "source": safe_rel(src), "target": safe_rel(dst)})
    return rows


def extract_ru_overrides() -> list[dict]:
    rows = []
    dst_root = FACTOR_MOON / "kubejs" / "assets"
    jar_paths = sorted((COBBLE_EXTRA / "mods").glob("*.jar"), key=lambda p: p.name.lower())
    for jar in jar_paths:
        try:
            with zipfile.ZipFile(jar) as zf:
                for info in zf.infolist():
                    entry = info.filename.replace("\\", "/")
                    parts = entry.split("/")
                    if len(parts) != 4:
                        continue
                    if parts[0] != "assets" or parts[2] != "lang" or parts[3] != "ru_ru.json":
                        continue
                    namespace = parts[1]
                    target = dst_root / namespace / "lang" / "ru_ru.json"
                    ensure_inside_factor_moon(target)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if target.exists():
                        rows.append(
                            {
                                "status": "skipped_existing",
                                "source": safe_rel(jar),
                                "entry": entry,
                                "target": safe_rel(target),
                            }
                        )
                        continue
                    data = zf.read(info)
                    target.write_bytes(data)
                    rows.append(
                        {
                            "status": "extracted",
                            "source": safe_rel(jar),
                            "entry": entry,
                            "target": safe_rel(target),
                        }
                    )
        except (zipfile.BadZipFile, OSError) as exc:
            rows.append(
                {
                    "status": f"error:{type(exc).__name__}",
                    "source": safe_rel(jar),
                    "entry": "",
                    "target": "",
                }
            )
    return rows


def main() -> int:
    custom_rows = preserve_custom_files()
    override_rows = extract_ru_overrides()
    write_csv(
        SCRIPT_DIR / "custom_reference_copy_manifest.csv",
        custom_rows,
        ["kind", "status", "source", "target"],
    )
    write_csv(
        SCRIPT_DIR / "kubejs_ru_translation_overrides.csv",
        override_rows,
        ["status", "source", "entry", "target"],
    )
    print(
        {
            "custom_reference_rows": len(custom_rows),
            "translation_override_rows": len(override_rows),
            "translation_overrides_extracted": sum(1 for row in override_rows if row["status"] == "extracted"),
            "translation_overrides_skipped_existing": sum(1 for row in override_rows if row["status"] == "skipped_existing"),
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
