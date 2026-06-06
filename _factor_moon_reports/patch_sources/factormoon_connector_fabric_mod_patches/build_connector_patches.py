from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


PACK_ROOT = Path(__file__).resolve().parents[3]
PATCH_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PATCH_ROOT / "src" / "main" / "java"
MODS_DIR = PACK_ROOT / "mods"
COBBLEMON_EXTRA_MODS = PACK_ROOT.parent / "cobblemon-extra" / "mods"

FIGHT_SOURCE = COBBLEMON_EXTRA_MODS / "cobblemon-fight-them-all-1.0.4-cobblemon-1.7.3.jar"
BATTLE_SOURCE = COBBLEMON_EXTRA_MODS / "cobblemon-battle-positions-1.1.3.jar"

FIGHT_TARGET = MODS_DIR / "cobblemon-fight-them-all-1.0.4-cobblemon-1.7.3-factormoon-connector.jar"
BATTLE_TARGET = MODS_DIR / "cobblemon-battle-positions-1.1.3-factormoon-connector.jar"


def one_jar(pattern: str) -> Path:
    matches = sorted(MODS_DIR.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"No jar matched {pattern}")
    return matches[0]


def extract_nested_jar(container: Path, nested_name: str, target_dir: Path) -> Path:
    with zipfile.ZipFile(container) as jar:
        matches = [name for name in jar.namelist() if name.endswith(nested_name)]
        if not matches:
            raise FileNotFoundError(f"{nested_name} was not found inside {container.name}")
        out = target_dir / nested_name
        out.write_bytes(jar.read(matches[0]))
        return out


def compile_fight_wrappers(tmp: Path) -> Path:
    classes = tmp / "classes"
    classes.mkdir(parents=True, exist_ok=True)

    cca_base = extract_nested_jar(one_jar("trinkets-3.10.0.jar"), "cardinal-components-base-6.1.0.jar", tmp)
    cca_entity = extract_nested_jar(one_jar("trinkets-3.10.0.jar"), "cardinal-components-entity-6.1.0.jar", tmp)

    classpath = [
        FIGHT_SOURCE,
        one_jar("connector-*.jar"),
        one_jar("forgified-fabric-api-*.jar"),
        one_jar("Cobblemon-neoforge-*.jar"),
        one_jar("kotlinforforge-*.jar"),
        one_jar("yet_another_config_lib_v3-*.jar"),
        cca_base,
        cca_entity,
    ]
    java_files = [str(path) for path in SRC_ROOT.rglob("*.java")]
    argfile = tmp / "javac.args"
    argfile.write_text(
        "\n".join(
            [
                "--release",
                "21",
                "-encoding",
                "UTF-8",
                "-cp",
                ";".join(str(path) for path in classpath),
                "-d",
                str(classes),
                *java_files,
            ]
        ),
        encoding="utf-8",
    )
    subprocess.run(["javac", f"@{argfile}"], check=True)
    return classes


def copy_jar_with_metadata(source: Path, target: Path, metadata: dict, extra_classes: Path | None = None) -> None:
    if not source.exists():
        raise FileNotFoundError(source)

    target.parent.mkdir(parents=True, exist_ok=True)
    tmp_target = target.with_suffix(target.suffix + ".tmp")
    if tmp_target.exists():
        tmp_target.unlink()

    with zipfile.ZipFile(source) as src, zipfile.ZipFile(tmp_target, "w", zipfile.ZIP_DEFLATED) as dst:
        for info in src.infolist():
            if info.filename == "fabric.mod.json":
                continue
            dst.writestr(info, src.read(info.filename))
        dst.writestr("fabric.mod.json", json.dumps(metadata, ensure_ascii=False, indent=2).encode("utf-8"))

        if extra_classes is not None:
            for path in extra_classes.rglob("*.class"):
                dst.write(path, path.relative_to(extra_classes).as_posix())

    tmp_target.replace(target)


def patched_fight_metadata() -> dict:
    with zipfile.ZipFile(FIGHT_SOURCE) as jar:
        data = json.loads(jar.read("fabric.mod.json"))

    data["version"] = f'{data.get("version", "1.0.4+cobblemon-1.7.3")}+factormoon.1'
    data["entrypoints"] = {
        "main": ["ru.factormoon.connectorpatch.fightthemall.FightThemAllEntrypoint"],
        "client": ["ru.factormoon.connectorpatch.fightthemall.FightThemAllClientEntrypoint"],
        "cardinal-components": ["ru.factormoon.connectorpatch.fightthemall.FightThemAllCardinalEntrypoint"],
    }
    data["depends"] = {
        "fabricloader": "*",
        "minecraft": "~1.21.1",
        "java": ">=21",
        "fabric-api": "*",
        "yet_another_config_lib_v3": ">=3.6.1",
        "cardinal-components-base": ">=6.1.0",
        "cardinal-components-entity": ">=6.1.0",
        "cobblemon": ">=1.7.0",
    }
    return data


def patched_battle_metadata() -> dict:
    with zipfile.ZipFile(BATTLE_SOURCE) as jar:
        data = json.loads(jar.read("fabric.mod.json"))

    data["version"] = f'{data.get("version", "1.1.3")}+factormoon.1'
    data.setdefault("depends", {})
    data["depends"]["fabricloader"] = "*"
    return data


def main() -> int:
    if not FIGHT_SOURCE.exists():
        print(f"Missing source jar: {FIGHT_SOURCE}", file=sys.stderr)
        return 1
    if not BATTLE_SOURCE.exists():
        print(f"Missing source jar: {BATTLE_SOURCE}", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix="factormoon_connector_patches_") as tmp_name:
        tmp = Path(tmp_name)
        fight_classes = compile_fight_wrappers(tmp)
        copy_jar_with_metadata(FIGHT_SOURCE, FIGHT_TARGET, patched_fight_metadata(), fight_classes)
        copy_jar_with_metadata(BATTLE_SOURCE, BATTLE_TARGET, patched_battle_metadata())

    print(f"Wrote {FIGHT_TARGET}")
    print(f"Wrote {BATTLE_TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
