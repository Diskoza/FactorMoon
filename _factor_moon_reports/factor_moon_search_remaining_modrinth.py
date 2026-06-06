from __future__ import annotations

import csv
import json
import urllib.parse
import urllib.request
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent

QUERIES = [
    ("cardinal-components", "Cardinal Components API"),
    ("cobblecuisine", "CobbleCuisine"),
    ("cobblemonbattlepositions", "Cobblemon Battle Positions"),
    ("cobblemon-fight-them-all", "Cobblemon Fight Them All"),
    ("CobbleverseBadges", "CobbleverseBadges"),
    ("Debugify", "Debugify"),
    ("Interactic", "Interactic"),
    ("Lucky Cozy Home Refurnished", "Cozy Home"),
    ("LumyMon", "LumyMon"),
    ("LumyREI", "LumyREI"),
    ("Only Bottle Caps", "Only Bottle Caps"),
    ("Poke Clothing", "Poke Clothing"),
    ("Pokeblocks", "Pokeblocks"),
    ("Resource Pack Options", "Resource Pack Options"),
    ("StackDeobfuscator", "StackDeobfuscator"),
    ("trinkets", "Trinkets"),
]


def http_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "FactorMoonBuilder/1.0"})
    with urllib.request.urlopen(req, timeout=45) as response:
        return json.loads(response.read())


def versions_for(slug: str) -> list[dict]:
    try:
        return http_json(f"https://api.modrinth.com/v2/project/{slug}/version")
    except Exception:
        return []


def main() -> int:
    rows = []
    for mod_id, query in QUERIES:
        search = http_json("https://api.modrinth.com/v2/search?limit=8&query=" + urllib.parse.quote(query))
        for hit in search.get("hits", []):
            slug = hit.get("slug", "")
            versions = versions_for(slug)
            matching = []
            for version in versions:
                loaders = set(version.get("loaders") or [])
                games = set(version.get("game_versions") or [])
                if "1.21.1" in games and loaders & {"neoforge", "forge"}:
                    matching.append(
                        {
                            "version_number": version.get("version_number", ""),
                            "version_id": version.get("id", ""),
                            "loaders": ";".join(sorted(loaders)),
                            "game_versions": ";".join(sorted(games)),
                            "files": ";".join(file.get("filename", "") for file in version.get("files", [])),
                        }
                    )
            rows.append(
                {
                    "wanted_mod_id": mod_id,
                    "query": query,
                    "hit_slug": slug,
                    "hit_title": hit.get("title", ""),
                    "project_id": hit.get("project_id", ""),
                    "client_side": hit.get("client_side", ""),
                    "server_side": hit.get("server_side", ""),
                    "source_url": hit.get("source_url", ""),
                    "project_url": "https://modrinth.com/mod/" + slug if slug else "",
                    "neoforge_1_21_1_matches": json.dumps(matching[:5], ensure_ascii=False),
                }
            )
    fieldnames = [
        "wanted_mod_id",
        "query",
        "hit_slug",
        "hit_title",
        "project_id",
        "client_side",
        "server_side",
        "source_url",
        "project_url",
        "neoforge_1_21_1_matches",
    ]
    with (SCRIPT_DIR / "remaining_modrinth_search.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    count = sum(1 for row in rows if row["neoforge_1_21_1_matches"] != "[]")
    print(json.dumps({"rows": len(rows), "hits_with_neoforge_1_21_1": count}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
