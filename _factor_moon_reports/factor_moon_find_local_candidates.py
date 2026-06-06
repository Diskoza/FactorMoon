from __future__ import annotations

import csv
from pathlib import Path

import factor_moon_audit as audit


SCRIPT_DIR = Path(__file__).resolve().parent
FACTOR_MOON = SCRIPT_DIR.parent
INSTANCES = FACTOR_MOON.parent

FORBIDDEN_NAME_PARTS = {
    "immersive_aircraft",
    "immersive-aircraft",
    "smallships",
    "small-ships",
    "tacz",
    "createbigcannons",
    "big_cannons",
    "ritchiesprojectilelib",
}


def read_decisions() -> list[dict]:
    path = SCRIPT_DIR / "user_link_install_decisions.csv"
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_factor_ids() -> set[str]:
    path = SCRIPT_DIR / "current_factor_moon_mod_inventory.csv"
    ids = set()
    if not path.exists():
        return ids
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            for mod_id in row.get("mod_ids", "").split(";"):
                if mod_id:
                    ids.add(mod_id)
    return ids


def requested_ids() -> dict[str, list[dict]]:
    rows = {}
    for decision in read_decisions():
        if decision.get("decision") != "needs_download_and_metadata_check":
            continue
        if decision.get("destination") != "mods":
            continue
        mod_id = decision.get("expected_mod_id")
        if not mod_id:
            continue
        rows.setdefault(mod_id, []).append(decision)
    return rows


def is_forbidden_file(path: Path) -> bool:
    low = path.name.lower()
    return any(part in low for part in FORBIDDEN_NAME_PARTS)


def is_good_loader(record: dict) -> bool:
    loaders = set(filter(None, record.get("loaders", "").split(";")))
    metadata = record.get("metadata", "")
    if "fabric" in loaders and not ({"neoforge", "forge"} & loaders):
        return False
    return "neoforge" in loaders or "forge" in loaders or "META-INF/neoforge.mods.toml" in metadata or "META-INF/mods.toml" in metadata


def candidate_score(path: Path, record: dict) -> int:
    score = 0
    low = path.name.lower()
    loaders = record.get("loaders", "")
    if "neoforge" in loaders:
        score += 50
    if "forge" in loaders:
        score += 30
    if "1.21.1" in low:
        score += 20
    if "neoforge" in low:
        score += 10
    if "fabric" in low:
        score -= 100
    if "1.20" in low or "1.19" in low or "1.18" in low:
        score -= 50
    return score


def main() -> int:
    factor_ids = read_factor_ids()
    wanted = requested_ids()
    rows = []
    for mods_dir in sorted(INSTANCES.glob("*/mods"), key=lambda p: str(p).lower()):
        if FACTOR_MOON in mods_dir.resolve().parents:
            continue
        instance_name = mods_dir.parent.name
        for jar in sorted(mods_dir.glob("*.jar"), key=lambda p: p.name.lower()):
            if is_forbidden_file(jar):
                continue
            record = audit.parse_jar(jar).__dict__
            if not is_good_loader(record):
                continue
            ids = [mod_id for mod_id in record.get("mod_ids", "").split(";") if mod_id]
            matched = []
            for mod_id in ids:
                if mod_id in factor_ids:
                    continue
                if mod_id in wanted:
                    matched.append(mod_id)
            if not matched:
                continue
            rows.append(
                {
                    "score": candidate_score(jar, record),
                    "instance": instance_name,
                    "matched_mod_ids": ";".join(matched),
                    "file_name": jar.name,
                    "source": audit.safe_rel(jar),
                    "size": record["size"],
                    "sha1": record["sha1"],
                    "metadata": record["metadata"],
                    "loaders": record["loaders"],
                    "display_names": record["display_names"],
                }
            )

    rows.sort(key=lambda row: (-int(row["score"]), row["matched_mod_ids"], row["file_name"].lower()))
    audit.write_csv(
        SCRIPT_DIR / "local_neoforge_candidate_jars.csv",
        rows,
        ["score", "instance", "matched_mod_ids", "file_name", "source", "size", "sha1", "metadata", "loaders", "display_names"],
    )
    print({"local_candidates": len(rows), "matched_mod_ids": len({m for row in rows for m in row["matched_mod_ids"].split(";")})})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
