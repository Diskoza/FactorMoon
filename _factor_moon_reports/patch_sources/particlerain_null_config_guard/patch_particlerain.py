from __future__ import annotations

import os
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODS_DIR = ROOT / "mods"
SOURCE = Path(__file__).resolve().parent / "src" / "main" / "java" / "pigcart" / "particlerain" / "patch" / "ConfigGuard.java"
TARGET_CLASS = "pigcart/particlerain/mixin/render/SpriteLoaderMixin.class"
HELPER_CLASS = "pigcart/particlerain/patch/ConfigGuard.class"
PATCH_MARKER = b"pigcart/particlerain/patch/ConfigGuard"


def find_jar() -> Path:
    matches = sorted(MODS_DIR.glob("particlerain-*-neoforge.jar"))
    if not matches:
        raise SystemExit("Particle Rain NeoForge jar was not found in mods/")
    if len(matches) > 1:
        raise SystemExit(f"Expected one Particle Rain jar, found: {matches}")
    return matches[0]


def u2(data: bytes | bytearray, offset: int) -> int:
    return struct.unpack_from(">H", data, offset)[0]


def utf8_entry(text: str) -> bytes:
    encoded = text.encode("utf-8")
    return b"\x01" + struct.pack(">H", len(encoded)) + encoded


def patch_constant_pool(class_bytes: bytes) -> bytes:
    data = bytearray(class_bytes)
    if data[0:4] != b"\xca\xfe\xba\xbe":
        raise ValueError("Not a Java class file")

    cp_count = u2(data, 8)
    entries: list[bytes | None] = [None]
    pos = 10
    index = 1
    while index < cp_count:
        start = pos
        tag = data[pos]
        pos += 1
        if tag == 1:
            length = u2(data, pos)
            pos += 2 + length
        elif tag in (3, 4):
            pos += 4
        elif tag in (5, 6):
            pos += 8
            entries.append(bytes(data[start:pos]))
            entries.append(None)
            index += 2
            continue
        elif tag in (7, 8, 16, 19, 20):
            pos += 2
        elif tag in (9, 10, 11, 12, 17, 18):
            pos += 4
        elif tag == 15:
            pos += 3
        else:
            raise ValueError(f"Unsupported constant-pool tag {tag} at index {index}")
        entries.append(bytes(data[start:pos]))
        index += 1

    if len(entries) != cp_count:
        raise ValueError("Constant-pool parse mismatch")

    # Reuse the existing ConfigManager.config field reference slot as a Methodref
    # to ConfigGuard.waterTint()Z. The bytecode keeps its length by nopping the
    # two old GETFIELD instructions after the call.
    entry49 = bytearray(entries[49])
    if entry49[0] not in (9, 10):
        raise ValueError("Unexpected constant-pool slot #49")
    entry49[0] = 10
    entries[49] = bytes(entry49)
    entries[52] = utf8_entry("pigcart/particlerain/patch/ConfigGuard")
    entries[53] = utf8_entry("waterTint")
    entries[54] = utf8_entry("()Z")

    rebuilt = bytearray(data[:10])
    for entry in entries[1:]:
        if entry is not None:
            rebuilt.extend(entry)
    rebuilt.extend(data[pos:])
    return bytes(rebuilt)


def patch_mixin_class(class_bytes: bytes) -> bytes:
    if PATCH_MARKER in class_bytes:
        return class_bytes

    patched = bytearray(patch_constant_pool(class_bytes))
    pattern = bytes.fromhex("b2 00 31 b4 00 37 b4 00 3d 99")
    replacement = bytes.fromhex("b8 00 31 00 00 00 00 00 00 99")
    count = patched.count(pattern)
    if count != 2:
        raise ValueError(f"Expected two Particle Rain waterTint bytecode sites, found {count}")
    return bytes(patched.replace(pattern, replacement))


def compile_helper(jar_path: Path, build_dir: Path) -> Path:
    classes_dir = build_dir / "classes"
    classes_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "javac",
            "-encoding",
            "UTF-8",
            "-cp",
            str(jar_path),
            "-d",
            str(classes_dir),
            str(SOURCE),
        ],
        check=True,
    )
    helper = classes_dir / HELPER_CLASS
    if not helper.exists():
        raise FileNotFoundError(helper)
    return helper


def write_patched_jar(jar_path: Path, helper_class: Path, build_dir: Path) -> None:
    tmp_jar = build_dir / jar_path.name
    with zipfile.ZipFile(jar_path, "r") as zin, zipfile.ZipFile(tmp_jar, "w", zipfile.ZIP_DEFLATED) as zout:
        names = set()
        for info in zin.infolist():
            content = zin.read(info.filename)
            if info.filename == TARGET_CLASS:
                content = patch_mixin_class(content)
            zout.writestr(info, content)
            names.add(info.filename)
        if HELPER_CLASS not in names:
            zout.write(helper_class, HELPER_CLASS)

    backup = jar_path.with_suffix(jar_path.suffix + ".pre-factormoon-nullconfig.bak")
    if not backup.exists():
        shutil.copy2(jar_path, backup)
    os.replace(tmp_jar, jar_path)


def main() -> None:
    jar_path = find_jar()
    with tempfile.TemporaryDirectory(prefix="particlerain_patch_") as temp:
        build_dir = Path(temp)
        helper = compile_helper(jar_path, build_dir)
        write_patched_jar(jar_path, helper, build_dir)
    print(f"Patched {jar_path.name}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode) from exc
