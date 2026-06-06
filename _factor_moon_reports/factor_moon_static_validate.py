from __future__ import annotations

import csv
import io
import json
import re
import tomllib
import zipfile
from collections import defaultdict
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
FACTOR_MOON = SCRIPT_DIR.parent
INSTANCES = FACTOR_MOON.parent
MODS_DIR = FACTOR_MOON / "mods"

SKIP_DEP_IDS = {
    "minecraft",
    "neoforge",
    "forge",
    "java",
    "fabricloader",
    "fabric",
}

PLATFORM_VERSIONS = {
    "minecraft": "1.21.1",
    "neoforge": "21.1.228",
    "java": "21",
}

KNOWN_PROVIDED_IDS = {
    "commonnetworking",
    "common-networking-neoforge",
    "fabric_api",
    "fabric-api",
}

ID_ALIASES = {
    "commonnetworking": {"common-networking-neoforge", "common_networking"},
    "common-networking-neoforge": {"commonnetworking", "common_networking"},
    "cloth-config": {"cloth_config", "cloth-config2"},
    "cloth_config": {"cloth-config", "cloth-config2"},
    "roughlyenoughitems": {"rei"},
    "resourcepackoverrides": {"resource_pack_overrides"},
    "kotlinforforge": {"kotlin_for_forge"},
    "yumi-commons-core": {"yumi_commons_core"},
    "yumi-commons-collections": {"yumi_commons_collections"},
    "yumi-commons-event": {"yumi_commons_event"},
}

WEAPON_RE = re.compile(
    r"(?:^|[-_. ])(tacz|gun|guns|rifle|pistol|shotgun|firearm|ammo|cannon|cannons|bigcannons|artillery|projectilelib)(?:$|[-_. ])",
    re.IGNORECASE,
)


def safe_rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(INSTANCES.resolve()))
    except ValueError:
        return str(path)


def read_text(zf: zipfile.ZipFile, name: str, max_bytes: int = 2_000_000) -> str:
    info = zf.getinfo(name)
    if info.file_size > max_bytes:
        return ""
    data = zf.read(name)
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return ""


def parse_fabric(text: str) -> tuple[list[str], list[dict], dict[str, str]]:
    try:
        data = json.loads(text)
    except Exception:
        return [], [], {}
    mod_id = data.get("id")
    ids = [str(mod_id)] if mod_id else []
    versions = {}
    if mod_id and data.get("version"):
        versions[str(mod_id)] = str(data["version"])
    provides = data.get("provides", [])
    if isinstance(provides, list):
        ids.extend(str(provided) for provided in provides if provided)
        for provided in provides:
            if provided and data.get("version"):
                versions[str(provided)] = str(data["version"])
    deps = []
    for key in ("depends", "requires"):
        value = data.get(key, {})
        if isinstance(value, dict):
            for dep_id, dep_version in value.items():
                deps.append(
                    {
                        "mod_id": dep_id,
                        "required": True,
                        "version_range": "" if dep_version is None else str(dep_version),
                        "source": "fabric.mod.json",
                    }
                )
    return ids, deps, versions


def parse_toml(text: str, source: str) -> tuple[list[str], list[dict], dict[str, str]]:
    try:
        data = tomllib.loads(text)
    except Exception:
        data = {}
    ids = []
    deps = []
    versions = {}
    mods = data.get("mods", [])
    if isinstance(mods, dict):
        mods = [mods]
    for mod in mods:
        if isinstance(mod, dict) and mod.get("modId"):
            mod_id = str(mod["modId"])
            ids.append(mod_id)
            if mod.get("version"):
                versions[mod_id] = str(mod["version"])

    dep_table = data.get("dependencies", {})
    if isinstance(dep_table, dict):
        for owner, entries in dep_table.items():
            if isinstance(entries, dict):
                entries = [entries]
            if not isinstance(entries, list):
                continue
            for dep in entries:
                if not isinstance(dep, dict):
                    continue
                dep_id = dep.get("modId")
                if not dep_id:
                    continue
                dep_type = str(dep.get("type", "")).lower()
                mandatory = dep.get("mandatory")
                required = dep_type in {"required", ""} if mandatory is None else bool(mandatory)
                deps.append(
                    {
                        "owner": owner,
                        "mod_id": str(dep_id),
                        "required": required,
                        "type": dep_type,
                        "version_range": str(dep.get("versionRange", "")),
                        "source": source,
                    }
                )

    if ids:
        return ids, deps, versions

    # Fallback for slightly non-standard TOML.
    blocks = re.split(r"(?m)^\s*\[\[", text)
    for block in blocks:
        header, _, rest = block.partition("]]")
        if header.strip() != "mods":
            continue
        match = re.search(r"(?im)^\s*modId\s*=\s*['\"]([^'\"]+)['\"]", rest)
        if match:
            ids.append(match.group(1))
    return ids, deps, versions


def parse_zip(zf: zipfile.ZipFile, prefix: str = "") -> dict:
    names = set(zf.namelist())
    ids = []
    deps = []
    versions = {}
    metadata = []
    has_neoforge = False
    has_fabric = False
    for toml_name in ("META-INF/neoforge.mods.toml", "META-INF/mods.toml"):
        if toml_name in names:
            has_neoforge = True
            metadata.append(prefix + toml_name)
            mod_ids, mod_deps, mod_versions = parse_toml(read_text(zf, toml_name), toml_name)
            ids.extend(mod_ids)
            deps.extend(mod_deps)
            versions.update(mod_versions)
    if "fabric.mod.json" in names:
        has_fabric = True
        metadata.append(prefix + "fabric.mod.json")
        mod_ids, mod_deps, mod_versions = parse_fabric(read_text(zf, "fabric.mod.json"))
        ids.extend(mod_ids)
        versions.update(mod_versions)
        if not has_neoforge:
            deps.extend(mod_deps)

    nested_ids = []
    nested_versions = {}
    for name in names:
        if not name.endswith(".jar") or not (
            name.startswith("META-INF/jarjar/")
            or name.startswith("META-INF/jars/")
            or "/jarjar/" in name
            or "/jars/" in name
        ):
            continue
        try:
            data = zf.read(name)
            with zipfile.ZipFile(io.BytesIO(data)) as nested:
                nested_data = parse_zip(nested, prefix=f"{name}:")
                nested_ids.extend(nested_data["ids"])
                nested_versions.update(nested_data["versions"])
                nested_versions.update(nested_data["nested_versions"])
                deps.extend(nested_data["deps"])
                metadata.extend(nested_data["metadata"])
        except Exception:
            continue

    return {
        "ids": list(dict.fromkeys(ids)),
        "nested_ids": list(dict.fromkeys(nested_ids)),
        "versions": versions,
        "nested_versions": nested_versions,
        "deps": deps,
        "metadata": metadata,
        "has_neoforge": has_neoforge,
        "has_fabric": has_fabric,
    }


def parse_jar(path: Path) -> dict:
    try:
        with zipfile.ZipFile(path) as zf:
            data = parse_zip(zf)
    except zipfile.BadZipFile:
        data = {
            "ids": [],
            "nested_ids": [],
            "versions": {},
            "nested_versions": {},
            "deps": [],
            "metadata": ["bad_zip"],
            "has_neoforge": False,
            "has_fabric": False,
        }
    data["path"] = path
    data["file_name"] = path.name
    return data


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def has_id(mod_id: str, provided: set[str]) -> bool:
    if mod_id in provided:
        return True
    normalized = {mod_id.replace("-", "_"), mod_id.replace("_", "-")}
    if any(candidate in provided for candidate in normalized):
        return True
    for alias in ID_ALIASES.get(mod_id, set()):
        if alias in provided:
            return True
    return False


def split_version(value: str) -> list[object]:
    pieces: list[object] = []
    for part in re.split(r"[.\-+_]", value.strip()):
        if not part:
            continue
        if part.isdigit():
            pieces.append(int(part))
            continue
        match = re.match(r"(\d+)([A-Za-z].*)", part)
        if match:
            pieces.append(int(match.group(1)))
            pieces.append(match.group(2).lower())
        else:
            pieces.append(part.lower())
    return pieces


def compare_versions(actual: str, expected: str) -> int:
    left = split_version(actual)
    right = split_version(expected)
    size = max(len(left), len(right))
    for index in range(size):
        a = left[index] if index < len(left) else 0
        b = right[index] if index < len(right) else 0
        if a == b:
            continue
        if isinstance(a, int) and isinstance(b, int):
            return -1 if a < b else 1
        return -1 if str(a) < str(b) else 1
    return 0


def version_satisfies(actual: str, version_range: str) -> bool:
    spec = version_range.strip().strip('"').strip("'")
    if not spec or spec == "*":
        return True
    if spec.endswith(".x"):
        return actual.startswith(spec[:-1])
    if spec.startswith(">="):
        return compare_versions(actual, spec[2:].strip()) >= 0
    if spec.startswith(">"):
        return compare_versions(actual, spec[1:].strip()) > 0
    if spec.startswith("<="):
        return compare_versions(actual, spec[2:].strip()) <= 0
    if spec.startswith("<"):
        return compare_versions(actual, spec[1:].strip()) < 0
    if spec.startswith("^"):
        base = spec[1:].strip()
        if compare_versions(actual, base) < 0:
            return False
        actual_parts = split_version(actual)
        base_parts = split_version(base)
        return bool(actual_parts and base_parts and actual_parts[0] == base_parts[0])
    if spec.startswith("~"):
        base = spec[1:].strip().rstrip("-")
        if compare_versions(actual, base) < 0:
            return False
        actual_parts = split_version(actual)
        base_parts = split_version(base)
        return len(actual_parts) >= 2 and len(base_parts) >= 2 and actual_parts[:2] == base_parts[:2]

    match = re.fullmatch(r"([\[(])\s*([^,\])]*?)\s*(?:,\s*([^)\]]*?)\s*)?([\])])", spec)
    if match:
        lower_bracket, lower, upper, upper_bracket = match.groups()
        if upper is None:
            return compare_versions(actual, lower) == 0
        if lower:
            cmp_lower = compare_versions(actual, lower)
            if cmp_lower < 0 or (cmp_lower == 0 and lower_bracket == "("):
                return False
        if upper:
            cmp_upper = compare_versions(actual, upper)
            if cmp_upper > 0 or (cmp_upper == 0 and upper_bracket == ")"):
                return False
        return True

    return actual == spec


def installed_version_for(mod_id: str, provided_versions: dict[str, str]) -> str:
    if mod_id in PLATFORM_VERSIONS:
        return PLATFORM_VERSIONS[mod_id]
    if mod_id in provided_versions:
        return provided_versions[mod_id]
    for alias in ID_ALIASES.get(mod_id, set()):
        if alias in provided_versions:
            return provided_versions[alias]
    return ""


def main() -> int:
    jars = sorted(MODS_DIR.glob("*.jar"), key=lambda p: p.name.lower())
    parsed = [parse_jar(path) for path in jars]
    connector_present = any(
        record["file_name"].lower().startswith("connector-")
        or "connectorextras" in record["ids"]
        or "forgified_fabric_api" in record["ids"]
        for record in parsed
    )
    provided = set(KNOWN_PROVIDED_IDS)
    provided_versions = dict(PLATFORM_VERSIONS)
    primary_by_file = {}
    for record in parsed:
        ids = record["ids"]
        if ids:
            primary_by_file[record["file_name"]] = ids[0]
        provided.update(ids)
        provided.update(record["nested_ids"])
        provided.update(record["versions"])
        provided.update(record["nested_versions"])
        provided_versions.update(record["versions"])
        provided_versions.update(record["nested_versions"])

    duplicate_rows = []
    by_id = defaultdict(list)
    for file_name, mod_id in primary_by_file.items():
        by_id[mod_id].append(file_name)
    for mod_id, files in sorted(by_id.items()):
        if len(files) > 1:
            duplicate_rows.append({"mod_id": mod_id, "files": ";".join(files)})

    loader_rows = []
    connector_fabric_rows = []
    for record in parsed:
        if record["has_fabric"] and not record["has_neoforge"]:
            if connector_present:
                connector_fabric_rows.append(
                    {
                        "file": record["file_name"],
                        "issue": "fabric_only_loaded_through_connector",
                        "metadata": ";".join(record["metadata"]),
                    }
                )
                continue
            loader_rows.append(
                {
                    "file": record["file_name"],
                    "issue": "fabric_only_active_jar",
                    "metadata": ";".join(record["metadata"]),
                }
            )

    missing_rows = []
    unsupported_version_rows = []
    for record in parsed:
        owner_ids = record["ids"]
        for dep in record["deps"]:
            dep_id = dep["mod_id"]
            if dep_id in owner_ids:
                continue
            if not dep.get("required"):
                actual_version = installed_version_for(dep_id, provided_versions)
                if actual_version and dep.get("version_range") and not version_satisfies(actual_version, dep["version_range"]):
                    unsupported_version_rows.append(
                        {
                            "file": record["file_name"],
                            "owner_mod_ids": ";".join(owner_ids),
                            "dependency_mod_id": dep_id,
                            "required": "false",
                            "expected_range": dep.get("version_range", ""),
                            "actual_version": actual_version,
                            "source": dep.get("source", ""),
                        }
                    )
                continue
            actual_version = installed_version_for(dep_id, provided_versions)
            if actual_version and dep.get("version_range") and not version_satisfies(actual_version, dep["version_range"]):
                unsupported_version_rows.append(
                    {
                        "file": record["file_name"],
                        "owner_mod_ids": ";".join(owner_ids),
                        "dependency_mod_id": dep_id,
                        "required": "true",
                        "expected_range": dep.get("version_range", ""),
                        "actual_version": actual_version,
                        "source": dep.get("source", ""),
                    }
                )
                continue
            if dep_id in SKIP_DEP_IDS or has_id(dep_id, provided):
                continue
            missing_rows.append(
                {
                    "file": record["file_name"],
                    "owner_mod_ids": ";".join(owner_ids),
                    "missing_mod_id": dep_id,
                    "dependency_type": dep.get("type", ""),
                    "source": dep.get("source", ""),
                }
            )

    weapon_rows = []
    for record in parsed:
        haystack = " ".join([record["file_name"], *record["ids"]])
        if WEAPON_RE.search(haystack):
            weapon_rows.append({"file": record["file_name"], "mod_ids": ";".join(record["ids"])})

    write_csv(SCRIPT_DIR / "validation_duplicate_mod_ids.csv", duplicate_rows, ["mod_id", "files"])
    write_csv(SCRIPT_DIR / "validation_loader_issues.csv", loader_rows, ["file", "issue", "metadata"])
    write_csv(SCRIPT_DIR / "validation_connector_fabric_jars.csv", connector_fabric_rows, ["file", "issue", "metadata"])
    write_csv(
        SCRIPT_DIR / "validation_missing_dependencies.csv",
        missing_rows,
        ["file", "owner_mod_ids", "missing_mod_id", "dependency_type", "source"],
    )
    write_csv(
        SCRIPT_DIR / "validation_unsupported_dependency_versions.csv",
        unsupported_version_rows,
        ["file", "owner_mod_ids", "dependency_mod_id", "required", "expected_range", "actual_version", "source"],
    )
    write_csv(SCRIPT_DIR / "validation_weapon_suspects.csv", weapon_rows, ["file", "mod_ids"])

    summary = {
        "installed_jar_files": len(jars),
        "unique_primary_mod_ids": len(set(primary_by_file.values())),
        "duplicate_primary_mod_ids": len(duplicate_rows),
        "fabric_only_active_jars": len(loader_rows),
        "fabric_jars_expected_through_connector": len(connector_fabric_rows),
        "weapon_or_artillery_suspects": len(weapon_rows),
        "missing_required_dependencies": len(missing_rows),
        "unsupported_dependency_versions": len(unsupported_version_rows),
    }
    (SCRIPT_DIR / "validation_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
