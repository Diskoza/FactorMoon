from __future__ import annotations

import csv
import html
import json
import re
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

import factor_moon_audit as audit


SCRIPT_DIR = Path(__file__).resolve().parent
FACTOR_MOON = SCRIPT_DIR.parent
INSTANCES = FACTOR_MOON.parent
DOWNLOAD_DIR = SCRIPT_DIR / "downloads"
MODS_DIR = FACTOR_MOON / "mods"
DATAPACKS_DIR = FACTOR_MOON / "datapacks"

USER_AGENT = "Mozilla/5.0 FactorMoonBuilder/1.0"
TIMEOUT = 45
MAX_INSTALL = 200

FORBIDDEN_MOD_IDS = {
    "immersive_aircraft",
    "smallships",
    "niftycarts",
    "infinite-music",
}
FORBIDDEN_SLUGS = {
    "immersive-aircraft",
    "small-ships",
    "small-ships-mod",
    "niftycarts",
    "infinite-music",
}
EXPECTED_ALIASES = {
    "better_tooltips": {"better_tooltips", "tooltipfix"},
    "catchrate-display": {"catchrate-display", "catchrate_display"},
    "cobblemon-battle-extras": {"cobblemon-battle-extras", "cobblemon_battle_extras"},
    "cobblemon_playerxp": {"cobblemon_playerxp", "playerxp"},
    "cobblemon_tms": {"cobblemon_tms", "tmcraft"},
    "cobblesafepastures": {"cobblesafepastures", "safepastures"},
    "cosmeticarmor": {"cosmeticarmor", "cosmeticarmorreworked"},
    "customsplashscreen": {"customsplashscreen", "simplesplashscreen"},
    "euphoriapatcher": {"euphoriapatcher", "euphoria_patcher"},
    "kotlinforforge": {"kotlinforforge", "kotlin_for_forge"},
    "krypton": {"krypton", "krypton_fnp"},
    "mega_showdown": {"mega_showdown", "megashowdown"},
    "moarconcrete": {"moarconcrete", "moreconcrete"},
    "modmenu": {"modmenu", "mod_menu"},
    "navas_zas": {"navas_zas", "zamega"},
    "nethermap": {"nethermap", "betternether"},
    "pasture-loot": {"pasture-loot", "pastureloot", "pasturelootnf"},
    "pastureloot": {"pastureloot", "pasture-loot"},
    "ping-wheel": {"ping-wheel", "ping_wheel"},
    "resourcepackoverrides": {"resourcepackoverrides", "resource_pack_overrides"},
    "roughlyenoughitems": {"roughlyenoughitems", "rei"},
    "safepastures": {"safepastures", "safepastures_neoforge"},
    "smartparticles": {"smartparticles", "smart_particles"},
    "sound_physics_remastered": {"sound_physics_remastered", "soundphysics"},
    "stardew_fishing_fabric": {"stardew_fishing_fabric", "stardew_fishing"},
    "tmcraft": {"tmcraft", "cobblemon_tm", "cobblemon_tms"},
    "tooltipfix": {"tooltipfix", "better_tooltips"},
    "tims_core": {"tims_core", "tim_core"},
    "unknown:cobblemon-additions-4.1.6": {"bca", "cobblemon_additions", "cobblemon-additions"},
    "unknown:EuphoriaPatcher-1.8.6-r5.7.1-fabric": {"euphoriapatcher", "euphoria_patcher"},
    "unknown:mega_showdown-fabric-1.6.12+1.7.3+1.21.1": {"mega_showdown", "megashowdown"},
}
EXPLICIT_DATAPACK_IDS = {
    "mr_cobble_cafforms",
    "mr_extra_moveanimscobblemon",
}


def http_get(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return response.read()


def download_file(url: str, dst: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response, dst.open("wb") as out:
        shutil.copyfileobj(response, out)


def download_with_fallback(meta: dict, dst: Path) -> str:
    try:
        download_file(meta["download_url"], dst)
        return meta["download_url"]
    except Exception:
        fallback = meta.get("fallback_download_url")
        if not fallback:
            raise
        download_file(fallback, dst)
        return fallback


def strip_html(raw: bytes) -> list[str]:
    text = raw.decode("utf-8", errors="ignore")
    text = re.sub(r"(?is)<script.*?</script>", "\n", text)
    text = re.sub(r"(?is)<style.*?</style>", "\n", text)
    text = re.sub(r"(?is)<[^>]+>", "\n", text)
    text = html.unescape(text)
    return [line.strip() for line in text.splitlines() if line.strip()]


def find_after(lines: list[str], label: str) -> str:
    for index, line in enumerate(lines):
        if line.lower() == label.lower():
            for value in lines[index + 1 : index + 8]:
                if value and value.lower() != label.lower():
                    return value
    return ""


def parse_curseforge(url: str) -> dict:
    match = re.search(r"/minecraft/([^/]+)/([^/]+)/files/(\d+)", url)
    if not match:
        raise ValueError(f"Unsupported CurseForge URL: {url}")
    kind, slug, file_id_text = match.groups()
    file_id = int(file_id_text)
    project = json.loads(http_get(f"https://api.cfwidget.com/minecraft/{kind}/{slug}"))
    file_info = next((file for file in project.get("files", []) if int(file.get("id", -1)) == file_id), None)
    if not file_info:
        raise RuntimeError(f"Could not find file {file_id_text} in CFWidget project {slug}")
    file_name = file_info["name"]
    versions = set(file_info.get("versions") or [])
    game_ok = "1.21.1" in versions
    loader_ok = bool(versions & {"NeoForge", "Forge"})
    project_id = str(project.get("id", ""))
    if not project_id:
        raise RuntimeError(f"Could not resolve project id for {slug}")
    cursemaven_name = f"{slug}-{project_id}-{file_id_text}.jar"
    maven_slug = urllib.parse.quote(f"{slug}-{project_id}", safe="-_.")
    cdn_name = urllib.parse.quote(file_name, safe="-_.+")
    first = file_id // 1000
    second = file_id % 1000
    cdn_url = f"https://edge.forgecdn.net/files/{first}/{second:03d}/{cdn_name}"
    maven_url = f"https://cursemaven.com/curse/maven/{maven_slug}/{file_id_text}/{urllib.parse.quote(cursemaven_name, safe='-_.')}"
    return {
        "source": "curseforge",
        "kind": kind,
        "slug": slug,
        "project_id": project_id,
        "file_id": file_id_text,
        "file_name": file_name,
        "download_url": maven_url,
        "fallback_download_url": cdn_url,
        "game_ok": game_ok,
        "loader_ok": loader_ok,
        "versions": ";".join(sorted(versions)),
        "display": file_info.get("display", ""),
    }


def parse_modrinth(url: str) -> dict:
    match = re.search(r"modrinth\.com/([^/]+)/([^/]+)/version/([^/?#]+)", url)
    if not match:
        raise ValueError(f"Unsupported Modrinth URL: {url}")
    kind, slug, version_token = match.groups()
    version_token = urllib.parse.unquote(version_token)
    version = None
    try:
        version = json.loads(http_get(f"https://api.modrinth.com/v2/version/{urllib.parse.quote(version_token, safe='')}"))
    except urllib.error.HTTPError:
        versions = json.loads(http_get(f"https://api.modrinth.com/v2/project/{slug}/version"))
        for candidate in versions:
            if candidate.get("id") == version_token or candidate.get("version_number") == version_token:
                version = candidate
                break
    if not version:
        raise RuntimeError(f"Could not resolve Modrinth version {slug}/{version_token}")
    files = version.get("files") or []
    primary = next((file for file in files if file.get("primary")), files[0] if files else None)
    if not primary:
        raise RuntimeError("Modrinth version has no files")
    loaders = set(version.get("loaders") or [])
    game_versions = set(version.get("game_versions") or [])
    return {
        "source": "modrinth",
        "kind": kind,
        "slug": slug,
        "file_id": version.get("id", version_token),
        "file_name": primary["filename"],
        "download_url": primary["url"],
        "game_ok": "1.21.1" in game_versions,
        "loader_ok": bool(loaders & {"neoforge", "forge", "datapack"}),
        "loaders": ";".join(sorted(loaders)),
        "game_versions": ";".join(sorted(game_versions)),
    }


def read_rows() -> list[dict]:
    path = SCRIPT_DIR / "cobblemon_pending_with_user_links.csv"
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    seen = set()
    unique = []
    for row in rows:
        url = row.get("url", "")
        if not url or url in seen:
            continue
        seen.add(url)
        unique.append(row)
    return unique[:MAX_INSTALL]


def existing_mod_ids() -> set[str]:
    ids = set()
    for jar in MODS_DIR.glob("*.jar"):
        record = audit.parse_jar(jar).__dict__
        for mod_id in record.get("mod_ids", "").split(";"):
            if mod_id:
                ids.add(mod_id)
        if "kotlinforforge" in jar.name.lower():
            ids.add("kotlinforforge")
    return ids


def expected_names(expected: str) -> set[str]:
    names = {expected}
    names.update(EXPECTED_ALIASES.get(expected, set()))
    if expected.startswith("unknown:"):
        names.add(expected.removeprefix("unknown:"))
    return {name for name in names if name}


def archive_has_pack_mcmeta(path: Path) -> bool:
    try:
        with zipfile.ZipFile(path) as zf:
            return "pack.mcmeta" in zf.namelist()
    except zipfile.BadZipFile:
        return False


def choose_target(expected: str, link_kind: str, local_path: Path, record: dict) -> tuple[Path, str]:
    metadata = record.get("metadata", "")
    has_mod_metadata = "META-INF/neoforge.mods.toml" in metadata or "META-INF/mods.toml" in metadata
    if has_mod_metadata:
        return MODS_DIR / local_path.name, "mods"
    if expected in EXPLICIT_DATAPACK_IDS or link_kind == "datapack" or archive_has_pack_mcmeta(local_path):
        return DATAPACKS_DIR / local_path.name, "datapacks"
    return MODS_DIR / local_path.name, "mods"


def has_good_mod_metadata(record: dict) -> bool:
    metadata = record.get("metadata", "")
    loaders = record.get("loaders", "")
    return "META-INF/neoforge.mods.toml" in metadata or "META-INF/mods.toml" in metadata or "neoforge" in loaders or "forge" in loaders


def expected_matches(expected: str, record: dict, target_bucket: str) -> bool:
    if target_bucket == "datapacks":
        return True
    mod_ids = set(filter(None, record.get("mod_ids", "").split(";")))
    if not mod_ids:
        return False
    return bool(mod_ids & expected_names(expected))


def ensure_inside_factor(path: Path) -> None:
    root = FACTOR_MOON.resolve()
    resolved = path.resolve()
    if not (resolved == root or root in resolved.parents):
        raise RuntimeError(f"Refusing to write outside FactorMoon: {path}")


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def process(row: dict, installed_ids: set[str]) -> dict:
    url = row["url"]
    expected = row["mod_id"]
    slug = row.get("link_slug", "")
    if expected in FORBIDDEN_MOD_IDS or slug in FORBIDDEN_SLUGS:
        return {**row, "status": "skipped_forbidden", "downloaded_file": "", "installed_to": "", "details": "skip rule"}
    if expected in installed_ids:
        return {**row, "status": "skipped_already_installed", "downloaded_file": "", "installed_to": "", "details": expected}

    try:
        meta = parse_modrinth(url) if "modrinth.com" in url else parse_curseforge(url)
        if not meta.get("game_ok"):
            return {**row, "status": "skipped_wrong_game_version", "downloaded_file": "", "installed_to": "", "details": json.dumps(meta, ensure_ascii=False)}
        if not meta.get("loader_ok"):
            return {**row, "status": "skipped_wrong_loader", "downloaded_file": "", "installed_to": "", "details": json.dumps(meta, ensure_ascii=False)}

        source_dir = DOWNLOAD_DIR / meta["source"]
        source_dir.mkdir(parents=True, exist_ok=True)
        local = source_dir / meta["file_name"]
        used_url = ""
        if not local.exists() or local.stat().st_size == 0:
            used_url = download_with_fallback(meta, local)
            time.sleep(0.15)

        record = audit.parse_jar(local).__dict__ if local.suffix.lower() == ".jar" else {"metadata": "", "loaders": "", "mod_ids": ""}
        target, bucket = choose_target(expected, row.get("link_kind", ""), local, record)
        ensure_inside_factor(target)
        if bucket == "mods" and not has_good_mod_metadata(record):
            return {**row, "status": "skipped_no_neoforge_metadata", "downloaded_file": audit.safe_rel(local), "installed_to": "", "details": json.dumps({**meta, **record}, ensure_ascii=False)}
        if not expected_matches(expected, record, bucket):
            return {**row, "status": "skipped_mod_id_mismatch", "downloaded_file": audit.safe_rel(local), "installed_to": "", "details": json.dumps({**meta, **record}, ensure_ascii=False)}
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            status = "already_downloaded_target_exists"
        else:
            shutil.copy2(local, target)
            status = "installed"
            for mod_id in record.get("mod_ids", "").split(";"):
                if mod_id:
                    installed_ids.add(mod_id)
        if used_url:
            meta["used_download_url"] = used_url
        return {**row, "status": status, "downloaded_file": audit.safe_rel(local), "installed_to": audit.safe_rel(target), "details": json.dumps(meta, ensure_ascii=False)}
    except Exception as exc:
        return {**row, "status": f"error:{type(exc).__name__}", "downloaded_file": "", "installed_to": "", "details": str(exc)}


def main() -> int:
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    installed_ids = existing_mod_ids()
    rows = []
    for row in read_rows():
        result = process(row, installed_ids)
        rows.append(result)
        print(f"{result['status']}: {row.get('mod_id')} <- {row.get('url')}", flush=True)
    fieldnames = [
        "status",
        "mod_id",
        "name",
        "fabric_file",
        "link_slug",
        "link_kind",
        "link_file_or_version",
        "url",
        "downloaded_file",
        "installed_to",
        "details",
        "reason",
        "next_action",
    ]
    write_csv(SCRIPT_DIR / "download_install_results.csv", rows, fieldnames)
    summary = {}
    for row in rows:
        summary[row["status"]] = summary.get(row["status"], 0) + 1
    (SCRIPT_DIR / "download_install_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
