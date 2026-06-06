#!/usr/bin/env python3
"""Patch Cobblenav so item singletons are initialized before registry freeze.

Cobblenav 2.3.3 can first touch CobblenavItems from its ModelBakery mixin during
client model reload. At that point vanilla registries are frozen, and creating
the Pokenav Item throws "Registry is already frozen". This inserts:

    getstatic CobblenavItems.INSTANCE
    pop

at the start of CobblenavNeoForge.registerItems(), which runs during mod setup
before the item registry event and before registries are frozen.
"""

from __future__ import annotations

import shutil
import struct
import sys
import tempfile
import zipfile
from pathlib import Path


JAR_NAME = "cobblenav-neoforge-2.3.3.jar"
CLASS_PATH = "com/metacontent/cobblenav/neoforge/CobblenavNeoForge.class"
BACKUP_SUFFIX = ".pre-factormoon-earlyitems.bak"
TARGET_METHOD = "registerItems"
TARGET_DESCRIPTOR = "()V"
ITEMS_OWNER = "com/metacontent/cobblenav/CobblenavItems"
ITEMS_FIELD_NAME = "INSTANCE"
ITEMS_FIELD_DESC = "Lcom/metacontent/cobblenav/CobblenavItems;"
STACK_MAP_TABLE = "StackMapTable"


def u1(data: bytes | bytearray, offset: int) -> int:
    return data[offset]


def u2(data: bytes | bytearray, offset: int) -> int:
    return struct.unpack_from(">H", data, offset)[0]


def u4(data: bytes | bytearray, offset: int) -> int:
    return struct.unpack_from(">I", data, offset)[0]


def put_u2(data: bytearray, offset: int, value: int) -> None:
    struct.pack_into(">H", data, offset, value)


def put_u4(data: bytearray, offset: int, value: int) -> None:
    struct.pack_into(">I", data, offset, value)


def parse_constant_pool(data: bytes) -> tuple[int, dict[int, tuple], dict[int, str]]:
    if u4(data, 0) != 0xCAFEBABE:
        raise ValueError("Not a Java class file")

    cp_count = u2(data, 8)
    entries: dict[int, tuple] = {}
    utf8: dict[int, str] = {}
    offset = 10
    index = 1

    while index < cp_count:
        tag = u1(data, offset)
        offset += 1

        if tag == 1:  # Utf8
            length = u2(data, offset)
            offset += 2
            raw = data[offset : offset + length]
            # Java class files use modified UTF-8. The Cobblenav Kotlin metadata
            # contains the modified NUL encoding, while the symbols we patch are
            # plain ASCII; this normalization keeps both cases readable enough.
            value = raw.replace(b"\xc0\x80", b"\x00").decode("utf-8", errors="replace")
            entries[index] = (tag, value)
            utf8[index] = value
            offset += length
        elif tag in (3, 4):  # Integer, Float
            entries[index] = (tag,)
            offset += 4
        elif tag in (5, 6):  # Long, Double
            entries[index] = (tag,)
            offset += 8
            index += 1
        elif tag in (7, 8, 16, 19, 20):  # Class, String, MethodType, Module, Package
            entries[index] = (tag, u2(data, offset))
            offset += 2
        elif tag in (9, 10, 11, 12, 17, 18):  # refs, NameAndType, Dynamic, InvokeDynamic
            entries[index] = (tag, u2(data, offset), u2(data, offset + 2))
            offset += 4
        elif tag == 15:  # MethodHandle
            entries[index] = (tag, u1(data, offset), u2(data, offset + 1))
            offset += 3
        else:
            raise ValueError(f"Unsupported constant-pool tag {tag} at index {index}")

        index += 1

    return offset, entries, utf8


def cp_class_name(index: int, entries: dict[int, tuple], utf8: dict[int, str]) -> str:
    tag, name_index = entries[index]
    if tag != 7:
        raise ValueError(f"Constant pool entry {index} is not a class")
    return utf8[name_index]


def cp_name_and_type(index: int, entries: dict[int, tuple], utf8: dict[int, str]) -> tuple[str, str]:
    tag, name_index, descriptor_index = entries[index]
    if tag != 12:
        raise ValueError(f"Constant pool entry {index} is not a NameAndType")
    return utf8[name_index], utf8[descriptor_index]


def find_cobblenav_items_fieldref(entries: dict[int, tuple], utf8: dict[int, str]) -> int:
    for index, entry in entries.items():
        if entry[0] != 9:  # Fieldref
            continue
        _, class_index, name_and_type_index = entry
        owner = cp_class_name(class_index, entries, utf8)
        name, descriptor = cp_name_and_type(name_and_type_index, entries, utf8)
        if owner == ITEMS_OWNER and name == ITEMS_FIELD_NAME and descriptor == ITEMS_FIELD_DESC:
            return index

    raise ValueError("CobblenavItems.INSTANCE fieldref was not found in constant pool")


def skip_member(data: bytes, offset: int) -> int:
    offset += 6
    attributes_count = u2(data, offset)
    offset += 2
    for _ in range(attributes_count):
        attribute_length = u4(data, offset + 2)
        offset += 6 + attribute_length
    return offset


def code_subattributes(data: bytes, code_attr_content: int, code_length: int, utf8: dict[int, str]) -> list[str]:
    offset = code_attr_content + 8 + code_length
    exception_table_length = u2(data, offset)
    offset += 2 + exception_table_length * 8
    attributes_count = u2(data, offset)
    offset += 2

    names: list[str] = []
    for _ in range(attributes_count):
        name_index = u2(data, offset)
        attribute_length = u4(data, offset + 2)
        names.append(utf8[name_index])
        offset += 6 + attribute_length

    return names


def patch_class(data: bytes) -> tuple[bytes, bool]:
    offset, entries, utf8 = parse_constant_pool(data)
    items_fieldref = find_cobblenav_items_fieldref(entries, utf8)
    injection = b"\xb2" + struct.pack(">H", items_fieldref) + b"\x57"

    offset += 6  # access_flags, this_class, super_class
    interfaces_count = u2(data, offset)
    offset += 2 + interfaces_count * 2

    fields_count = u2(data, offset)
    offset += 2
    for _ in range(fields_count):
        offset = skip_member(data, offset)

    methods_count = u2(data, offset)
    offset += 2

    for _ in range(methods_count):
        method_name = utf8[u2(data, offset + 2)]
        method_descriptor = utf8[u2(data, offset + 4)]
        attributes_count = u2(data, offset + 6)
        offset += 8

        for _ in range(attributes_count):
            attr_start = offset
            attr_name = utf8[u2(data, attr_start)]
            attr_length = u4(data, attr_start + 2)
            attr_content = attr_start + 6

            if (
                method_name == TARGET_METHOD
                and method_descriptor == TARGET_DESCRIPTOR
                and attr_name == "Code"
            ):
                max_stack_offset = attr_content
                code_length_offset = attr_content + 4
                code_length = u4(data, code_length_offset)
                code_start = attr_content + 8

                if data[code_start : code_start + len(injection)] == injection:
                    return data, False

                subattributes = code_subattributes(data, attr_content, code_length, utf8)
                if STACK_MAP_TABLE in subattributes:
                    raise ValueError("Refusing to patch registerItems because it has a StackMapTable")

                patched = bytearray()
                patched += data[:code_start]
                patched += injection
                patched += data[code_start:]

                put_u2(patched, max_stack_offset, max(u2(data, max_stack_offset), 1))
                put_u4(patched, code_length_offset, code_length + len(injection))
                put_u4(patched, attr_start + 2, attr_length + len(injection))
                return bytes(patched), True

            offset += 6 + attr_length

    raise ValueError("registerItems()V Code attribute was not found")


def is_signature_file(name: str) -> bool:
    upper = name.upper()
    return upper.startswith("META-INF/") and upper.endswith((".SF", ".RSA", ".DSA", ".EC"))


def patch_jar(jar_path: Path) -> bool:
    if not jar_path.exists():
        raise FileNotFoundError(jar_path)

    backup_path = jar_path.with_name(jar_path.name + BACKUP_SUFFIX)
    if not backup_path.exists():
        shutil.copy2(jar_path, backup_path)

    with zipfile.ZipFile(jar_path, "r") as zin:
        class_bytes = zin.read(CLASS_PATH)
        patched_class, changed = patch_class(class_bytes)
        if not changed:
            print(f"{jar_path.name}: already patched")
            return False

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jar") as tmp:
            tmp_path = Path(tmp.name)

        try:
            with zipfile.ZipFile(tmp_path, "w") as zout:
                for info in zin.infolist():
                    if is_signature_file(info.filename):
                        continue
                    payload = patched_class if info.filename == CLASS_PATH else zin.read(info.filename)
                    zout.writestr(info, payload)
            shutil.move(str(tmp_path), jar_path)
        finally:
            if tmp_path.exists():
                tmp_path.unlink()

    print(f"{jar_path.name}: patched early CobblenavItems initialization")
    return True


def default_jar_path() -> Path:
    repo_root = Path(__file__).resolve().parents[3]
    return repo_root / "mods" / JAR_NAME


def main() -> int:
    jar_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_jar_path()
    patch_jar(jar_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
