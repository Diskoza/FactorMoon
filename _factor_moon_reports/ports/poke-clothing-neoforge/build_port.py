from __future__ import annotations

import json
import shutil
import subprocess
import zipfile
from pathlib import Path


PORT_DIR = Path(__file__).resolve().parent
REPORTS_DIR = PORT_DIR.parents[1]
FACTOR_MOON = REPORTS_DIR.parent
INSTANCES = FACTOR_MOON.parent
SOURCE_JAR = INSTANCES / "cobblemon-extra" / "mods" / "poke-clothing-1.1.2.jar"
BUILD_DIR = PORT_DIR / "build"
CLASSES_DIR = BUILD_DIR / "classes"
JAR_DIR = BUILD_DIR / "libs"
OUT_JAR = JAR_DIR / "poke-clothing-neoforge-1.1.2-port.1.jar"


def jars_under(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [str(jar) for jar in sorted(path.rglob("*.jar"))]


def reset_build() -> None:
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    CLASSES_DIR.mkdir(parents=True, exist_ok=True)
    JAR_DIR.mkdir(parents=True, exist_ok=True)


def should_copy_resource(name: str, data: bytes) -> bool:
    if not (name.startswith("assets/") or name.startswith("data/")):
        return False
    if name.startswith("data/poke-clothing/recipe/") and name.endswith(".json"):
        try:
            parsed = json.loads(data.decode("utf-8"))
        except Exception:
            return False
        if parsed.get("type") == "poke-clothing:tailoring":
            return False
    if name.startswith("data/poke-clothing/advancement/recipes/tailoring/"):
        return False
    return True


def copy_resources() -> None:
    resources = PORT_DIR / "src" / "main" / "resources"
    shutil.copytree(resources, CLASSES_DIR, dirs_exist_ok=True)
    with zipfile.ZipFile(SOURCE_JAR) as source:
        for info in source.infolist():
            if info.is_dir():
                continue
            data = source.read(info)
            if not should_copy_resource(info.filename, data):
                continue
            target = CLASSES_DIR / info.filename
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)


def compile_sources() -> None:
    sources = [str(path) for path in sorted((PORT_DIR / "src" / "main" / "java").rglob("*.java"))]
    classpath = [
        str(FACTOR_MOON / "libraries" / "net" / "minecraft" / "client" / "1.21.1-20240808.144430" / "client-1.21.1-20240808.144430-srg.jar"),
        str(FACTOR_MOON / "libraries" / "net" / "neoforged" / "neoforge" / "21.1.228" / "neoforge-21.1.228-client.jar"),
        str(FACTOR_MOON / "libraries" / "net" / "neoforged" / "neoforge" / "21.1.228" / "neoforge-21.1.228-universal.jar"),
    ]
    classpath += [
        jar
        for jar in jars_under(FACTOR_MOON / "libraries")
        if "\\net\\minecraft\\client\\" not in jar
        and "\\net\\minecraftforge\\forge\\" not in jar
        and "\\net\\neoforged\\neoforge\\" not in jar
    ]
    args_path = BUILD_DIR / "javac.args"
    args = [
        "--release",
        "21",
        "-encoding",
        "UTF-8",
        "-classpath",
        ";".join(classpath),
        "-d",
        str(CLASSES_DIR),
        *sources,
    ]

    def quote(arg: str) -> str:
        return '"' + arg.replace("\\", "\\\\").replace('"', '\\"') + '"'

    args_path.write_text(
        "\n".join(quote(arg) if any(ch.isspace() for ch in arg) or ";" in arg else arg for arg in args),
        encoding="utf-8",
    )
    subprocess.run(["javac", f"@{args_path}"], cwd=PORT_DIR, check=True)


def build_jar() -> None:
    subprocess.run(["jar", "--create", "--file", str(OUT_JAR), "-C", str(CLASSES_DIR), "."], check=True)


def main() -> int:
    reset_build()
    copy_resources()
    compile_sources()
    build_jar()
    print(OUT_JAR)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
