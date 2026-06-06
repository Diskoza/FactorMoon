from __future__ import annotations

import csv
import shutil
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
FACTOR_MOON = SCRIPT_DIR.parent
INSTANCES = FACTOR_MOON.parent

APPROVED_LOCAL_IDS = {
    "cobblemon_shiny_rarities",
    "mr_cobblemon_alphas",
    "mr_cobblemon_journeymounts",
    "packetfixer",
    "globalpacks",
}


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


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> int:
    source_report = SCRIPT_DIR / "local_neoforge_candidate_jars.csv"
    rows = []
    with source_report.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            matched_ids = set(filter(None, row["matched_mod_ids"].split(";")))
            if not (matched_ids & APPROVED_LOCAL_IDS):
                continue
            if row["instance"] != "cobblemon-extra":
                continue
            src = INSTANCES / row["source"]
            dst = FACTOR_MOON / "mods" / src.name
            ensure_inside_factor_moon(dst)
            status = "missing_source"
            if src.exists():
                if dst.exists():
                    status = "already_present"
                else:
                    shutil.copy2(src, dst)
                    status = "copied"
            rows.append(
                {
                    "status": status,
                    "matched_mod_ids": row["matched_mod_ids"],
                    "source": safe_rel(src),
                    "target": safe_rel(dst),
                    "sha1": row["sha1"],
                    "note": "local multi-loader jar with NeoForge metadata; copied without network download",
                }
            )
    write_csv(
        SCRIPT_DIR / "local_neoforge_copied_to_factormoon.csv",
        rows,
        ["status", "matched_mod_ids", "source", "target", "sha1", "note"],
    )
    print({"copied": sum(1 for row in rows if row["status"] == "copied"), "rows": len(rows)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
