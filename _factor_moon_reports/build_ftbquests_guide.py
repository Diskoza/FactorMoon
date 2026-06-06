from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTS = ROOT / "config" / "ftbquests" / "quests"
CHAPTERS = QUESTS / "chapters"
LANG = QUESTS / "lang" / "en_us.snbt"
REPORTS = ROOT / "_factor_moon_reports"
OUT_MD = ROOT / "QUESTS_FILE_GUIDE.md"
OUT_CSV = REPORTS / "ftbquests_active_structure.csv"


def active_mod_ids() -> set[str]:
    ids = {"minecraft", "forge", "neoforge", "ftbquests", "atm"}
    inventory = REPORTS / "current_factor_moon_mod_inventory.csv"
    if inventory.exists():
        with inventory.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                for mod_id in row.get("mod_ids", "").split(";"):
                    if mod_id:
                        ids.add(mod_id)
    return ids


def lang_titles() -> tuple[dict[str, str], dict[str, str]]:
    chapters: dict[str, str] = {}
    groups: dict[str, str] = {}
    if not LANG.exists():
        return chapters, groups
    text = LANG.read_text(encoding="utf-8", errors="ignore")
    for match in re.finditer(r'chapter\.([0-9A-F]{16})\.title:\s*"((?:[^"\\]|\\.)*)"', text):
        chapters[match.group(1)] = match.group(2)
    for match in re.finditer(r'chapter_group\.([0-9A-F]{16})\.title:\s*"((?:[^"\\]|\\.)*)"', text):
        groups[match.group(1)] = match.group(2)
    return chapters, groups


def first(pattern: str, text: str, default: str = "") -> str:
    match = re.search(pattern, text)
    return match.group(1) if match else default


def chapter_rows() -> list[dict[str, str | int]]:
    ids = active_mod_ids()
    chapter_titles, group_titles = lang_titles()
    rows: list[dict[str, str | int]] = []

    for path in sorted(CHAPTERS.glob("*.snbt")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        chapter_id = first(r'\bid:\s*"([0-9A-F]{16})"', text)
        group_id = first(r'\bgroup:\s*"([0-9A-F]*)"', text)
        namespaces = sorted(set(re.findall(r'"([a-z0-9_.-]+):[a-z0-9_./-]+"', text)))
        missing = [namespace for namespace in namespaces if namespace not in ids]
        task_types = Counter(re.findall(r'\btype:\s*"([^"]+)"', text))
        custom_task_types = sorted(task for task in task_types if ":" in task and not task.startswith("minecraft:"))
        quests = len(re.findall(r'\n\t\t\{\n\t\t\t(?:[^{}]|\{[^{}]*\})*?\bid:\s*"[0-9A-F]{16}"', text))
        rows.append(
            {
                "file": path.name,
                "chapter_id": chapter_id,
                "title": chapter_titles.get(chapter_id, path.stem),
                "group_id": group_id,
                "group": group_titles.get(group_id, "Ungrouped" if not group_id else group_id),
                "quest_count": text.count("\n\t\t{"),
                "task_count": text.count('type: "item"')
                + text.count('type: "checkmark"')
                + text.count('type: "dimension"')
                + sum(text.count(f'type: "{task}"') for task in custom_task_types),
                "reward_count": text.count("\n\t\t\t\trewards:") + text.count("\n\t\t\trewards:"),
                "namespaces": ", ".join(namespaces),
                "missing_namespaces": ", ".join(missing),
                "custom_task_types": ", ".join(custom_task_types),
            }
        )
    return rows


def disabled_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for manifest in sorted((REPORTS / "disabled_quests").glob("**/*manifest.csv")):
        with manifest.open(newline="", encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                row = dict(row)
                row["manifest"] = str(manifest.relative_to(ROOT)).replace("\\", "/")
                rows.append(row)
    return rows


def write_csv(rows: list[dict[str, str | int]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "group",
        "file",
        "title",
        "chapter_id",
        "quest_count",
        "task_count",
        "reward_count",
        "missing_namespaces",
        "custom_task_types",
        "namespaces",
    ]
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def md_table(headers: list[str], rows: list[list[str]], limit: int | None = None) -> str:
    shown = rows if limit is None else rows[:limit]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in shown:
        safe = [cell.replace("|", "\\|").replace("\n", " ") for cell in row]
        lines.append("| " + " | ".join(safe) + " |")
    if limit is not None and len(rows) > limit:
        lines.append(f"| ... | ... | ... | ... | ... |")
    return "\n".join(lines)


def build_markdown(rows: list[dict[str, str | int]], disabled: list[dict[str, str]]) -> str:
    grouped: dict[str, list[dict[str, str | int]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["group"])].append(row)

    active_table_rows = [
        [
            str(row["group"]),
            str(row["file"]),
            str(row["title"]),
            str(row["quest_count"]),
            str(row["missing_namespaces"] or "-"),
            str(row["custom_task_types"] or "-"),
        ]
        for row in rows
    ]

    disabled_table_rows = [
        [
            row.get("file", ""),
            row.get("action", ""),
            row.get("reason", ""),
            row.get("manifest", ""),
        ]
        for row in disabled
    ]

    missing_rows = [
        [str(row["file"]), str(row["missing_namespaces"]), str(row["custom_task_types"] or "-")]
        for row in rows
        if row.get("missing_namespaces") or row.get("custom_task_types")
    ]

    return f"""# FactorMoon: работа с FTB Quests через файлы

Сгенерировано: 2026-06-06

Этот файл можно передавать другим людям как карту квестов FactorMoon и короткую инструкцию по редактированию книги через файлы игры, а не через GUI FTB Quests.

## Где Что Лежит

- `config/ftbquests/quests/data.snbt` — глобальные настройки книги. Сейчас иконка книги заменена на `cobblemon:poke_ball`.
- `config/ftbquests/quests/chapter_groups.snbt` — порядок видимых групп глав.
- `config/ftbquests/quests/chapters/*.snbt` — активные главы. Один файл равен одной главе. Если вынести файл из этой папки, глава пропадет из книги.
- `config/ftbquests/quests/lang/*.snbt` — видимые названия, подзаголовки и описания. Большинство кастомных Cobblemon-глав пока живут по имени файла, если для них не добавлен отдельный lang-ключ.
- `config/ftbquests/quests/reward_tables/*.snbt` — таблицы лута для наград `type: "loot"`.
- `_factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/chapters` — архив отключенных ATM10/устаревших глав. Они не удалены, их можно вернуть.
- `_factor_moon_reports/ftbquests_active_structure.csv` — та же структура активных глав в CSV-формате.

## Активные Главы

{md_table(["Группа", "Файл", "Название", "Квестов", "Отсутствующие namespace", "Кастомные типы задач"], active_table_rows)}

## Отключенные Главы

Эти файлы не удалены. Они вынесены из активной папки, чтобы книга не показывала квесты от удаленных модов, но сами главы можно вернуть или использовать как черновики.

{md_table(["Файл", "Действие", "Причина", "Манифест"], disabled_table_rows)}

## Что Еще Нужно Почистить

{md_table(["Активный файл", "Отсутствующие namespace", "Кастомные типы задач"], missing_rows)}

Важные заметки:

- `cobblemon_tasks:cobblemon_task` используется в кастомной Cobblemon-линейке, но сейчас активные jar не дают mod id `cobblemon_tasks` и очевидных ресурсов под этот тип задач. Нужно либо портировать этот task provider, либо заменить такие задачи на стандартные типы FTB Quests.
- `03_trainers_nest.snbt` уже переведен с Tom's Storage на Sophisticated Storage: `sophisticatedstorage:controller` и `sophisticatedstorage:storage_link`.
- `06_bond_and_breed.snbt` больше не требует `cobblecuisine:coffee`; временно используется `minecraft:honey_bottle`, пока CobbleCuisine не перенесен.
- Отключенные generic-главы ATM10 лучше не возвращать как есть. Их стоит пересобрать заново как FactorMoon-гайды.

## Как Редактировать

1. Найти нужную главу или предмет:
   ```powershell
   rg -n "chapter title or item id" config\\ftbquests\\quests\\chapters
   ```

2. Заменить предмет в задании или награде:
   ```snbt
   item: {{ count: 1, id: "modid:item_name" }}
   type: "item"
   ```

3. Отключить главу: перенести ее `.snbt` файл из `config/ftbquests/quests/chapters` в архивную папку.

4. Вернуть главу: перенести файл обратно в `config/ftbquests/quests/chapters`. Если у главы есть `group`, проверь, что этот id есть в `chapter_groups.snbt`.

5. Добавить или переименовать видимый текст в `config/ftbquests/quests/lang/en_us.snbt`, а затем при желании продублировать в `ru_ru.snbt`:
   ```snbt
   chapter.CHAPTER_ID.title: "Chapter Name"
   quest.QUEST_ID.title: "Quest Name"
   quest.QUEST_ID.quest_desc: ["Description text"]
   task.TASK_ID.title: "Task Name"
   ```

6. Сгенерировать новый 16-символьный hex id для новой главы/квеста/задачи/награды:
   ```powershell
   [guid]::NewGuid().ToString("N").Substring(0,16).ToUpper()
   ```

7. После правок пересобрать эту карту и проверить missing namespaces:
   ```powershell
   python _factor_moon_reports\\build_ftbquests_guide.py
   ```

8. Потом прогнать общую проверку сборки:
   ```powershell
   python _factor_moon_reports\\factor_moon_static_validate.py
   ```

## Правила Для Редактора

- Держи одну игровую идею в одном файле главы.
- Проверяй mod id по `_factor_moon_reports/current_factor_moon_mod_inventory.csv`.
- Не добавляй активные квесты на моды, которых еще нет в сборке. Лучше держать такие главы в архиве.
- Если меняешь только предмет удаленного мода на аналог, оставляй старый quest id, чтобы прогресс игроков не сбросился.
- Если полностью меняешь смысл квеста, генерируй новый quest id.
"""


def main() -> int:
    rows = chapter_rows()
    disabled = disabled_rows()
    write_csv(rows)
    OUT_MD.write_text(build_markdown(rows, disabled), encoding="utf-8")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
