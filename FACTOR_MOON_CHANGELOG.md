# FactorMoon Chronology

This file tracks the merge and repair work done while turning the `aeronaftics` / CreateAERO / Cobblemon pack mix into the NeoForge-based FactorMoon test pack.

## 2026-06-04 Initial Merge Direction

- Created FactorMoon as a NeoForge 1.21.1 / NeoForge 21.1.228 pack line.
- Used the `aeronaftics` mega-pack as the semantic base because it represents the evolved CreateAERO direction.
- Kept Create Aeronautics as the reason for NeoForge being the target loader.
- Excluded firearms/artillery and user-skipped travel mods for balance, including Immersive Aircraft, Small Ships, NiftyCarts, and Infinite Music.
- Began transferring Cobblemon-side mods where NeoForge builds existed.
- Preserved custom Fabric references and source material under `_cobblemon_extra_reference`.

## 2026-06-05 Cobblemon Transfer And Local Ports

- Installed/copy-matched available NeoForge versions from the user-provided Cobblemon links.
- Preserved extracted Russian translation assets in `kubejs/assets/.../lang/ru_ru.json` without overwriting existing FactorMoon translations.
- Built or staged local NeoForge ports for:
  - `cobblemon-extra-ride-compat-neoforge-0.1.1.jar`
  - `only-bottle-caps-neoforge-1.3.0-port.1.jar`
  - `cobbleversebadges-neoforge-1.3-port.1.jar`
  - `poke-clothing-neoforge-1.1.2-port.1.jar`
- Recorded remaining mandatory manual ports in `_factor_moon_reports/mandatory_neoforge_ports.md`.

## 2026-06-05 First Launch Fixes

- Replaced first-launch Minecraft-version blockers:
  - `AdvancementPlaques-1.21.11-neoforge-1.7.0.jar` -> `AdvancementPlaques-1.21.1-neoforge-1.6.8.jar`
  - `BetterF3-17.0.0-NeoForge-1.21.11.jar` -> `BetterF3-11.0.3-NeoForge-1.21.1.jar`
  - `trinkets-4.0.0-beta.2+26.1.jar` -> `trinkets-3.10.0.jar` through Sinytra Connector
- Patched the Sodium Dynamic Lights / LambDynamicLights API split-package conflict by using a local no-LambAPI Sodium Dynamic Lights jar.
- Replaced EMF/ETF 1.21.11 builds with their 1.21-compatible NeoForge builds.
- Removed Crash Assistant and Better Compatibility Checker to get rid of stale All The Mods 10 crash branding and support UI.
- Updated Supplementaries to `1.21.1-3.6.7`.
- Patched OmegaConfig to avoid early Architectury client networking registration.
- Moved Music Notification and Not Enough Crashes out of active use after a client tick crash loop.
- Added `factormoon-legendarymonuments-patch-1.0.0.jar` to register the missing Legendary Monuments model layer.
- Moved Sound Physics Remastered out after it broke client-event loading.
- Updated Moonlight to `moonlight-neoforge-1.21.1-3.0.16.jar`.
- Removed `accessories_compat_layer` because real Curios is active and the layer was rejected by compatibility checks.

## 2026-06-06 World Creation Fixes

- Removed FancyMenu and DrippyLoadingScreen active layers to clear foreign Cobbleverse/CurseForge/ATM menu overlays.
- Patched `COBBLEVERSE-DP-v18-CF.zip` to remove missing BCA structure references and replace missing `lumymon:music.raid` with `minecraft:music.game`.
- Restored the Customizable Player Models skin editor button after Replay removal.
- Removed Replay/ReForgedPlay active mod/config/cache by user request, while leaving `replay_recordings/` as user data.
- Patched `biomereplacer-2.2.1-pinkeen-neo.jar` across several 1.21.11-to-1.21.1 ABI mismatches:
  - `lookupOrThrow` -> `registryOrThrow`
  - `Identifier` -> `ResourceLocation`
  - `ResourceKey.identifier()` -> `ResourceKey.location()`
  - `Registry.get(ResourceKey)` optional holder paths -> `Registry.getHolder(ResourceKey)`
  - TerraBlender holder lookup -> `Registry.getHolderOrThrow(ResourceKey)`
- Lowered instance memory to start at 8 GiB and cap at 24 GiB after crash reports showed Java reserving too much RAM up front.
- Patched `tpsum-1.21.1-0.0.3.jar` to remove only its entity-spawn mixins so `Artifacts` can apply its `NaturalSpawnerMixin`.
- Reduced recipe-browser conflicts to the `aeronaftics` JEI stack:
  - Kept `jei`, `ae2jeiintegration`, `ftb-jei-extras`, and temporarily `refinedstorage-jei-integration`.
  - Moved EMI, EMI addons, REI, `extra_mod_integrations`, and their EMI/REI configs/logs to backup.

## 2026-06-06 Friend Recommendation Slim Pass

- Applied the friend's recommendation to refocus FactorMoon away from ATM-style mega-pack sprawl and toward Create / Aeronautics, Cobblemon, AE2, JEI, worldgen, QoL, and performance.
- Moved 189 active jar files out of `mods`, reducing active jars from 671 to 482.
- Moved 385 KubeJS script/data files tied to disabled mod namespaces out of active `kubejs`.
- Disabled the Refined Storage stack now that AE2 is the chosen storage axis.
- Disabled large duplicate tech/magic/dimension/progression stacks including Mekanism, Modern Industrialization, Industrial Foregoing, Ender IO, Immersive Engineering, Ars Nouveau, Occultism, Theurgy, Mystical Agriculture, MineColonies, Aether, BetterNether, Twilight Forest, Bumblezone, and ATM leftovers.
- Left disabled files locally in `_disabled_mods/2026-06-06-friend-slim-pass`; this folder is ignored by Git.
- Updated `ACTIVE_MODS.*`, `current_factor_moon_mod_inventory.csv`, validation files, and added `_factor_moon_reports/friend_recommendation_slim_pass.md`.

## 2026-06-06 Railcraft Dynamic Lights Fix

- Fixed the next launch blocker where Railcraft Reborn crashed during `FMLClientSetupEvent` with missing `dev/lambdaurora/lambdynlights/api/DynamicLightHandler`.
- Replaced `sodiumdynamiclights-neoforge-1.0.5-1.21.1-factormoon-no-lambapi.jar` with `sodiumdynamiclights-neoforge-1.0.10-1.21.1.jar`.
- The old no-LambAPI jar was moved to `_factor_moon_reports/replaced_mod_backups/2026-06-06-railcraft-lambdynlights-api`.
- This is safe after the friend slim pass because Ars Nouveau, the previous duplicate LambDynamicLights API source, is no longer active.

## 2026-06-06 Final Cobblemon Connector Ports And Quest Cleanup

- Added the remaining requested Cobblemon battle-side Fabric mods through targeted Connector bridge patches:
  - `cobblemon-fight-them-all-1.0.4-cobblemon-1.7.3-factormoon-connector.jar`
  - `cobblemon-battle-positions-1.1.3-factormoon-connector.jar`
- Fight Them All keeps its original Fabric/Kotlin logic, but FactorMoon adds Java entrypoint wrappers and relaxed metadata so it can load without Fabric Language Kotlin.
- Battle Positions keeps the original Fabric implementation and now uses relaxed Fabric loader metadata; Cobblemon, RCT API, Forgified Fabric API, and Sinytra Connector satisfy its runtime side.
- Updated `_factor_moon_reports/mandatory_neoforge_ports.md` to mark both mods as installed.
- Cleaned the FTB Quests book by moving stale ATM10 and removed-mod chapters out of active `config/ftbquests/quests/chapters`.
- Removed old active quest references to Tom's Storage, CobbleCuisine coffee, Small Ships, NiftyCarts, Immersive Aircraft, and the ATM Star book icon.
- Replaced Tom's Storage quest targets with Sophisticated Storage targets in `03_trainers_nest.snbt`.
- Replaced the temporary CobbleCuisine coffee quest item with `minecraft:honey_bottle` until CobbleCuisine is ported.
- Added `QUESTS_FILE_GUIDE.md` plus `_factor_moon_reports/ftbquests_active_structure.csv` to document the active quest structure and file-edit workflow.

## 2026-06-06 Particle Rain Resource Reload Fix

- Fixed the next client crash reported as `Rendering overlay`.
- The visible stack entered `NoChatReports` while Minecraft tried to show a resource-pack recovery toast, but the recovery reason was a `Particle Rain` null config read:
  - `Cannot read field "compat" because "pigcart.particlerain.config.ConfigManager.config" is null`
  - `SpriteLoaderMixin.registerWeatherParticleSprites`
- Patched `particlerain-4.0.0-beta.10+1.21.1-neoforge.jar` locally with `pigcart.particlerain.patch.ConfigGuard`.
- The patched mixin now asks `ConfigGuard.waterTint()` instead of reading `ConfigManager.config.compat.waterTint` directly, so an early resource reload can continue until Particle Rain has loaded its config.
- Added the reproducible patch source/script under `_factor_moon_reports/patch_sources/particlerain_null_config_guard`.
- Rebuilt the helper class with `javac --release 21` after the first local patch was accidentally compiled as Java 25 bytecode, which Minecraft's Java 21 runtime cannot load.
- Extended the same guard to `TextureUtil.getRippleResolution`, covering the next early reload crash where `ConfigManager.config.ripple` was still null.

## Current State

- Runtime target: Minecraft 1.21.1 / NeoForge 21.1.228.
- Active jar count after the two Cobblemon Connector bridge ports: 484.
- Static validation: no duplicate primary mod IDs, no missing required dependencies, no Fabric-only jars outside the expected Connector set.
- Active recipe browser baseline: JEI, AE2 JEI Integration, and FTB JEI Extras.
- Known remaining risk: the custom Cobblemon questline still references `cobblemon_tasks:cobblemon_task`; that task provider is not currently visible as an active mod id and should be ported or replaced with standard FTB Quests tasks.

## Detailed Logs

- Full launch-by-launch audit: `_factor_moon_reports/create_and_first_launch_audit.md`
- Build summary: `FACTOR_MOON_BUILD_REPORT.md`
- Active mod manifest: `ACTIVE_MODS.md` and `ACTIVE_MODS.json`
- Active resource-pack manifest: `RESOURCEPACKS.md` and `RESOURCEPACKS.json`
