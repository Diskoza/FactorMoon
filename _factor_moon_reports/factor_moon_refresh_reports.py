from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
FACTOR_MOON = SCRIPT_DIR.parent
INSTANCES = FACTOR_MOON.parent

MANUAL_SKIP_IDS = {"immersive_aircraft", "smallships", "niftycarts", "infinite-music"}
EQUIVALENT_IDS = {
    "catchrate-display": {"catchrate_display"},
    "cloth-config": {"cloth_config"},
    "cobblemon-battle-extras": {"cobblemon_battle_extras"},
    "fabric-api": {"fabric_api", "forgified_fabric_api"},
    "fabric-language-kotlin": {"kotlinforforge", "kotlin_for_forge"},
    "cobblesafepastures": {"safepastures", "safepastures_neoforge"},
    "cosmeticarmor": {"cosmeticarmorreworked"},
    "customsplashscreen": {"simplesplashscreen"},
    "krypton": {"krypton_fnp"},
    "moarconcrete": {"moreconcrete"},
    "modmenu": {"mod_menu"},
    "nethermap": {"betternether"},
    "pasture-loot": {"pastureloot", "pasturelootnf"},
    "pastureloot": {"pasture-loot", "pasturelootnf"},
    "ping-wheel": {"ping_wheel"},
    "poke-clothing": {"poke_clothing"},
    "reeses-sodium-options": {"reeses_sodium_options"},
    "roughlyenoughitems": {"rei"},
    "resourcepackoverrides": {"resource_pack_overrides"},
    "safepastures": {"safepastures_neoforge"},
    "smartparticles": {"smart_particles"},
    "sodium-extra": {"sodium_extra"},
    "stardew_fishing_fabric": {"stardew_fishing"},
    "tmcraft": {"cobblemon_tm", "cobblemon_tms"},
    "tooltipfix": {"better_tooltips"},
    "tims_core": {"tim_core"},
    "unknown:cobblemon-additions-4.1.6": {"cobblemon-additions"},
    "unknown:CobbleverseBadges-1.3": {"cobbleversebadges"},
    "unknown:EuphoriaPatcher-1.8.6-r5.7.1-fabric": {"euphoria_patcher"},
    "unknown:mega_showdown-fabric-1.6.12+1.7.3+1.21.1": {"mega_showdown", "megashowdown"},
    "zoomify": {"justzoom"},
    "kotlinforforge": {"kotlin_for_forge"},
}

LINK_ID_ALIASES = {
    "better_tooltips": {"tooltipfix"},
    "cobblemon-battle-extras": {"cobblemon_battle_extras"},
    "cobblemon_playerxp": {"playerxp"},
    "cobblemon_tms": {"tmcraft"},
    "cobblesafepastures": {"safepastures"},
    "cosmeticarmor": {"cosmeticarmorreworked"},
    "customsplashscreen": {"simplesplashscreen"},
    "euphoriapatcher": {"unknown:EuphoriaPatcher-1.8.6-r5.7.1-fabric"},
    "krypton": {"krypton_fnp"},
    "mega_showdown": {"unknown:mega_showdown-fabric-1.6.12+1.7.3+1.21.1"},
    "moarconcrete": {"moreconcrete"},
    "modmenu": {"mod_menu"},
    "navas_zas": {"zamega"},
    "nethermap": {"betternether"},
    "pasture-loot": {"pasturelootnf"},
    "pastureloot": {"pasture-loot"},
    "safepastures": {"safepastures_neoforge"},
    "smartparticles": {"smart_particles"},
    "stardew_fishing_fabric": {"stardew_fishing"},
    "tmcraft": {"cobblemon_tm"},
}

FILE_IMPLIED_PRESENT_IDS = {
    "kotlinforforge": "kotlinforforge",
}

DATAPACK_IMPLIED_PRESENT_IDS = {
    "BCA-Datapack": "cobblemon-additions",
    "cobble-caf": "mr_cobble_cafforms",
    "extra-move-anims": "mr_extra_moveanimscobblemon",
}


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def rows_from_cobblemon_inventory() -> list[dict]:
    inventory = SCRIPT_DIR / "cobblemon_extra_mod_inventory.csv"
    rows = []
    seen_counts: dict[str, int] = {}
    for source in read_csv(inventory):
        ids = [mod_id for mod_id in source.get("mod_ids", "").split(";") if mod_id]
        mod_id = ids[0] if ids else f"unknown:{Path(source['file_name']).stem}"
        seen_counts[mod_id] = seen_counts.get(mod_id, 0) + 1
        name = source.get("display_names") or Path(source["file_name"]).stem
        if ";" in name:
            name = name.split(";")[0]
        reason = "no final NeoForge equivalent present; needs manual download/check or port"
        if seen_counts[mod_id] > 1:
            reason = "duplicate Fabric jar / backup copy"
        rows.append(
            {
                "mod_id": mod_id,
                "name": name,
                "fabric_file": source["file_name"],
                "reason": reason,
            }
        )
    return rows


def current_ids() -> set[str]:
    ids = set()
    for row in read_csv(SCRIPT_DIR / "current_factor_moon_mod_inventory.csv"):
        for mod_id in row.get("mod_ids", "").split(";"):
            if mod_id:
                ids.add(mod_id)
        file_name = row.get("file_name", "").lower()
        for marker, implied_id in FILE_IMPLIED_PRESENT_IDS.items():
            if marker in file_name:
                ids.add(implied_id)
    datapacks_dir = FACTOR_MOON / "datapacks"
    if datapacks_dir.exists():
        for path in datapacks_dir.iterdir():
            name = path.name.lower()
            for marker, implied_id in DATAPACK_IMPLIED_PRESENT_IDS.items():
                if marker.lower() in name:
                    ids.add(implied_id)
    return ids


def is_present(mod_id: str, ids: set[str]) -> bool:
    if mod_id in ids:
        return True
    for alias in EQUIVALENT_IDS.get(mod_id, set()):
        if alias in ids:
            return True
    return False


def link_lookup() -> dict[str, dict]:
    lookup: dict[str, dict] = {}
    rows = read_csv(SCRIPT_DIR / "user_link_install_decisions.csv")
    for row in rows:
        if row.get("decision", "").startswith("skip") or row.get("kind") == "modpacks":
            continue
        key = row.get("expected_mod_id", "")
        if key:
            lookup[key] = row
            for alias in LINK_ID_ALIASES.get(key, set()):
                lookup[alias] = row
    for row in rows:
        if row.get("decision", "").startswith("skip") or row.get("kind") == "modpacks":
            continue
        expected = row.get("expected_mod_id", "")
        if not expected:
            continue
        for alias in LINK_ID_ALIASES.get(expected, set()):
            lookup.setdefault(alias, row)
    return lookup


def main() -> int:
    ids = current_ids()
    previous = rows_from_cobblemon_inventory()
    links = link_lookup()
    remaining = []
    pending_with_links = []
    port_or_skip = []
    covered = []
    skipped = []
    for row in previous:
        clean_id = row["mod_id"].removeprefix("unknown:")
        low_file = row["fabric_file"].lower()
        if (
            row["mod_id"] in MANUAL_SKIP_IDS
            or clean_id in MANUAL_SKIP_IDS
            or low_file.startswith("immersive_aircraft")
            or "smallships" in low_file
            or "niftycarts" in low_file
            or "infinite-music" in low_file
        ):
            skipped.append({**row, "final_status": "skipped_by_user"})
        elif is_present(row["mod_id"], ids):
            covered.append({**row, "final_status": "covered_by_current_factormoon"})
        else:
            link = links.get(row["mod_id"])
            if link:
                enriched = {
                    **row,
                    "link_slug": link.get("slug", ""),
                    "link_kind": link.get("kind", ""),
                    "link_file_or_version": link.get("file_or_version", ""),
                    "url": link.get("url", ""),
                    "next_action": "download provided link, verify NeoForge/1.21.1 metadata, then install",
                }
                pending_with_links.append(enriched)
                remaining.append(enriched)
            else:
                enriched = {
                    **row,
                    "next_action": "no user link provided; port to NeoForge or skip if low value",
                }
                port_or_skip.append(enriched)
                remaining.append(enriched)

    write_csv(
        SCRIPT_DIR / "cobblemon_final_covered.csv",
        covered,
        ["mod_id", "name", "fabric_file", "reason", "final_status"],
    )
    write_csv(
        SCRIPT_DIR / "cobblemon_skipped_by_user.csv",
        skipped,
        ["mod_id", "name", "fabric_file", "reason", "final_status"],
    )
    write_csv(
        SCRIPT_DIR / "cobblemon_not_transferred.csv",
        remaining,
        ["mod_id", "name", "fabric_file", "reason", "link_slug", "link_kind", "link_file_or_version", "url", "next_action"],
    )
    write_csv(
        SCRIPT_DIR / "cobblemon_pending_with_user_links.csv",
        pending_with_links,
        ["mod_id", "name", "fabric_file", "reason", "link_slug", "link_kind", "link_file_or_version", "url", "next_action"],
    )
    write_csv(
        SCRIPT_DIR / "cobblemon_needs_port_or_skip_no_link.csv",
        port_or_skip,
        ["mod_id", "name", "fabric_file", "reason", "next_action"],
    )

    lines = [
        "# Cobblemon Mods Not Yet Transferred",
        "",
        f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "These Fabric-side mods are not currently represented in FactorMoon by a matching/equivalent active modId.",
        "They need a verified NeoForge build, a manual compatibility decision, or a port.",
        "",
        "## Current Counts",
        f"- Covered in current FactorMoon: {len(covered)}",
        f"- Explicitly skipped by user/balance rule: {len(skipped)}",
        f"- Still not transferred: {len(remaining)}",
        f"- Not transferred but user already provided a link: {len(pending_with_links)}",
        f"- No provided link; port to NeoForge or skip decision needed: {len(port_or_skip)}",
        "",
        "## Pending From Provided Links",
        "",
        "| mod_id | name | Fabric file | link | next action |",
        "|---|---|---|---|---|",
    ]
    for row in pending_with_links:
        lines.append(
            f"| `{row['mod_id']}` | {row['name']} | `{row['fabric_file']}` | {row['url']} | {row['next_action']} |"
        )
    lines.extend(
        [
            "",
            "## No Provided Link: Port Or Skip",
            "",
            "| mod_id | name | Fabric file | next action |",
            "|---|---|---|---|",
        ]
    )
    for row in port_or_skip:
        lines.append(f"| `{row['mod_id']}` | {row['name']} | `{row['fabric_file']}` | {row['next_action']} |")
    lines.extend(
        [
            "",
            "## Explicitly Skipped",
            "",
            "| mod_id | name | Fabric file | reason |",
            "|---|---|---|---|",
        ]
    )
    for row in skipped:
        lines.append(f"| `{row['mod_id']}` | {row['name']} | `{row['fabric_file']}` | skipped by user/balance rule |")
    (FACTOR_MOON / "COBBLEMON_NOT_TRANSFERRED.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    summary = {
        "covered": len(covered),
        "skipped_by_user": len(skipped),
        "remaining": len(remaining),
        "pending_with_user_links": len(pending_with_links),
        "needs_port_or_skip_no_link": len(port_or_skip),
    }
    (SCRIPT_DIR / "cobblemon_transfer_refresh_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
