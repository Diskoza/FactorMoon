# FactorMoon Build Report

Updated: 2026-06-06 15:40

## Direction
- FactorMoon is based on the `aeronaftics` mega-pack line plus the CreateAERO/Cobblemon merge layer.
- Runtime target remains Minecraft 1.21.1 / NeoForge 21.1.228.
- Firearms, artillery, Immersive Aircraft, Small Ships, NiftyCarts, and Infinite Music remain excluded for balance.

## Current Validation
- Installed active jar files: 482
- Unique primary mod ids: 479
- Duplicate primary mod ids: 0
- Missing required dependencies in static NeoForge/Forge/Fabric metadata check: 0
- Weapon/artillery suspects left in active `mods`: 0
- Fabric-only jars without support: 0
- Fabric jars expected through Sinytra Connector: 1 (`trinkets-3.10.0.jar`)
- Active `mods` size after the friend recommendation slim pass: about 0.92 GiB, down from about 1.80 GiB.
- First launch found version-range blockers in active `mods`: `AdvancementPlaques-1.21.11-neoforge-1.7.0.jar`, `BetterF3-17.0.0-NeoForge-1.21.11.jar`, and `trinkets-4.0.0-beta.2+26.1.jar`; these have now been replaced.
- Second launch found a Java module split-package between Ars Nouveau's bundled `lambdynlights_api` and `sodiumdynamiclights`; this has now been patched by replacing Sodium Dynamic Lights and removing the duplicate `dynamiclights-26.1.2.1NF.jar`.
- Third launch found a client mixin crash from `entity_model_features-3.2.4-1.21.11-neoforge.jar`; EMF and ETF have now been replaced with their `1.21` NeoForge line for the 1.21.1 pack target.
- Fourth launch found stale All The Mods / Crash Assistant branding plus a `Supplementaries` EMF compatibility mixin descriptor crash. `CrashAssistant` and `better-compatability-checker` are no longer active, and `Supplementaries` is now updated to `1.21.1-3.6.7`.
- Fifth launch found `Omega Config Architectury` registering Architectury networking too early from its client mixin. Active `omegaconfig-neoforge-1.5.1.jar` is now a FactorMoon patched jar with that client mixin registration disabled.
- Sixth launch found a `MusicNotification` client tick NPE and `Not Enough Crashes` repeatedly catching the same crash, making the client look stuck. `musicnotification-neoforge-3.0.0+mc1.21.1.jar`, `notenoughcrashes-neoforge-4.4.9+1.21.1.jar`, and their configs are no longer active.
- Seventh launch found `Sound Physics Remastered` putting ModLoader into broken client-event state and a recovery failure for `legendarymonuments:distortion_portal#main`. `Sound Physics Remastered` is no longer active, and `factormoon-legendarymonuments-patch-1.0.0.jar` now registers the missing Legendary Monuments model layer.
- Eighth launch found `Supplementaries 1.21.1-3.6.7` calling a newer Moonlight API (`ConfigBuilder.parentCategory()`) that was missing from active `Moonlight 1.21.1-3.0.5`. Moonlight is now updated to `moonlight-neoforge-1.21.1-3.0.16.jar`.
- Ninth launch found `accessories_compat_layer` rejected alongside real `Curios`, plus a stale `allthetweaks -> bcc` dependency override left after removing Better Compatibility Checker. `accessories_compat_layer-neoforge-0.1.12+1.21.1.jar` is no longer active, and `config/fml.toml` no longer references `bcc`.
- Tenth launch reached world creation/list loading, then failed on datapack registry data: `COBBLEVERSE-DP-v18-CF.zip` referenced missing BCA structure ids and missing `lumymon:music.raid`. That datapack is now patched in place, and the foreign Cobbleverse/CurseForge/ATM main-menu layer has been moved out of active mods/configs.
- Eleventh through fourteenth launches reached Biome Replacer during world creation and exposed several 1.21.11-to-1.21.1 ABI mismatches. Active `biomereplacer-2.2.1-pinkeen-neo.jar` is now patched for `registryOrThrow`, `ResourceLocation` / `ResourceKey.location()`, `Registry.getHolder(ResourceKey)`, and TerraBlender's `Registry.getHolderOrThrow(ResourceKey)` holder lookup.
- FactorMoon instance memory was adjusted from `minMemory=12288` / `maxMemory=25600` to `minMemory=8192` / `maxMemory=24576`. Recent crash reports showed Java launching with `-Xms28672M`, which reserved too much RAM up front and left Windows under heavy virtual-memory pressure.
- Fifteenth launch reached spawn-chunk generation and then stalled after a critical mixin conflict: `artifacts` could not inject into `NaturalSpawner` because `tpsum` had already overwritten the same spawn method. Active `tpsum-1.21.1-0.0.3.jar` is now patched to keep its non-spawn optimizations while removing only the `entity_spawn` mixins from `tpsum.mixins.json`.
- The visible recipe-browser conflict was reduced to the `aeronaftics` JEI stack. EMI, EMI addons, REI, and the EMI-only `extra_mod_integrations` addon are no longer active; after the friend recommendation slim pass, active recipe-browser jars are `jei`, `ae2jeiintegration`, and `ftb-jei-extras`.
- The friend recommendation slim pass moved 189 active jar files and 385 KubeJS script/data files out of active use, leaving local backups in `_disabled_mods/2026-06-06-friend-slim-pass`. The disabled areas include ATM leftovers, Refined Storage, duplicate tech stacks, large magic stacks, extra dimensions, MineColonies, and duplicate map/UI/food/decor layers.
- The next launch found Railcraft Reborn calling LambDynamicLights API classes that were absent from the earlier no-LambAPI Sodium Dynamic Lights patch. Active Sodium Dynamic Lights is now `sodiumdynamiclights-neoforge-1.0.10-1.21.1.jar`, which provides `DynamicLightHandler` and `DynamicLightHandlers`; the old patched jar is backed up in `_factor_moon_reports/replaced_mod_backups/2026-06-06-railcraft-lambdynlights-api`.
- The static validator now writes `_factor_moon_reports/validation_unsupported_dependency_versions.csv`; it is intentionally broad, so the focused first-launch interpretation is in `_factor_moon_reports/create_and_first_launch_audit.md`.

## Newly Ported Locally
- `cobblemon-extra-ride-compat-neoforge-0.1.1.jar`
  - Full NeoForge rebuild from the preserved custom source.
  - Keeps the Cobblemon riding mixins and copied species data.
- `only-bottle-caps-neoforge-1.3.0-port.1.jar`
  - NeoForge/Cobblemon Java port.
  - Registers all bottle cap items, carries original assets/recipes/tags, and keeps the IV-changing `PokemonSelectingItem` behavior.
  - Fishing loot injection still needs a NeoForge Global Loot Modifier pass if exact Fabric drop behavior is required.
- `cobbleversebadges-neoforge-1.3-port.1.jar`
  - Safe content-port for badges, trophies, badge box items, assets, lang, and copied data.
  - Badge-box storage GUI is not included yet; that needs a separate menu/screen handler port.
- `poke-clothing-neoforge-1.1.2-port.1.jar`
  - Base NeoForge port for Poke Clothing.
  - Registers cloth items, wearable armor pieces, armor materials, the tailoring station block/item, assets, tags, and safe vanilla recipes.
  - Custom tailoring GUI and `poke-clothing:tailoring` recipes are intentionally left for a second pass so datapack reload does not fail on an unported recipe type.

## Cobblemon Transfer
- Cobblemon-side jars covered in current FactorMoon: 145
- Cobblemon-side jars explicitly skipped by balance/user rule: 4
- Cobblemon-side jars still not transferred: 12
- No remaining items are pending from provided links.
- The remaining 12 have no working provided NeoForge link and need a manual NeoForge port or a skip decision.

## Remaining Port/Skip Queue
- `cardinal-components` (`cardinal-components-api-6.1.3.jar`)
- `cobblecuisine` (`cobblecuisine-2.0.1-1.7-rc1.jar`)
- `cobblemonbattlepositions` (`cobblemon-battle-positions-1.1.3.jar`)
- `cobblemon-fight-them-all` (`cobblemon-fight-them-all-1.0.4-cobblemon-1.7.3.jar`)
- `unknown:Debugify-1.21.1+1.0` (`Debugify-1.21.1+1.0.jar`)
- `interactic` (`interactic-0.2.3+1.21.jar`)
- `cozyhome` (`Luckys-Cozyhome-Refurnished-1.1.20.jar`)
- `lumymon` (`LumyMon-0.6.3.jar`)
- `lumyrei` (`LumyREI-1.1.2.jar`)
- `pokeblocks` (`pokeblocks-1.4.0-1.21.1.jar`)
- `respackopts` (`respackopts-4.11.3.jar`)
- `stackdeobfuscator` (`StackDeobfuscatorFabric-1.4.3+08e71cc.jar`)
- User-confirmed mandatory manual ports are tracked in `_factor_moon_reports/mandatory_neoforge_ports.md`.

## Notes On Manual Downloads
- The 16 manually downloaded jars are preserved in `FactorMoon/mods`.
- The wrong-version `1.21.11` / `26.1` first-launch blockers were moved to `_factor_moon_reports/replaced_mod_backups/2026-06-05-first-launch-blockers`.
- Active replacements are `AdvancementPlaques-1.21.1-neoforge-1.6.8.jar`, `BetterF3-11.0.3-NeoForge-1.21.1.jar`, and `trinkets-3.10.0.jar`.
- `trinkets-3.10.0.jar` is the original Fabric 1.21.1 Trinkets jar from `cobblemon-extra`, loaded through Sinytra Connector because no valid NeoForge `Trinkets Updated` 1.21.1 build was found.
- The dynamic-lights conflict files were moved to `_factor_moon_reports/replaced_mod_backups/2026-06-05-dynamic-lights-conflict`.
- Active Sodium Dynamic Lights is now `sodiumdynamiclights-neoforge-1.0.5-1.21.1-factormoon-no-lambapi.jar`, a local patched build with the duplicate LambDynamicLights API class removed.
- The EMF/ETF 1.21.11 conflict files were moved to `_factor_moon_reports/replaced_mod_backups/2026-06-05-emf-etf-12111-mixin`.
- Active EMF/ETF files are now `entity_model_features-3.2.4-1.21-neoforge.jar` and `entity_texture_features_1.21-neoforge-7.1.jar`.
- `CrashAssistant-neoforge-1.20.6-1.21.4-1.11.6.jar`, `better-compatability-checker-neoforge-21.1.8.jar`, `config/bcc-common.toml`, and `config/crash_assistant/` were moved to `_factor_moon_reports/replaced_mod_backups/2026-06-05-remove-atm-crash-branding`.
- `supplementaries-1.21-3.5.33-neoforge.jar` was moved to `_factor_moon_reports/replaced_mod_backups/2026-06-05-supplementaries-emf-compat`; active Supplementaries is now `supplementaries-neoforge-1.21.1-3.6.7.jar`.
- Original `omegaconfig-neoforge-1.5.1.jar` was moved to `_factor_moon_reports/replaced_mod_backups/2026-06-05-omegaconfig-early-architectury`; active `omegaconfig-neoforge-1.5.1.jar` is patched from `_factor_moon_reports/replacement_candidates/omegaconfig-neoforge-1.5.1-factormoon-no-client-mixin.jar`.
- `musicnotification-neoforge-3.0.0+mc1.21.1.jar`, `notenoughcrashes-neoforge-4.4.9+1.21.1.jar`, `config/musicnotification.json`, and `config/notenoughcrashes.json` were moved to `_factor_moon_reports/replaced_mod_backups/2026-06-05-musicnotification-nec-crash-loop`.
- `sound-physics-remastered-neoforge-1.21.1-1.5.1.jar` and `config/sound_physics_remastered/` were moved to `_factor_moon_reports/replaced_mod_backups/2026-06-05-sound-physics-legendary-layer`; active `factormoon-legendarymonuments-patch-1.0.0.jar` was built from `_factor_moon_reports/patch_sources/factormoon_legendarymonuments_patch`.
- `moonlight-neoforge-1.21.1-3.0.5.jar` was moved to `_factor_moon_reports/replaced_mod_backups/2026-06-05-moonlight-for-supplementaries-367`; active Moonlight is now `moonlight-neoforge-1.21.1-3.0.16.jar`.
- `accessories_compat_layer-neoforge-0.1.12+1.21.1.jar` and the original `config/fml.toml` were moved/copied to `_factor_moon_reports/replaced_mod_backups/2026-06-05-accessories-compat-layer-curios-conflict`; active `config/fml.toml` has no stale `+bcc` dependency override.
- `fancymenu_neoforge_3.8.1_MC_1.21.1.jar`, `drippyloadingscreen_neoforge_3.1.0_MC_1.21.1.jar`, `config/fancymenu/`, and `config/drippyloadingscreen/` were moved to `_factor_moon_reports/replaced_mod_backups/2026-06-06-worldgen-menu-cleanup`.
- `datapacks/COBBLEVERSE-DP-v18-CF.zip` was patched in place after backing up the original to `_factor_moon_reports/replaced_mod_backups/2026-06-06-worldgen-menu-cleanup/datapacks/`; the patch removes missing BCA structure references and replaces missing LumyMon raid music with `minecraft:music.game`.
- Main-menu add-ons were reduced further by setting `config/cpm.json:titleScreenButton=false`, `config/create-client.toml:mainMenuConfigButtonRow=0`, and Mod Menu `modify_title_screen=false`.
- `biomereplacer-2.2.1-pinkeen-neo.jar` was patched in place after backing up the original to `_factor_moon_reports/replaced_mod_backups/2026-06-06-biomereplacer-1211-abi`; the patch keeps Biome Replacer active on Minecraft 1.21.1 by replacing its 1.21.11-only `lookupOrThrow` call with `registryOrThrow`. The same backup folder contains the original Handcrafted KubeJS recipe script; active `kubejs/server_scripts/mods/Handcrafted/Recipes.js` now reads recipe json through `toString()` and guards unexpected recipe shapes.
- `reforgedplaymod-1.21.1-0.3.jar`, `config/replaymod.json`, and `.replay_cache/` were moved to `_factor_moon_reports/replaced_mod_backups/2026-06-06-remove-replay-restore-cpm`; Replay keybind entries were removed from `options.txt`, and `replay_recordings/` was left in place as user data. `config/cpm.json:titleScreenButton` was restored to `true`.
- `biomereplacer-2.2.1-pinkeen-neo.jar` was patched again after backing up the previous active jar to `_factor_moon_reports/replaced_mod_backups/2026-06-06-remove-replay-restore-cpm/mods/`; the patch rewrites remaining `Identifier` / `ResourceKey.identifier()` references to 1.21.1-compatible `ResourceLocation` / `ResourceKey.location()` calls.
- `biomereplacer-2.2.1-pinkeen-neo.jar` was patched again after backing up the previous active jar to `_factor_moon_reports/replaced_mod_backups/2026-06-06-biomereplacer-registry-getholder`; the patch rewrites `Registry.get(ResourceKey)` calls in `VanillaReplacer` and `BlueprintReplacer` to 1.21.1-compatible `Registry.getHolder(ResourceKey)`.
- `biomereplacer-2.2.1-pinkeen-neo.jar` was patched again after backing up the previous active jar to `_factor_moon_reports/replaced_mod_backups/2026-06-06-biomereplacer-terrablender-holderorthrow`; the patch rewrites TerraBlender's `Registry.getOrThrow(ResourceKey)` holder call to `Registry.getHolderOrThrow(ResourceKey)`.
- `instance.json` was backed up to `_factor_moon_reports/replaced_mod_backups/2026-06-06-memory-settings` and adjusted to start with 8 GiB while keeping a 24 GiB upper heap cap.
- `tpsum-1.21.1-0.0.3.jar` was patched after backing up the original to `_factor_moon_reports/replaced_mod_backups/2026-06-06-tpsum-artifacts-spawn-mixin`; the patch removes `entity_spawn.MixinNaturalSpawner$redirect_to_optimized_methods` and `entity_spawn.MixinSpawnState$optimize_operation` from `tpsum.mixins.json` so `Artifacts` can apply its `NaturalSpawnerMixin`.
- `emi-1.1.22+1.21.1+neoforge.jar`, `emi_enchanting-0.1.2+1.21+neoforge.jar`, `emi_loot-0.7.9+1.21+neoforge.jar`, `emixx-neoforge-1.2.3.jar`, `RoughlyEnoughItems-16.0.799-neoforge.jar`, `extra-mod-integrations-all-neoforge-1.0.3+1.21.1.jar`, and their EMI/REI configs/logs were moved to `_factor_moon_reports/replaced_mod_backups/2026-06-06-jei-only-aeronaftics`.

## Custom Mods And Translations
- Preserved custom/personal Fabric references under `_cobblemon_extra_reference/custom_mods_fabric_original` and `_cobblemon_extra_reference/custom_sources`.
- Extracted Russian `ru_ru.json` files from `cobblemon-extra` Fabric jars into `kubejs/assets/.../lang/ru_ru.json` without overwriting existing FactorMoon translations.
- Important extracted translation layers include PokeNav, Cobblemon Battle Extras, Catch Rate Display, Wonder Trade, and Legendary Monuments.
- Cobblepedia NeoForge is installed, but no local `ru_ru` Cobblepedia translation was found in the Fabric jar or copied resource/datapack layers.

## Key Report Files
- `_factor_moon_reports/cobblemon_not_transferred.csv`
- `_factor_moon_reports/cobblemon_pending_with_user_links.csv`
- `_factor_moon_reports/cobblemon_needs_port_or_skip_no_link.csv`
- `_factor_moon_reports/validation_summary.json`
- `_factor_moon_reports/validation_missing_dependencies.csv`
- `_factor_moon_reports/validation_first_launch_blockers.csv`
- `_factor_moon_reports/validation_unsupported_dependency_versions.csv`
- `_factor_moon_reports/create_and_first_launch_audit.md`
- `_factor_moon_reports/friend_recommendation_slim_pass.md`
- `_factor_moon_reports/friend_slim_pass_plan.json`
- `_factor_moon_reports/friend_slim_pass_moved.json`
- `_factor_moon_reports/port_candidate_analysis.csv`
- `_factor_moon_reports/kubejs_ru_translation_overrides.csv`
- `_factor_moon_reports/custom_reference_copy_manifest.csv`
- `ACTIVE_MODS.md` / `ACTIVE_MODS.json`
- `RESOURCEPACKS.md` / `RESOURCEPACKS.json`
