from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


PORT_DIR = Path(__file__).resolve().parent
REPORTS_DIR = PORT_DIR.parents[1]
FACTOR_MOON = REPORTS_DIR.parent
INSTANCES = FACTOR_MOON.parent
SOURCE_DATA = FACTOR_MOON / "_cobblemon_extra_reference" / "custom_sources" / "cobblemon-extra-ride-compat"
BUILD_DIR = PORT_DIR / "build"
CLASSES_DIR = BUILD_DIR / "classes"
JAR_DIR = BUILD_DIR / "libs"
OUT_JAR = JAR_DIR / "cobblemon-extra-ride-compat-neoforge-0.1.1.jar"


def jars_under(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [str(jar) for jar in sorted(path.rglob("*.jar"))]


def reset_build() -> None:
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    CLASSES_DIR.mkdir(parents=True, exist_ok=True)
    JAR_DIR.mkdir(parents=True, exist_ok=True)


def copy_resources() -> None:
    resources = PORT_DIR / "src" / "main" / "resources"
    shutil.copytree(resources, CLASSES_DIR, dirs_exist_ok=True)
    data_dir = SOURCE_DATA / "data"
    if data_dir.exists():
        shutil.copytree(data_dir, CLASSES_DIR / "data", dirs_exist_ok=True)


def compile_sources() -> None:
    sources = [str(path) for path in sorted((PORT_DIR / "src" / "main" / "java").rglob("*.java"))]
    classpath = [
        str(FACTOR_MOON / "libraries" / "net" / "minecraft" / "client" / "1.21.1-20240808.144430" / "client-1.21.1-20240808.144430-srg.jar"),
        str(FACTOR_MOON / "libraries" / "net" / "neoforged" / "neoforge" / "21.1.228" / "neoforge-21.1.228-client.jar"),
        str(FACTOR_MOON / "libraries" / "net" / "neoforged" / "neoforge" / "21.1.228" / "neoforge-21.1.228-universal.jar"),
        str(FACTOR_MOON / "libraries" / "org" / "spongepowered" / "mixin" / "0.8.7" / "mixin-0.8.7.jar"),
        str(FACTOR_MOON / "mods" / "Cobblemon-neoforge-1.7.3+1.21.1.jar"),
        str(FACTOR_MOON / "mods" / "kotlinforforge-5.11.0-all.jar"),
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

    args_path.write_text("\n".join(quote(arg) if any(ch.isspace() for ch in arg) or ";" in arg else arg for arg in args), encoding="utf-8")
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
