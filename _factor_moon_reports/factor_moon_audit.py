from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import tomllib
import zipfile
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import urlparse


SCRIPT_DIR = Path(__file__).resolve().parent
FACTOR_MOON = SCRIPT_DIR.parent
INSTANCES = FACTOR_MOON.parent
COBBLE_EXTRA = INSTANCES / "cobblemon-extra"

USER_LINKS = """
https://www.curseforge.com/minecraft/mc-mods/accessories-compat-layer/files/7585673
https://www.curseforge.com/minecraft/mc-mods/accessories/files/7583320
https://www.curseforge.com/minecraft/mc-mods/advancementdisable/files/5510148
https://www.curseforge.com/minecraft/mc-mods/advancement-plaques/files/8124727
https://www.curseforge.com/minecraft/mc-mods/beautify-decorate/files/5947973
https://www.curseforge.com/minecraft/mc-mods/better-beds/files/5437846
https://www.curseforge.com/minecraft/mc-mods/better-f1-reborn/files/5673620
https://www.curseforge.com/minecraft/mc-mods/betterf3/files/7436342
https://www.curseforge.com/minecraft/mc-mods/better-third-person/files/5833474
https://www.curseforge.com/minecraft/mc-mods/biome-replacer/files/7451481
https://www.curseforge.com/minecraft/mc-mods/brb/files/5512413
https://www.curseforge.com/minecraft/mc-mods/cobblemon-capture-xp/files/7568508
https://www.curseforge.com/minecraft/mc-mods/carved-wood/files/8074012
https://www.curseforge.com/minecraft/mc-mods/catch-indicator/files/7864851
https://www.curseforge.com/minecraft/mc-mods/cobblemon-catch-rate-display/files/8050485
https://www.curseforge.com/minecraft/mc-mods/cloth-config/files/7361439
https://modrinth.com/datapack/cobble-caf-forms/version/NEndOzch
https://modrinth.com/datapack/cobblemon-additions/version/3.8.1
https://www.curseforge.com/minecraft/mc-mods/cobbledgacha/files/7787787
https://www.curseforge.com/minecraft/mc-mods/cobbledollars/files/6604564
https://www.curseforge.com/minecraft/mc-mods/cobblefurnies/files/7969051
https://www.curseforge.com/minecraft/modpacks/cobblemon-neoforge/files/7568756
https://www.curseforge.com/minecraft/mc-mods/cobblemon-alpha-project/files/7631041
https://www.curseforge.com/minecraft/mc-mods/cobblemon-battle-extras/files/7968869
https://www.curseforge.com/minecraft/mc-mods/cobblemon-ride-on/files/6739719
https://www.curseforge.com/minecraft/mc-mods/cobblemon-journey-mounts/files/7440127
https://www.curseforge.com/minecraft/mc-mods/cobblemon-legends-untold-reborn/files/6198593
https://www.curseforge.com/minecraft/mc-mods/cobblemon-quests/files/7257241
https://modrinth.com/mod/cobblemon-shiny-rarities/version/0.2.1
https://www.curseforge.com/minecraft/mc-mods/cobblemon-wonder-trade/files/7725599
https://modrinth.com/mod/cobblemon-trainer-structures/version/1.7.0
https://www.curseforge.com/minecraft/mc-mods/cobblemonraiddens/files/8158997
https://www.curseforge.com/minecraft/mc-mods/cobblemon-pokenav/files/7940651
https://www.curseforge.com/minecraft/mc-mods/cobblepedia/files/7272042
https://modrinth.com/mod/cobbreeding/version/xt8IiPEN
https://www.curseforge.com/minecraft/mc-mods/continuity/files/5981335
https://www.curseforge.com/minecraft/mc-mods/cosmetic-armor-reworked/files/5610814
https://modrinth.com/mod/simple-splash-screen/version/1.21-1.3.2
https://www.curseforge.com/minecraft/mc-mods/default-options/files/7966181
https://www.curseforge.com/minecraft/mc-mods/dynamic-lights/files/7906440
https://www.curseforge.com/minecraft/mc-mods/entity-model-features/files/8063560
https://www.curseforge.com/minecraft/mc-mods/entity-texture-features-fabric/files/7930637
https://www.curseforge.com/minecraft/mc-mods/euphoria-patches/files/8177588
https://modrinth.com/datapack/extra-move-anims-cobblemon/version/1.7v1.0.2+mod
https://www.curseforge.com/minecraft/mc-mods/kotlin-for-forge/files/7471280
https://modrinth.com/mod/cobblemon-fight-or-flight-reborn/version/kyo4qCAc
https://www.curseforge.com/minecraft/mc-mods/forge-config-api-port/files/7213611
https://www.curseforge.com/minecraft/mc-mods/forgiving-void/files/7966159
https://www.curseforge.com/minecraft/mc-mods/globalpacks/files/6634585
https://www.curseforge.com/minecraft/mc-mods/highlight/files/7330434
https://www.curseforge.com/minecraft/mc-mods/huge-structure-blocks/files/7065481
https://www.curseforge.com/minecraft/mc-mods/krypton-fnp/files/7461802
https://www.curseforge.com/minecraft/mc-mods/legendary-monuments-cobblemon/files/7095325
https://modrinth.com/mod/lenientdeathforneoforge/version/1.1.2
https://modrinth.com/mod/libjf/version/3.17.6+forge
https://www.curseforge.com/minecraft/mc-mods/lootrmon/files/7339627
https://www.curseforge.com/minecraft/mc-mods/cobblemon-mega-showdown/files/8102863
https://www.curseforge.com/minecraft/mc-mods/more-concrete/files/6359256
https://www.curseforge.com/minecraft/mc-mods/mod-menu-neoforge-edition/files/7312908
https://www.curseforge.com/minecraft/mc-mods/morecobblemontweaks/files/7593359
https://www.curseforge.com/minecraft/mc-mods/music-notification/files/7918231
https://www.curseforge.com/minecraft/mc-mods/betternether-neoforge/files/8194859
https://www.curseforge.com/minecraft/mc-mods/not-enough-crashes-forge/files/6598103
https://www.curseforge.com/minecraft/mc-mods/packet-fixer/files/7221528
https://www.curseforge.com/minecraft/mc-mods/forgedpaginatedadvancements/files/7127823
https://www.curseforge.com/minecraft/mc-mods/particle-rain/files/8055433
https://www.curseforge.com/minecraft/mc-mods/particular-reforged/files/8161696
https://www.curseforge.com/minecraft/mc-mods/cobblemon-pasture-loot-neoforged/files/7772551
https://modrinth.com/mod/ping-wheel/version/Zrh2Fmn9
https://www.curseforge.com/minecraft/mc-mods/platform/files/8075942
https://www.curseforge.com/minecraft/mc-mods/cobblemon-playerxp/files/7886114
https://modrinth.com/mod/rctapi/version/0.15.2-beta
https://www.curseforge.com/minecraft/mc-mods/rctmod/files/7913180
https://www.curseforge.com/minecraft/mc-mods/reeses-sodium-options/files/8141953
https://modrinth.com/mod/resource-pack-overrides/version/v21.1.0-1.21.1-NeoForge
https://www.curseforge.com/minecraft/mc-mods/roughly-enough-items/files/6199140
https://www.curseforge.com/minecraft/mc-mods/cobblemon-safepastures/files/7248005
https://www.curseforge.com/minecraft/mc-mods/simplehats/files/5970513
https://www.curseforge.com/minecraft/mc-mods/smart-particles/files/7470043
https://www.curseforge.com/minecraft/mc-mods/sodium-extra/files/8189182
https://modrinth.com/mod/sound-physics-remastered/version/neoforge-1.21.1-1.5.1
https://www.curseforge.com/minecraft/mc-mods/stardew-fishing/files/8070778
https://www.curseforge.com/minecraft/mc-mods/tectonic/files/7903156
https://modrinth.com/mod/cobblemon-tim-core/version/1.8.0-neoforge-1.32.0-r1
https://www.curseforge.com/minecraft/mc-mods/cobblemon-tm-neoforge/files/7257566
https://www.curseforge.com/minecraft/mc-mods/better-tooltips-neoforge/files/6372309
https://www.curseforge.com/minecraft/mc-mods/trinkets-updated/files/8187944
https://www.curseforge.com/minecraft/mc-mods/vanillabackport/files/8194329
https://modrinth.com/mod/villagerconfig/version/neoforge-4.5.3+1.21.1
https://www.curseforge.com/minecraft/mc-mods/navas-za-megas/files/7961237
https://www.curseforge.com/minecraft/mc-mods/just-zoom/files/6290230
"""

FORBIDDEN_SLUGS = {"immersive-aircraft", "small-ships", "small-ships-mod", "niftycarts", "infinite-music"}

EXPECTED_IDS = {
    "accessories-compat-layer": "accessories_compat_layer",
    "accessories": "accessories",
    "advancementdisable": "advancementdisable",
    "advancement-plaques": "advancementplaques",
    "beautify-decorate": "beautify",
    "better-beds": "betterbeds",
    "better-f1-reborn": "betterf1",
    "betterf3": "betterf3",
    "better-third-person": "betterthirdperson",
    "biome-replacer": "biome_replacer",
    "brb": "brb",
    "cobblemon-capture-xp": "capture_xp",
    "carved-wood": "carved_wood",
    "catch-indicator": "catchindicator",
    "cobblemon-catch-rate-display": "catchrate-display",
    "cloth-config": "cloth_config",
    "cobble-caf-forms": "mr_cobble_cafforms",
    "cobblemon-additions": "unknown:cobblemon-additions-4.1.6",
    "cobbledgacha": "cobbledgacha",
    "cobbledollars": "cobbledollars",
    "cobblefurnies": "cobblefurnies",
    "cobblemon-alpha-project": "mr_cobblemon_alphas",
    "cobblemon-battle-extras": "cobblemon-battle-extras",
    "cobblemon-ride-on": "cobblemon_ride_on",
    "cobblemon-journey-mounts": "mr_cobblemon_journeymounts",
    "cobblemon-legends-untold-reborn": "cobblemon_legends_reborn",
    "cobblemon-quests": "cobblemon_quests",
    "cobblemon-shiny-rarities": "cobblemon_shiny_rarities",
    "cobblemon-wonder-trade": "cobblemon_wonder_trade",
    "cobblemon-trainer-structures": "cobblemonopponents",
    "cobblemonraiddens": "cobblemonraiddens",
    "cobblemon-pokenav": "cobblenav",
    "cobblepedia": "cobblepedia",
    "cobbreeding": "cobbreeding",
    "continuity": "continuity",
    "cosmetic-armor-reworked": "cosmeticarmor",
    "simple-splash-screen": "customsplashscreen",
    "default-options": "defaultoptions",
    "dynamic-lights": "dynamiclights",
    "entity-model-features": "entity_model_features",
    "entity-texture-features-fabric": "entity_texture_features",
    "euphoria-patches": "euphoriapatcher",
    "extra-move-anims-cobblemon": "mr_extra_moveanimscobblemon",
    "kotlin-for-forge": "kotlinforforge",
    "cobblemon-fight-or-flight-reborn": "fightorflight",
    "forge-config-api-port": "forgeconfigapiport",
    "forgiving-void": "forgivingvoid",
    "globalpacks": "globalpacks",
    "highlight": "highlight",
    "huge-structure-blocks": "hugestructureblocks",
    "krypton-fnp": "krypton",
    "legendary-monuments-cobblemon": "legendarymonuments",
    "lenientdeathforneoforge": "lenientdeath",
    "libjf": "libjf",
    "lootrmon": "lootrmon",
    "cobblemon-mega-showdown": "mega_showdown",
    "more-concrete": "moarconcrete",
    "mod-menu-neoforge-edition": "modmenu",
    "morecobblemontweaks": "more_cobblemon_tweaks",
    "music-notification": "musicnotification",
    "betternether-neoforge": "nethermap",
    "not-enough-crashes-forge": "notenoughcrashes",
    "packet-fixer": "packetfixer",
    "forgedpaginatedadvancements": "paginatedadvancements",
    "particle-rain": "particlerain",
    "particular-reforged": "particular",
    "cobblemon-pasture-loot-neoforged": "pastureloot",
    "ping-wheel": "ping-wheel",
    "platform": "platform",
    "cobblemon-playerxp": "cobblemon_playerxp",
    "rctapi": "rctapi",
    "rctmod": "rctmod",
    "reeses-sodium-options": "reeses_sodium_options",
    "resource-pack-overrides": "resourcepackoverrides",
    "roughly-enough-items": "roughlyenoughitems",
    "cobblemon-safepastures": "cobblesafepastures",
    "simplehats": "simplehats",
    "smart-particles": "smartparticles",
    "sodium-extra": "sodium_extra",
    "sound-physics-remastered": "sound_physics_remastered",
    "stardew-fishing": "stardew_fishing_fabric",
    "tectonic": "tectonic",
    "cobblemon-tim-core": "tims_core",
    "cobblemon-tm-neoforge": "cobblemon_tms",
    "better-tooltips-neoforge": "better_tooltips",
    "trinkets-updated": "trinkets",
    "vanillabackport": "vanillabackport",
    "villagerconfig": "villagerconfig",
    "navas-za-megas": "navas_zas",
    "just-zoom": "justzoom",
}

INSTALLED_ID_ALIASES = {
    "catchrate-display": ["catchrate_display"],
    "ping-wheel": ["ping_wheel"],
    "mega_showdown": ["mega_showdown", "megashowdown"],
    "kotlinforforge": ["kotlin_for_forge"],
    "roughlyenoughitems": ["rei"],
    "resourcepackoverrides": ["resource_pack_overrides"],
    "tims_core": ["cobblemon_tim_core", "tim_core"],
    "cobblemon_tms": ["cobblemon_tm", "tms"],
    "better_tooltips": ["bettertooltips"],
}

PERSONAL_PATTERNS = [
    "cobbleverse",
    "cobblemon-extra-ride-compat",
    "stardew-fishing",
    "legendarymonuments-cobbleverse",
    "cobbleversebadges",
    "cobblemon-additions",
    "cobbleverse - pokemon adventure",
]

TEXT_SUFFIXES = {
    ".json",
    ".lang",
    ".txt",
    ".mcmeta",
    ".properties",
    ".toml",
    ".snbt",
    ".js",
}

HINT_RE = re.compile(
    r"(ru_ru|cobblepedia|cobblenav|pokenav|pokedex|dex|move|attack|battle|patchouli|journal|trainer|translation|lang)",
    re.IGNORECASE,
)
CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
FOCUSED_NEEDLES = {
    "cobblepedia": [
        "book.cobblepedia",
        "assets/cobblepedia/lang/ru_ru.json",
        "patchouli_books/cobblepedia/ru_ru",
        "patchouli_books/cobblepedia",
    ],
    "cobblenav_pokenav": [
        "assets/cobblenav/lang/ru_ru.json",
        "gui.cobblenav",
        "pokenav",
        "pokefinder",
    ],
    "battle_move_descriptions": [
        "assets/cobblemon-battle-extras/lang/ru_ru.json",
        "move.battleinfo",
        "move.description",
        "battleinfo",
    ],
}


@dataclass
class JarRecord:
    rel_path: str
    file_name: str
    size: int
    sha1: str
    metadata: str
    mod_ids: str
    display_names: str
    loaders: str


def safe_rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(INSTANCES.resolve()))
    except ValueError:
        return str(path)


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def sha1(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text_from_zip(zf: zipfile.ZipFile, name: str, max_bytes: int = 2_000_000) -> str:
    info = zf.getinfo(name)
    if info.file_size > max_bytes:
        return ""
    data = zf.read(name)
    for encoding in ("utf-8", "utf-8-sig", "cp1251", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return ""


def parse_fabric_json(text: str) -> tuple[list[str], list[str]]:
    try:
        data = json.loads(text)
    except Exception:
        return [], []
    mod_id = data.get("id")
    provides = data.get("provides", [])
    name = data.get("name")
    ids = [str(mod_id)] if mod_id else []
    if isinstance(provides, list):
        ids.extend(str(provided) for provided in provides if provided)
    return ids, ([str(name)] if name else [])


def parse_toml_like(text: str) -> tuple[list[str], list[str]]:
    try:
        data = tomllib.loads(text)
        mods = data.get("mods", [])
        if isinstance(mods, dict):
            mods = [mods]
        ids = []
        names = []
        for mod in mods:
            if not isinstance(mod, dict):
                continue
            mod_id = mod.get("modId")
            display = mod.get("displayName")
            if mod_id:
                ids.append(str(mod_id))
            if display:
                names.append(str(display))
        if ids:
            return ids, names
    except Exception:
        pass

    ids = []
    names = []
    blocks = re.split(r"(?m)^\s*\[\[", text)
    for block in blocks:
        header, _, rest = block.partition("]]")
        if header.strip() != "mods":
            continue
        mod_match = re.search(r"(?im)^\s*modId\s*=\s*['\"]([^'\"]+)['\"]", rest)
        if mod_match:
            ids.append(mod_match.group(1))
        name_match = re.search(r"(?im)^\s*displayName\s*=\s*['\"]([^'\"]+)['\"]", rest)
        if name_match:
            names.append(name_match.group(1))
    if not ids:
        inline = re.search(r"(?is)\bmods\s*=\s*\[(.*?)\]\s*(?:\r?\n\s*\[|$)", text)
        if inline:
            for match in re.finditer(r"modId\s*=\s*['\"]([^'\"]+)['\"]", inline.group(1)):
                ids.append(match.group(1))
            for match in re.finditer(r"displayName\s*=\s*['\"]([^'\"]+)['\"]", inline.group(1)):
                names.append(match.group(1))
    return ids, names


def parse_jar(path: Path) -> JarRecord:
    metadata = []
    mod_ids = []
    names = []
    loaders = []
    try:
        with zipfile.ZipFile(path) as zf:
            entries = set(zf.namelist())
            if "fabric.mod.json" in entries:
                metadata.append("fabric.mod.json")
                loaders.append("fabric")
                ids, display = parse_fabric_json(read_text_from_zip(zf, "fabric.mod.json"))
                mod_ids.extend(ids)
                names.extend(display)
            for toml_name in ("META-INF/neoforge.mods.toml", "META-INF/mods.toml"):
                if toml_name in entries:
                    metadata.append(toml_name)
                    loaders.append("neoforge" if "neoforge" in toml_name else "forge")
                    ids, display = parse_toml_like(read_text_from_zip(zf, toml_name))
                    mod_ids.extend(ids)
                    names.extend(display)
    except zipfile.BadZipFile:
        metadata.append("bad_zip")
    except Exception as exc:
        metadata.append(f"error:{type(exc).__name__}")

    unique_ids = []
    for mod_id in mod_ids:
        if mod_id and mod_id not in unique_ids:
            unique_ids.append(mod_id)
    unique_names = []
    for name in names:
        if name and name not in unique_names:
            unique_names.append(name)

    return JarRecord(
        rel_path=safe_rel(path),
        file_name=path.name,
        size=path.stat().st_size,
        sha1=sha1(path),
        metadata=";".join(metadata),
        mod_ids=";".join(unique_ids),
        display_names=";".join(unique_names),
        loaders=";".join(dict.fromkeys(loaders)),
    )


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def inventory_jars(base: Path) -> list[dict]:
    rows = []
    if not base.exists():
        return rows
    for jar in sorted(base.glob("*.jar"), key=lambda p: p.name.lower()):
        record = parse_jar(jar)
        rows.append(record.__dict__)
    return rows


def parse_not_transferred() -> list[dict]:
    report = FACTOR_MOON / "COBBLEMON_NOT_TRANSFERRED.md"
    rows = []
    if not report.exists():
        return rows
    for line in report.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `") or "|---" in line:
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 4:
            continue
        rows.append(
            {
                "mod_id": parts[0].strip("`"),
                "name": parts[1],
                "fabric_file": parts[2].strip("`"),
                "reason": parts[3],
            }
        )
    return rows


def parse_user_link(raw: str) -> dict:
    parsed = urlparse(raw)
    parts = [part for part in parsed.path.split("/") if part]
    result = {
        "url": raw,
        "source": parsed.netloc,
        "kind": "",
        "slug": "",
        "file_or_version": "",
        "expected_mod_id": "",
    }
    if parsed.netloc.endswith("curseforge.com") and len(parts) >= 5:
        result["kind"] = parts[1]
        result["slug"] = parts[2]
        result["file_or_version"] = parts[4]
    elif parsed.netloc.endswith("modrinth.com") and len(parts) >= 4:
        result["kind"] = parts[0]
        result["slug"] = parts[1]
        result["file_or_version"] = parts[3]
    result["expected_mod_id"] = EXPECTED_IDS.get(result["slug"], "")
    return result


def best_missing_match(slug: str, missing: list[dict]) -> tuple[str, str, str]:
    if not slug:
        return "", "", ""
    slug_norm = normalize(slug)
    best_score = 0.0
    best = None
    for row in missing:
        candidates = [row["mod_id"], row["name"], row["fabric_file"]]
        row_score = max(SequenceMatcher(None, slug_norm, normalize(c)).ratio() for c in candidates)
        if row_score > best_score:
            best_score = row_score
            best = row
    if not best or best_score < 0.45:
        return "", "", ""
    return best["mod_id"], best["name"], f"{best_score:.3f}"


def installed_ids(rows: list[dict]) -> set[str]:
    ids = set()
    for row in rows:
        for mod_id in row.get("mod_ids", "").split(";"):
            if mod_id:
                ids.add(mod_id)
    return ids


def id_is_present(expected: str, ids: set[str]) -> bool:
    if expected in ids:
        return True
    for alias in INSTALLED_ID_ALIASES.get(expected, []):
        if alias in ids:
            return True
    return False


def link_decisions(factor_rows: list[dict], missing_rows: list[dict]) -> list[dict]:
    ids = installed_ids(factor_rows)
    rows = []
    for raw in [line.strip() for line in USER_LINKS.splitlines() if line.strip()]:
        parsed = parse_user_link(raw)
        slug = parsed["slug"]
        expected = parsed["expected_mod_id"]
        match_id, match_name, match_score = best_missing_match(slug, missing_rows)
        if not expected:
            expected = match_id
        decision = "needs_download_and_metadata_check"
        note = "verify loader, Minecraft 1.21.1, NeoForge metadata, and dependencies before copying to mods"
        destination = "mods"
        if slug in FORBIDDEN_SLUGS:
            decision = "skip_forbidden_by_user"
            note = "user explicitly said not to install this"
            destination = "skip"
        elif parsed["kind"] == "modpacks":
            decision = "skip_modpack_file"
            note = "CurseForge modpack file is not a single mod jar for mods/"
            destination = "skip"
        elif parsed["kind"] == "datapack":
            destination = "datapacks"
            note = "datapack/resource pack candidate; verify pack_format and whether active data already exists"
        elif expected and id_is_present(expected, ids):
            decision = "already_present_or_equivalent"
            note = "a matching/equivalent mod id is already present in FactorMoon"
        rows.append(
            {
                "decision": decision,
                "destination": destination,
                "source": parsed["source"],
                "kind": parsed["kind"],
                "slug": slug,
                "file_or_version": parsed["file_or_version"],
                "expected_mod_id": expected,
                "matched_missing_mod_id": match_id,
                "matched_missing_name": match_name,
                "match_score": match_score,
                "note": note,
                "url": raw,
            }
        )

    for forbidden in sorted(FORBIDDEN_SLUGS):
        if not any(row["slug"] == forbidden for row in rows):
            rows.append(
                {
                    "decision": "skip_forbidden_by_user",
                    "destination": "skip",
                    "source": "user_note",
                    "kind": "mod",
                    "slug": forbidden,
                    "file_or_version": "",
                    "expected_mod_id": EXPECTED_IDS.get(forbidden, ""),
                    "matched_missing_mod_id": "",
                    "matched_missing_name": "",
                    "match_score": "",
                    "note": "user explicitly said not to install this",
                    "url": "",
                }
            )
    return rows


def looks_personal(path: Path) -> bool:
    low = path.name.lower()
    return any(pattern in low for pattern in PERSONAL_PATTERNS)


def custom_rows(missing_rows: list[dict]) -> list[dict]:
    rows = []
    for row in missing_rows:
        file_name = row["fabric_file"]
        low = file_name.lower()
        if row["mod_id"].startswith("unknown:") or any(pattern in low for pattern in PERSONAL_PATTERNS):
            source = COBBLE_EXTRA / "mods" / file_name
            rows.append(
                {
                    "mod_id": row["mod_id"],
                    "name": row["name"],
                    "source_file": safe_rel(source),
                    "exists": str(source.exists()),
                    "recommendation": "preserve as inactive reference; needs NeoForge port or verified replacement",
                    "reason": row["reason"],
                }
            )

    root_pack = COBBLE_EXTRA / "COBBLEVERSE - Pokemon Adventure [Cobblemon] COBBLEVERSE-1.7.30-CF.jar"
    if root_pack.exists():
        rows.append(
            {
                "mod_id": "unknown:cobbleverse_root_pack",
                "name": "COBBLEVERSE root pack",
                "source_file": safe_rel(root_pack),
                "exists": "True",
                "recommendation": "preserve as inactive reference; inspect before NeoForge use",
                "reason": "top-level Cobbleverse jar is not in normal mods inventory",
            }
        )
    return rows


def scan_archive_for_translation(path: Path) -> list[dict]:
    rows = []
    try:
        with zipfile.ZipFile(path) as zf:
            for name in zf.namelist():
                low = name.lower()
                suffix = Path(low).suffix
                hint = bool(HINT_RE.search(name))
                if "ru_ru" not in low and not hint and suffix not in {".json", ".lang", ".txt"}:
                    continue
                if suffix not in TEXT_SUFFIXES:
                    continue
                text = read_text_from_zip(zf, name)
                if not text:
                    continue
                has_cyrillic = bool(CYRILLIC_RE.search(text))
                if "ru_ru" in low or has_cyrillic or hint:
                    rows.append(
                        {
                            "container": safe_rel(path),
                            "entry": name,
                            "has_cyrillic": str(has_cyrillic),
                            "has_ru_ru_path": str("ru_ru" in low),
                            "hint_match": str(hint),
                            "sample": sample_text(text),
                        }
                    )
    except (zipfile.BadZipFile, OSError):
        pass
    return rows


def sample_text(text: str) -> str:
    compact = re.sub(r"\s+", " ", text)
    match = CYRILLIC_RE.search(compact)
    if match:
        start = max(0, match.start() - 80)
        return compact[start : start + 260]
    return compact[:260]


def scan_file_for_translation(path: Path) -> list[dict]:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return []
    try:
        if path.stat().st_size > 2_000_000:
            return []
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    low = str(path).lower()
    hint = bool(HINT_RE.search(low))
    has_cyrillic = bool(CYRILLIC_RE.search(text))
    if "ru_ru" not in low and not hint and not has_cyrillic:
        return []
    return [
        {
            "container": safe_rel(path),
            "entry": "",
            "has_cyrillic": str(has_cyrillic),
            "has_ru_ru_path": str("ru_ru" in low),
            "hint_match": str(hint),
            "sample": sample_text(text),
        }
    ]


def translation_rows() -> list[dict]:
    rows = []
    archive_bases = [
        COBBLE_EXTRA / "mods",
        COBBLE_EXTRA / "resourcepacks",
        COBBLE_EXTRA / "datapacks",
        COBBLE_EXTRA,
        FACTOR_MOON / "resourcepacks",
        FACTOR_MOON / "datapacks",
    ]
    seen = set()
    for base in archive_bases:
        if not base.exists():
            continue
        for path in sorted(base.glob("*")):
            if path.is_file() and path.suffix.lower() in {".jar", ".zip"} and path.resolve() not in seen:
                seen.add(path.resolve())
                rows.extend(scan_archive_for_translation(path))

    dir_bases = [
        COBBLE_EXTRA / "datapacks",
        COBBLE_EXTRA / "resourcepacks",
        COBBLE_EXTRA / "patchouli_books",
        COBBLE_EXTRA / "cobblenav",
        COBBLE_EXTRA / "build",
        FACTOR_MOON / "datapacks",
        FACTOR_MOON / "resourcepacks",
        FACTOR_MOON / "_cobblemon_extra_reference",
    ]
    seen_files = set()
    for base in dir_bases:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if path.is_file() and path.resolve() not in seen_files:
                seen_files.add(path.resolve())
                rows.extend(scan_file_for_translation(path))
    return rows


def all_candidate_archives() -> list[Path]:
    bases = [
        COBBLE_EXTRA / "mods",
        COBBLE_EXTRA / "resourcepacks",
        COBBLE_EXTRA / "datapacks",
        COBBLE_EXTRA,
        FACTOR_MOON / "mods",
        FACTOR_MOON / "resourcepacks",
        FACTOR_MOON / "datapacks",
    ]
    seen = set()
    paths = []
    for base in bases:
        if not base.exists():
            continue
        for path in sorted(base.glob("*")):
            if path.is_file() and path.suffix.lower() in {".jar", ".zip"}:
                resolved = path.resolve()
                if resolved not in seen:
                    seen.add(resolved)
                    paths.append(path)
    return paths


def focus_for_text(name: str, text: str) -> list[str]:
    low_name = name.lower()
    low_text = text.lower()
    focuses = []
    for focus, needles in FOCUSED_NEEDLES.items():
        for needle in needles:
            low_needle = needle.lower()
            if low_needle in low_name or low_needle in low_text:
                focuses.append(focus)
                break
    return focuses


def focused_translation_rows() -> list[dict]:
    rows = []
    for archive in all_candidate_archives():
        try:
            with zipfile.ZipFile(archive) as zf:
                for name in zf.namelist():
                    suffix = Path(name.lower()).suffix
                    if suffix not in TEXT_SUFFIXES:
                        continue
                    text = read_text_from_zip(zf, name, max_bytes=5_000_000)
                    if not text:
                        continue
                    focuses = focus_for_text(name, text)
                    if not focuses:
                        continue
                    rows.append(
                        {
                            "focus": ";".join(focuses),
                            "container": safe_rel(archive),
                            "entry": name,
                            "has_cyrillic": str(bool(CYRILLIC_RE.search(text))),
                            "has_ru_ru_path": str("ru_ru" in name.lower()),
                            "sample": sample_text(text),
                        }
                    )
        except (zipfile.BadZipFile, OSError):
            pass

    dir_bases = [
        COBBLE_EXTRA / "datapacks",
        COBBLE_EXTRA / "resourcepacks",
        COBBLE_EXTRA / "patchouli_books",
        COBBLE_EXTRA / "cobblenav",
        COBBLE_EXTRA / "build",
        FACTOR_MOON / "datapacks",
        FACTOR_MOON / "resourcepacks",
        FACTOR_MOON / "_cobblemon_extra_reference",
    ]
    seen = set()
    for base in dir_bases:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            try:
                if path.stat().st_size > 5_000_000:
                    continue
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            focuses = focus_for_text(str(path), text)
            if not focuses:
                continue
            rows.append(
                {
                    "focus": ";".join(focuses),
                    "container": safe_rel(path),
                    "entry": "",
                    "has_cyrillic": str(bool(CYRILLIC_RE.search(text))),
                    "has_ru_ru_path": str("ru_ru" in str(path).lower()),
                    "sample": sample_text(text),
                }
            )
    return rows


def main() -> int:
    factor_rows = inventory_jars(FACTOR_MOON / "mods")
    extra_rows = inventory_jars(COBBLE_EXTRA / "mods")
    missing_rows = parse_not_transferred()
    decisions = link_decisions(factor_rows, missing_rows)
    personal = custom_rows(missing_rows)
    translations = translation_rows()
    focused_translations = focused_translation_rows()

    write_csv(
        SCRIPT_DIR / "current_factor_moon_mod_inventory.csv",
        factor_rows,
        ["rel_path", "file_name", "size", "sha1", "metadata", "mod_ids", "display_names", "loaders"],
    )
    write_csv(
        SCRIPT_DIR / "cobblemon_extra_mod_inventory.csv",
        extra_rows,
        ["rel_path", "file_name", "size", "sha1", "metadata", "mod_ids", "display_names", "loaders"],
    )
    write_csv(
        SCRIPT_DIR / "user_link_install_decisions.csv",
        decisions,
        [
            "decision",
            "destination",
            "source",
            "kind",
            "slug",
            "file_or_version",
            "expected_mod_id",
            "matched_missing_mod_id",
            "matched_missing_name",
            "match_score",
            "note",
            "url",
        ],
    )
    write_csv(
        SCRIPT_DIR / "custom_or_personal_mods_to_preserve.csv",
        personal,
        ["mod_id", "name", "source_file", "exists", "recommendation", "reason"],
    )
    write_csv(
        SCRIPT_DIR / "translation_assets_report.csv",
        translations,
        ["container", "entry", "has_cyrillic", "has_ru_ru_path", "hint_match", "sample"],
    )
    write_csv(
        SCRIPT_DIR / "focused_cobblemon_translation_candidates.csv",
        focused_translations,
        ["focus", "container", "entry", "has_cyrillic", "has_ru_ru_path", "sample"],
    )

    summary = {
        "factor_moon_jars": len(factor_rows),
        "factor_moon_mod_ids": len(installed_ids(factor_rows)),
        "cobblemon_extra_jars": len(extra_rows),
        "user_links": len(decisions),
        "already_present_or_equivalent": sum(1 for row in decisions if row["decision"] == "already_present_or_equivalent"),
        "needs_download_and_metadata_check": sum(1 for row in decisions if row["decision"] == "needs_download_and_metadata_check"),
        "skip_forbidden_by_user": sum(1 for row in decisions if row["decision"] == "skip_forbidden_by_user"),
        "skip_modpack_file": sum(1 for row in decisions if row["decision"] == "skip_modpack_file"),
        "datapack_candidates": sum(1 for row in decisions if row["destination"] == "datapacks"),
        "personal_or_custom_candidates": len(personal),
        "translation_hits": len(translations),
        "focused_translation_hits": len(focused_translations),
    }
    (SCRIPT_DIR / "user_link_audit_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
