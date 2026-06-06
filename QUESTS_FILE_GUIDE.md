# FactorMoon: работа с FTB Quests через файлы

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

| Группа | Файл | Название | Квестов | Отсутствующие namespace | Кастомные типы задач |
| --- | --- | --- | --- | --- | --- |
| Ungrouped | 01_first_steps.snbt | 01_first_steps | 12 | cobblemon_tasks | cobblemon_tasks:cobblemon_task |
| Ungrouped | 02_into_the_wild.snbt | 02_into_the_wild | 14 | cobblemon_tasks | cobblemon_tasks:cobblemon_task |
| Ungrouped | 03_trainers_nest.snbt | 03_trainers_nest | 10 | - | - |
| Ungrouped | 04_pokedex_chronicles.snbt | 04_pokedex_chronicles | 12 | cobblemon_tasks | cobblemon_tasks:cobblemon_task |
| Ungrouped | 05_raid_frontline.snbt | 05_raid_frontline | 12 | - | - |
| Ungrouped | 06_bond_and_breed.snbt | 06_bond_and_breed | 10 | cobblemon_tasks | cobblemon_tasks:cobblemon_task |
| Ungrouped | 07_type_gauntlet.snbt | 07_type_gauntlet | 14 | cobblemon_tasks | cobblemon_tasks:cobblemon_task |
| Ungrouped | 08_legendary_hunt.snbt | 08_legendary_hunt | 10 | cobblemon_tasks | cobblemon_tasks:cobblemon_task |
| Ungrouped | 09_elite_challenge.snbt | 09_elite_challenge | 10 | cobblemon_tasks | cobblemon_tasks:cobblemon_task |
| Ungrouped | 10_champion.snbt | 10_champion | 8 | cobblemon_tasks | cobblemon_tasks:cobblemon_task |
| Ungrouped | 11_relics_transport.snbt | 11_relics_transport | 4 | - | - |
| Resources | apotheosis_2.snbt | Apothic Spawners | 38 | ars_additions, draconicevolution, enderio, evilcraft, industrialforegoing, mysticalagriculture, pneumaticcraft, reliquary | - |
| Tools and Gear | apotheosis_gear.snbt | Apotheosis Gear | 50 | allthemodium | - |
| Magic | apothic_enchanting.snbt | Apothic Enchanting | 56 | - | - |
| Storage | applied_energistics_2.snbt | Applied Energistics 2 | 73 | - | - |
| Tools and Gear | artifacts.snbt | Artifacts | 63 | - | - |
| Exploration | cataclysm.snbt | Cataclysm | 146 | dyenamics | - |
| Tech | create.snbt | Create | 206 | alltheores, the_bumblezone | - |
| Storage | extended__advanced_ae.snbt | Extended \\& Advanced AE | 68 | allthetweaks, enderio | - |
| Power | generators.snbt | Generators N Furnaces | 88 | allthetweaks, generatorgalore | - |
| Exploration | ice__fire.snbt | &bIce &fand &cFire | 126 | allthemodium, alltheores | - |
| Tech | justdirethings.snbt | Just Dire Things | 157 | actuallyadditions, allthetweaks, mekanism | - |
| Logistics | modular_router.snbt | Modular Routers | 64 | - | - |
| Power | powah.snbt | Powah | 147 | allthetweaks | - |
| Resources | productive_trees.snbt | Productive Trees | 169 | allthetweaks, productivelib | - |
| Logistics | pylons.snbt | Pylons | 21 | - | - |
| Tech | railcraft.snbt | RailCraft | 75 | cookingforblockheads, mekanism | - |
| Tools and Gear | relics.snbt | Relics | 43 | aquaculture, ars_nouveau | - |
| Tools and Gear | silent_gear.snbt | Silent Gear | 71 | mysticalagriculture | - |

## Отключенные Главы

Эти файлы не удалены. Они вынесены из активной папки, чтобы книга не показывала квесты от удаленных модов, но сами главы можно вернуть или использовать как черновики.

| Файл | Действие | Причина | Манифест |
| --- | --- | --- | --- |
| achapter_2r_6the_atm_star.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| allthemodium.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| ars_nouveau.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| bumblezone.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| chapter_2_the_star.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| deeper_and_darker.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| draconic_evolution.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| elmystical_agriculturerr.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| eternal_starlight.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| evilcraft.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| extreme_reactors.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| forbidden__arcanus.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| hostile_neural_networks.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| immersive_engineering.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| industrial_foregoing.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| integrated_dynamics.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| iron_spells_and_spellbooks.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| mahou_tsukai.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| mainquestline_part_1.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| mekanism.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| mekanism_reactors.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| mi_digital.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| mi_electric.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| mi_endgame.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| mi_steam.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| natures_aura.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| occultism.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| oritech.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| pneumaticcraft.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| refined_storage.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| theurgy.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| twilight_forest.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| undergarden.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| xycraft.snbt | moved_out_of_active_chapters | Primary mod is absent from FactorMoon or chapter is ATM10 star/progression content | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_chapter_manifest.csv |
| basic_armor.snbt | moved_out_of_active_chapters | Generic ATM10 chapter has many references to absent mods and should be rebuilt for FactorMoon | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_generic_chapter_manifest.csv |
| basic_logistics.snbt | moved_out_of_active_chapters | Generic ATM10 chapter has many references to absent mods and should be rebuilt for FactorMoon | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_generic_chapter_manifest.csv |
| basic_power.snbt | moved_out_of_active_chapters | Generic ATM10 chapter has many references to absent mods and should be rebuilt for FactorMoon | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_generic_chapter_manifest.csv |
| basic_tools.snbt | moved_out_of_active_chapters | Generic ATM10 chapter has many references to absent mods and should be rebuilt for FactorMoon | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_generic_chapter_manifest.csv |
| bounty_board.snbt | moved_out_of_active_chapters | Generic ATM10 chapter has many references to absent mods and should be rebuilt for FactorMoon | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_generic_chapter_manifest.csv |
| building_tips.snbt | moved_out_of_active_chapters | Generic ATM10 chapter has many references to absent mods and should be rebuilt for FactorMoon | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_generic_chapter_manifest.csv |
| food_and_farming.snbt | moved_out_of_active_chapters | Generic ATM10 chapter has many references to absent mods and should be rebuilt for FactorMoon | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_generic_chapter_manifest.csv |
| productive_bees.snbt | moved_out_of_active_chapters | Generic ATM10 chapter has many references to absent mods and should be rebuilt for FactorMoon | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_generic_chapter_manifest.csv |
| storage.snbt | moved_out_of_active_chapters | Generic ATM10 chapter has many references to absent mods and should be rebuilt for FactorMoon | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_generic_chapter_manifest.csv |
| tips_and_tricks.snbt | moved_out_of_active_chapters | Generic ATM10 chapter has many references to absent mods and should be rebuilt for FactorMoon | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_generic_chapter_manifest.csv |
| welcome.snbt | moved_out_of_active_chapters | ATM10 logo/Discord welcome page does not belong to FactorMoon | _factor_moon_reports/disabled_quests/2026-06-06-removed-mod-chapters/disabled_welcome_manifest.csv |

## Что Еще Нужно Почистить

| Активный файл | Отсутствующие namespace | Кастомные типы задач |
| --- | --- | --- |
| 01_first_steps.snbt | cobblemon_tasks | cobblemon_tasks:cobblemon_task |
| 02_into_the_wild.snbt | cobblemon_tasks | cobblemon_tasks:cobblemon_task |
| 04_pokedex_chronicles.snbt | cobblemon_tasks | cobblemon_tasks:cobblemon_task |
| 06_bond_and_breed.snbt | cobblemon_tasks | cobblemon_tasks:cobblemon_task |
| 07_type_gauntlet.snbt | cobblemon_tasks | cobblemon_tasks:cobblemon_task |
| 08_legendary_hunt.snbt | cobblemon_tasks | cobblemon_tasks:cobblemon_task |
| 09_elite_challenge.snbt | cobblemon_tasks | cobblemon_tasks:cobblemon_task |
| 10_champion.snbt | cobblemon_tasks | cobblemon_tasks:cobblemon_task |
| apotheosis_2.snbt | ars_additions, draconicevolution, enderio, evilcraft, industrialforegoing, mysticalagriculture, pneumaticcraft, reliquary | - |
| apotheosis_gear.snbt | allthemodium | - |
| cataclysm.snbt | dyenamics | - |
| create.snbt | alltheores, the_bumblezone | - |
| extended__advanced_ae.snbt | allthetweaks, enderio | - |
| generators.snbt | allthetweaks, generatorgalore | - |
| ice__fire.snbt | allthemodium, alltheores | - |
| justdirethings.snbt | actuallyadditions, allthetweaks, mekanism | - |
| powah.snbt | allthetweaks | - |
| productive_trees.snbt | allthetweaks, productivelib | - |
| railcraft.snbt | cookingforblockheads, mekanism | - |
| relics.snbt | aquaculture, ars_nouveau | - |
| silent_gear.snbt | mysticalagriculture | - |

Важные заметки:

- `cobblemon_tasks:cobblemon_task` используется в кастомной Cobblemon-линейке, но сейчас активные jar не дают mod id `cobblemon_tasks` и очевидных ресурсов под этот тип задач. Нужно либо портировать этот task provider, либо заменить такие задачи на стандартные типы FTB Quests.
- `03_trainers_nest.snbt` уже переведен с Tom's Storage на Sophisticated Storage: `sophisticatedstorage:controller` и `sophisticatedstorage:storage_link`.
- `06_bond_and_breed.snbt` больше не требует `cobblecuisine:coffee`; временно используется `minecraft:honey_bottle`, пока CobbleCuisine не перенесен.
- Отключенные generic-главы ATM10 лучше не возвращать как есть. Их стоит пересобрать заново как FactorMoon-гайды.

## Как Редактировать

1. Найти нужную главу или предмет:
   ```powershell
   rg -n "chapter title or item id" config\ftbquests\quests\chapters
   ```

2. Заменить предмет в задании или награде:
   ```snbt
   item: { count: 1, id: "modid:item_name" }
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
   python _factor_moon_reports\build_ftbquests_guide.py
   ```

8. Потом прогнать общую проверку сборки:
   ```powershell
   python _factor_moon_reports\factor_moon_static_validate.py
   ```

## Правила Для Редактора

- Держи одну игровую идею в одном файле главы.
- Проверяй mod id по `_factor_moon_reports/current_factor_moon_mod_inventory.csv`.
- Не добавляй активные квесты на моды, которых еще нет в сборке. Лучше держать такие главы в архиве.
- Если меняешь только предмет удаленного мода на аналог, оставляй старый quest id, чтобы прогресс игроков не сбросился.
- Если полностью меняешь смысл квеста, генерируй новый quest id.
