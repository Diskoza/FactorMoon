from __future__ import annotations

import csv
import json
import shutil
import urllib.request
from pathlib import Path

import factor_moon_audit as audit


SCRIPT_DIR = Path(__file__).resolve().parent
FACTOR_MOON = SCRIPT_DIR.parent
DOWNLOAD_DIR = SCRIPT_DIR / "downloads" / "modrinth"
MODS_DIR = FACTOR_MOON / "mods"

USER_AGENT = "Mozilla/5.0 FactorMoonBuilder/1.0"
TIMEOUT = 45


DEPENDENCIES = [
    {
        "reason": "BetterNether dependency: bclib >= 21.0.14",
        "project": "bclib-neoforge",
        "version_id": "OaVg9Swk",
        "expected_mod_id": "bclib",
    },
    {
        "reason": "BetterNether dependency: wover >= 21.0.14",
        "project": "worldweaver-neoforge",
        "version_id": "jJJtSGMZ",
        "expected_mod_id": "wover",
    },
    {
        "reason": "BetterNether dependency: wunderlib >= 21.0.9",
        "project": "wunderlib-neoforge",
        "version_id": "5db3GZzg",
        "expected_mod_id": "wunderlib",
    },
    {
        "reason": "Capture XP dependency; 1.7.3 branch matches current Cobblemon/CaptureXP",
        "project": "cobblemon-tim-core",
        "version_id": "QQO61rRS",
        "expected_mod_id": "tim_core",
    },
    {
        "reason": "RCT Mod dependency: rctapi >= 0.15.0-beta",
        "project": "rctapi",
        "version_id": "zpphgptV",
        "expected_mod_id": "rctapi",
    },
]


def http_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return json.loads(response.read())


def download(url: str, dst: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response, dst.open("wb") as out:
        shutil.copyfileobj(response, out)


def ensure_inside_factor(path: Path) -> None:
    root = FACTOR_MOON.resolve()
    resolved = path.resolve()
    if not (resolved == root or root in resolved.parents):
        raise RuntimeError(f"Refusing to write outside FactorMoon: {path}")


def process(dep: dict) -> dict:
    version = http_json(f"https://api.modrinth.com/v2/version/{dep['version_id']}")
    files = version.get("files") or []
    primary = next((file for file in files if file.get("primary")), files[0] if files else None)
    if not primary:
        raise RuntimeError(f"No file in Modrinth version {dep['version_id']}")

    loaders = set(version.get("loaders") or [])
    game_versions = set(version.get("game_versions") or [])
    if "1.21.1" not in game_versions:
        raise RuntimeError(f"{dep['project']} is not marked for Minecraft 1.21.1: {game_versions}")
    if "neoforge" not in loaders and "forge" not in loaders:
        raise RuntimeError(f"{dep['project']} is not marked NeoForge/Forge: {loaders}")

    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    local = DOWNLOAD_DIR / primary["filename"]
    if not local.exists() or local.stat().st_size == 0:
        download(primary["url"], local)

    record = audit.parse_jar(local).__dict__
    mod_ids = set(filter(None, record.get("mod_ids", "").split(";")))
    if dep["expected_mod_id"] not in mod_ids:
        raise RuntimeError(f"{local.name} has mod ids {sorted(mod_ids)}, expected {dep['expected_mod_id']}")

    target = MODS_DIR / local.name
    ensure_inside_factor(target)
    status = "already_present" if target.exists() else "installed"
    if not target.exists():
        shutil.copy2(local, target)

    return {
        "status": status,
        "project": dep["project"],
        "version_number": version.get("version_number", ""),
        "version_id": dep["version_id"],
        "expected_mod_id": dep["expected_mod_id"],
        "mod_ids": record.get("mod_ids", ""),
        "downloaded_file": audit.safe_rel(local),
        "installed_to": audit.safe_rel(target),
        "reason": dep["reason"],
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    fieldnames = [
        "status",
        "project",
        "version_number",
        "version_id",
        "expected_mod_id",
        "mod_ids",
        "downloaded_file",
        "installed_to",
        "reason",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    rows = []
    for dep in DEPENDENCIES:
        row = process(dep)
        rows.append(row)
        print(f"{row['status']}: {row['project']} {row['version_number']}")
    write_csv(SCRIPT_DIR / "required_dependency_installs.csv", rows)
    summary: dict[str, int] = {}
    for row in rows:
        summary[row["status"]] = summary.get(row["status"], 0) + 1
    (SCRIPT_DIR / "required_dependency_installs_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
