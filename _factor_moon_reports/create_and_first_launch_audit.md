# FactorMoon first-launch / Create audit

Date: 2026-06-05
Runtime target: Minecraft 1.21.1 / NeoForge 21.1.228 / Create 6.0.10

## Seventeenth pass Friend recommendation slim pass

The user's friend's recommendations were applied as a broad but dependency-aware slimming pass before adding more performance mods.

Direction:

- Keep the pack centered on Create / Create Aeronautics, Cobblemon, AE2, JEI, worldgen, QoL, and performance.
- Stop carrying the ATM-style duplicate progression layers while the pack is still struggling to launch and generate worlds.
- Prefer reversible moves over permanent deletes.

Applied changes:

| Change | Reason |
|---|---|
| Moved 189 active jar files to `_disabled_mods/2026-06-06-friend-slim-pass` | Removes duplicate tech/magic/dimension/progression stacks while preserving local recovery copies. |
| Moved 385 KubeJS script/data files to the same backup | Prevents recipes/data from referencing disabled mod namespaces during datapack reload. |
| Disabled Refined Storage and RS integrations | AE2 is the chosen storage backbone for this direction. |
| Disabled ATM leftovers, Mekanism, Modern Industrialization, Industrial Foregoing, Ender IO, Immersive Engineering, Ars stack, Occultism, Theurgy, Mystical Agriculture, MineColonies, and several extra dimensions | Matches the friend's recommendation and cuts worldgen/startup/performance pressure. |
| Left passive `kubejs/assets/.../lang/ru_ru.json` translations in place | Avoids losing the user's translation work; passive lang assets should not break loading. |

Post-pass static check:

- Installed active jar files: 482
- Unique primary mod ids: 479
- Duplicate primary mod ids: 0
- Missing required dependencies: 0
- Fabric jars expected through Sinytra Connector: 1 (`trinkets-3.10.0.jar`)

Detailed report: `_factor_moon_reports/friend_recommendation_slim_pass.md`.

## Applied fix

The first-launch blocker jars were replaced in active `FactorMoon/mods`:

| Removed from active mods | Active replacement |
|---|---|
| `AdvancementPlaques-1.21.11-neoforge-1.7.0.jar` | `AdvancementPlaques-1.21.1-neoforge-1.6.8.jar` |
| `BetterF3-17.0.0-NeoForge-1.21.11.jar` | `BetterF3-11.0.3-NeoForge-1.21.1.jar` |
| `trinkets-4.0.0-beta.2+26.1.jar` | `trinkets-3.10.0.jar` |

The old jars were preserved in `_factor_moon_reports/replaced_mod_backups/2026-06-05-first-launch-blockers`.

Post-replacement static check:

- Installed active jar files: 686
- Duplicate primary mod ids: 0
- Missing required dependencies: 0
- Fabric jars expected through Sinytra Connector: 3

## Third launch EMF/ETF version fix

The next `latest.log` reached client mixin application and stopped in Entity Model Features:

```text
Mixin apply for mod entity_model_features failed entity_model_features.mixins.json:accessor.MinecraftClientAccessor
InvalidAccessorException: No candidates were found matching deltaTracker:Lnet/minecraft/client/DeltaTracker$Timer;
```

Root cause:

- `entity_model_features-3.2.4-1.21.11-neoforge.jar` was built for the 1.21.11 client class layout.
- `entity_texture_features_1.21.11-neoforge-7.1.jar` was from the same newer line and should stay paired with EMF by Minecraft line.
- FactorMoon targets Minecraft `1.21.1`, where those 1.21.11-only client classes and fields do not exist.

Applied fix:

| Removed from active mods | Active replacement |
|---|---|
| `entity_model_features-3.2.4-1.21.11-neoforge.jar` | `entity_model_features-3.2.4-1.21-neoforge.jar` |
| `entity_texture_features_1.21.11-neoforge-7.1.jar` | `entity_texture_features_1.21-neoforge-7.1.jar` |

Replacement candidates are in `_factor_moon_reports/replacement_candidates`; old jars are backed up in `_factor_moon_reports/replaced_mod_backups/2026-06-05-emf-etf-12111-mixin`.

Post-fix static check:

- Installed active jar files: 685
- Duplicate primary mod ids: 0
- Missing required dependencies: 0
- Fabric jars expected through Sinytra Connector: 3

## Fourth launch ATM branding removal and Supplementaries EMF fix

The next crash reached the client rendering overlay and produced a full crash report. The report still showed All The Mods branding:

```text
BetterCompatibilityChecker: Modpack Name: All the Mods 10 | Modpack Version: 6.6
```

Applied cleanup:

| Removed from active pack | Reason |
|---|---|
| `CrashAssistant-neoforge-1.20.6-1.21.4-1.11.6.jar` | User requested removal; it only showed the ATM10 support GUI and did not help with FactorMoon debugging. |
| `better-compatability-checker-neoforge-21.1.8.jar` | This provided the stale `All the Mods 10` / `6.6` modpack branding in crash reports and likely the launch window title. |
| `config/bcc-common.toml`, `config/bcc-common-1.toml.bak`, `config/crash_assistant/` | Moved with the removed mods so stale ATM10 support/config text does not return accidentally. |

Backups are in `_factor_moon_reports/replaced_mod_backups/2026-06-05-remove-atm-crash-branding`.

Actual crash root cause:

```text
Mixin [supplementaries-common.mixins.json:compat.CompatEMFMixin from mod supplementaries] FAILED during APPLY
Invalid descriptor ... Expected (... EMFModelPartRoot; CallbackInfo) but found (... CallbackInfo)
```

`entity_model_features-3.2.4-1.21-neoforge.jar` changed the target descriptor that old `supplementaries-1.21-3.5.33-neoforge.jar` expected for its EMF compatibility mixin.

Applied fix:

| Removed from active mods | Active replacement |
|---|---|
| `supplementaries-1.21-3.5.33-neoforge.jar` | `supplementaries-neoforge-1.21.1-3.6.7.jar` |

Old Supplementaries is backed up in `_factor_moon_reports/replaced_mod_backups/2026-06-05-supplementaries-emf-compat`.

Post-fix static check:

- Installed active jar files: 683
- Duplicate primary mod ids: 0
- Missing required dependencies: 0
- Fabric jars expected through Sinytra Connector: 3

## Fifth launch Omega Config early Architectury fix

The next crash moved to Minecraft client initialization:

```text
Description: Initializing game
java.lang.IllegalStateException: Mod 'architectury' is not available!
...
at dev.architectury.networking.NetworkManager.registerReceiver(...)
at net.minecraft.client.Minecraft.handler$...$omegaconfig$onReturn(...)
```

Root cause:

- `omegaconfig-neoforge-1.5.1.jar` injects `io.github.frqnny.omegaconfig.mixin.ClientMixin` into `Minecraft.<init>`.
- That mixin registers an Architectury networking receiver too early for this NeoForge/Architectury load path.
- `Mo' Structures` also contains a nested `omegaconfig-neoforge-1.5.1.jar`, but the log shows JarJar selecting the external `mods/omegaconfig-neoforge-1.5.1.jar`, so patching the external jar is enough to override the nested copy.

Applied fix:

| Original active jar | Active replacement |
|---|---|
| `omegaconfig-neoforge-1.5.1.jar` | Patched jar with the same active filename. It keeps the `omegaconfig` mod/library classes, fixes the dependency-owner key from `omega-config` to `omegaconfig`, and removes the `[[mixins]] config = "omega-config.mixins.json"` registration. |

Patch candidate is stored as `_factor_moon_reports/replacement_candidates/omegaconfig-neoforge-1.5.1-factormoon-no-client-mixin.jar`; the original jar is backed up in `_factor_moon_reports/replaced_mod_backups/2026-06-05-omegaconfig-early-architectury`.

Post-fix static check:

- Installed active jar files: 683
- Duplicate primary mod ids: 0
- Missing required dependencies: 0
- Fabric jars expected through Sinytra Connector: 3

## Second launch dynamic-lights fix

The next `latest.log` stopped at Java module resolution:

```text
java.lang.module.ResolutionException: Modules lambdynlights_api and sodiumdynamiclights export package dev.lambdaurora.lambdynlights.api to module fabric_message_api_v1
```

Root cause:

- `ars_nouveau-1.21.1-5.11.3.jar` bundles `META-INF/jarjar/lambdynamiclights-api-4.5.1+1.21.1-mojmap.jar`.
- `sodiumdynamiclights-neoforge-1.0.10-1.21.1.jar` also exported the LambDynamicLights API packages.
- `dynamiclights-26.1.2.1NF.jar` was a duplicate dynamic-lights implementation from the wrong `26.1` line.

Applied fix:

| Removed from active mods | Active replacement / result |
|---|---|
| `sodiumdynamiclights-neoforge-1.0.10-1.21.1.jar` | Replaced with patched `sodiumdynamiclights-neoforge-1.0.5-1.21.1-factormoon-no-lambapi.jar`. The base 1.0.5 build is the NeoForge 1.21.1 build whose changelog mentions Ars Nouveau compatibility; the FactorMoon patch removes only `dev/lambdaurora/lambdynlights/api/DynamicLightsInitializer.class` so Ars remains the sole LambDynamicLights API provider. |
| `dynamiclights-26.1.2.1NF.jar` | Moved out as duplicate/wrong-version dynamic-lights provider. |

Backups are in `_factor_moon_reports/replaced_mod_backups/2026-06-05-dynamic-lights-conflict`.

Post-fix checks:

- Active dynamic-light jars: `create-dyn-light-2.3.1-sodium-sable.jar`, `sodiumdynamiclights-neoforge-1.0.5-1.21.1-factormoon-no-lambapi.jar`
- `dev.lambdaurora.lambdynlights.api` provider in active mods: only `ars_nouveau-1.21.1-5.11.3.jar`
- Installed active jar files: 685
- Duplicate primary mod ids: 0
- Missing required dependencies: 0

## Actual first-launch blocker

`FactorMoon/logs/latest.log` stops in NeoForge `ModSorter` before gameplay classes load. The hard blockers are wrong-version mods, not Create itself yet:

| Active jar | Problem |
|---|---|
| `AdvancementPlaques-1.21.11-neoforge-1.7.0.jar` | Built for Minecraft `1.21.11` and NeoForge `21.11.42+`; FactorMoon is `1.21.1` / `21.1.228`. It also asks for newer `Iceberg` and optional newer `Prism`. |
| `BetterF3-17.0.0-NeoForge-1.21.11.jar` | Built for Minecraft `1.21.11`; asks for `cloth_config` `21.11.0+`, while FactorMoon has the correct 1.21.1 line `15.0.140`. |
| `trinkets-4.0.0-beta.2+26.1.jar` | Built for the new `26.1` line, not Minecraft `1.21.1`. Its bundled `yumi_mc_core` also asks for `minecraft [26.1,)` and Java `25+`. |

## Prepared replacement candidates

These candidates were used for the active replacement:

| Candidate file | Source / note |
|---|---|
| `_factor_moon_reports/replacement_candidates/AdvancementPlaques-1.21.1-neoforge-1.6.8.jar` | CurseForge file `5905995`; metadata checks out for Minecraft `1.21.1`, NeoForge `21.1+`, Iceberg `1.2.2+`, Prism `1.0.8+`. |
| `_factor_moon_reports/replacement_candidates/BetterF3-11.0.3-NeoForge-1.21.1.jar` | CurseForge file `5873258`; metadata checks out for Minecraft `1.21+` and Cloth Config `15.0.0+`. |
| `_factor_moon_reports/replacement_candidates/trinkets-3.10.0-fabric-via-connector.jar` | Copied from `cobblemon-extra`; official Trinkets 3.10.0 Fabric for Minecraft `1.21-1.21.1`, likely only usable here through Sinytra Connector + Forgified Fabric API. |

The wrong-version jars are no longer active.

## Create warning double-check

The helper warning is real at the static class-reference level, but likely not the first crash.

| Jar | Static finding | Current judgement |
|---|---|---|
| `Design-n-Decor-1.21.1-2.1.0.jar` | Old Create recipe builder/data generator classes. | References are in datagen classes such as `dev.lopyluna.dndecor.content.datagen...`; likely false positive for normal gameplay. |
| `create_hypertube-0.4.0-COMPAT-NEOFORGE.jar` | Old Create recipe builder params/factory. | References are in `com.pedrorok.hypertube.core.data.HypertubeRecipeGen`; likely false positive for normal gameplay. |
| `create_vibrant_vaults-0.3.2.jar` | Old Create recipe builder/serializer/provider classes. | References are in `net.zlt.create_vibrant_vaults.data...RecipeProvider`; likely false positive for normal gameplay. |
| `amendments-1.21-2.0.15-neoforge.jar` | Old `com.jozufozu.flywheel` classes. | The old Flywheel compat class exists, but `CompatHandler.FLYWHEEL` is compiled to `false`, so this path should not execute. If a later crash mentions `FlywheelCompat` or `com.jozufozu.flywheel`, Amendments needs a patch/disable decision. |

## Validator update

`factor_moon_static_validate.py` now also emits:

- `_factor_moon_reports/validation_first_launch_blockers.csv`
- `_factor_moon_reports/validation_unsupported_dependency_versions.csv`
- `unsupported_dependency_versions` in `_factor_moon_reports/validation_summary.json`

`validation_first_launch_blockers.csv` is currently header-only because the known first-launch blockers have been replaced. `validation_unsupported_dependency_versions.csv` is intentionally broader and can contain noisy version-range guesses.

## Sixth launch Music Notification / NEC crash-loop fix

The latest user-provided log looked like a long loading hang, but `crash-reports` did receive repeated client crash reports:

- `crash-reports/crash-2026-06-05_22.30.01-client.txt`
- `crash-reports/crash-2026-06-05_22.30.02-client.txt`
- `crash-reports/crash-2026-06-05_22.30.03-client.txt`

The first hard crash was a client tick NPE from Music Notification:

```text
java.lang.NullPointerException: Cannot invoke "net.kosmo.music.neoforge.notification.GuiCompactLayer.tick()" because the return value of "net.kosmo.music.neoforge.notification.GuiCompactLayer.getInstance()" is null
    at TRANSFORMER/musicnotification@3.0.0/net.kosmo.music.neoforge.MusicNotificationClientNeoForge.lambda$new$2(MusicNotificationClientNeoForge.java:41)
```

`Not Enough Crashes` then caught the in-game crash repeatedly, producing several near-identical crash reports and making the client appear stuck instead of exiting cleanly.

Applied fix:

| Removed from active pack | Reason |
|---|---|
| `musicnotification-neoforge-3.0.0+mc1.21.1.jar` | Direct source of the client tick NPE. Optional UI-only music notification mod. |
| `notenoughcrashes-neoforge-4.4.9+1.21.1.jar` | Diagnostic mod, not gameplay content; it was recursively handling the same crash and obscuring the root cause. |
| `config/musicnotification.json` | Config for removed Music Notification. |
| `config/notenoughcrashes.json` | Config for removed Not Enough Crashes. |

Backups are in `_factor_moon_reports/replaced_mod_backups/2026-06-05-musicnotification-nec-crash-loop`.

Post-fix static check:

- Installed active jar files: 681
- Duplicate primary mod ids: 0
- Missing required dependencies: 0
- Fabric jars expected through Sinytra Connector: 3

## Sixteenth pass JEI-only recipe browser cleanup

The in-game creative inventory showed overlapping recipe-browser panels: EMI UI was active together with the JEI-side item list. The target baseline for FactorMoon is the `aeronaftics` recipe-browser stack, which uses JEI and JEI integrations.

Comparison:

| Pack | Active recipe-browser stack |
|---|---|
| `aeronaftics` | `jei`, `ae2jeiintegration`, `ftb-jei-extras`, `refinedstorage-jei-integration` |
| FactorMoon before cleanup | JEI stack plus EMI, EMI addons, REI, and EMI-only `extra_mod_integrations` |

Applied cleanup:

| Removed from active pack | Reason |
|---|---|
| `emi-1.1.22+1.21.1+neoforge.jar` | Duplicate recipe/item browser, not in `aeronaftics`. |
| `emi_enchanting-0.1.2+1.21+neoforge.jar` | EMI addon. |
| `emi_loot-0.7.9+1.21+neoforge.jar` | EMI addon. |
| `emixx-neoforge-1.2.3.jar` | EMI addon. |
| `RoughlyEnoughItems-16.0.799-neoforge.jar` | Duplicate recipe/item browser, not in `aeronaftics`. |
| `extra-mod-integrations-all-neoforge-1.0.3+1.21.1.jar` | EMI-only addon with required dependency on `emi`. |
| EMI/REI configs and logs | Stale configs for removed browser stack. |

Backups are in `_factor_moon_reports/replaced_mod_backups/2026-06-06-jei-only-aeronaftics`.

Verification:

- Active recipe-browser jars now match the `aeronaftics` JEI line:
  - `jei-1.21.1-neoforge-19.27.0.340.jar`
  - `ae2jeiintegration-1.2.1.jar`
  - `ftb-jei-extras-21.1.7.jar`
  - `refinedstorage-jei-integration-neoforge-1.0.0.jar`
- Static check after the cleanup:
  - Installed active jar files: 671
  - Duplicate primary mod ids: 0
  - Missing required dependencies: 0
  - Fabric-only active jars: 0

## Fifteenth launch TPSum / Artifacts NaturalSpawner mixin conflict

The 2026-06-06 11:14 world-creation attempt stayed at `0%` for about 20 minutes while RAM and disk were active. `latest.log` showed that this was not normal world generation; a worker thread hit a critical mixin failure during spawn-chunk generation:

```text
Mixin apply for mod artifacts failed mixins.artifacts.common.json:item.NaturalSpawnerMixin
InjectionPoint ... cannot inject into NaturalSpawner::spawnCategoryForPosition(...)
merged by dev.sixik.tpsum.mixin.entity_spawn.MixinNaturalSpawner$redirect_to_optimized_methods
```

Root cause:

- `Artifacts` needs its `NaturalSpawnerMixin` for mimic/artifact spawn behavior.
- `TPSum` had already overwritten the same `NaturalSpawner.spawnCategoryForPosition(...)` method with an entity-spawn optimization.
- The game did not recover to a normal crash screen, leaving the client visually stuck at `0%`.

Applied compatibility fix:

| Change | Reason |
|---|---|
| Stopped the stuck `javaw.exe` process | The fatal mixin error had already happened and the client was not going to recover cleanly. |
| Patched `mods/tpsum-1.21.1-0.0.3.jar` in place | Keeps TPSum installed and preserves its non-spawn optimizations. |
| Removed only `entity_spawn.MixinNaturalSpawner$redirect_to_optimized_methods` and `entity_spawn.MixinSpawnState$optimize_operation` from `tpsum.mixins.json` | Avoids the conflict with `Artifacts` while keeping chunk-generation, biome, block-state, and event-loop optimizations active. |
| Closed the already-open XMCL processes and restored `instance.json` to `minMemory=8192` / `maxMemory=24576` | The open launcher had overwritten the profile back to the old `12288` / `25600` memory values after the game exited. |

Backups are in:

- `_factor_moon_reports/replaced_mod_backups/2026-06-06-tpsum-artifacts-spawn-mixin`
- `_factor_moon_reports/replaced_mod_backups/2026-06-06-memory-settings`

Verification:

- Active `tpsum.mixins.json` contains no `entity_spawn.*` mixins.
- Static check after the patch:
  - Installed active jar files: 677
  - Duplicate primary mod ids: 0
  - Missing required dependencies: 0
  - Fabric-only active jars: 0

## Fourteenth launch Biome Replacer TerraBlender holder fix and memory trim

The 2026-06-06 10:44 world-creation attempt did create a server crash report even though the client did not present a normal crash-report flow:

```text
java.lang.NoSuchMethodError: 'net.minecraft.core.Holder$Reference net.minecraft.core.Registry.getOrThrow(net.minecraft.resources.ResourceKey)'
    at net.werdei.biome_replacer.replacer.TerraBlenderReplacer.modifyPairList(TerraBlenderReplacer.java:20)
```

Root cause:

- Biome Replacer had one remaining TerraBlender path compiled against a newer registry holder lookup.
- On Minecraft `1.21.1`, the holder-returning method with this behavior is `Registry.getHolderOrThrow(ResourceKey)`.

Applied compatibility fix:

| Change | Reason |
|---|---|
| Patched `mods/biomereplacer-2.2.1-pinkeen-neo.jar` in place | Keeps Biome Replacer active while changing only the TerraBlender holder lookup. |
| Rewrote `TerraBlenderReplacer` Registry lookup | `modifyPairList(...)` now calls `Registry.getHolderOrThrow(ResourceKey)`. |
| Adjusted `instance.json` memory from `12288` / `25600` to `8192` / `24576` | Recent crash reports showed Java launching with `-Xms28672M`, reserving nearly all system RAM up front and pushing Windows into heavy virtual-memory pressure. |

Backups are in:

- `_factor_moon_reports/replaced_mod_backups/2026-06-06-biomereplacer-terrablender-holderorthrow`
- `_factor_moon_reports/replaced_mod_backups/2026-06-06-memory-settings`

Verification:

- `javap` confirmed the patched TerraBlender call site now invokes `Registry.getHolderOrThrow(ResourceKey)`.
- Static check after the patch:
  - Installed active jar files: 677
  - Duplicate primary mod ids: 0
  - Missing required dependencies: 0
  - Fabric-only active jars: 0

## Thirteenth launch Biome Replacer Registry holder fix

The 2026-06-06 10:34 world-creation crash report advanced further into Biome Replacer and failed with:

```text
java.lang.NoSuchMethodError: 'java.util.Optional net.minecraft.core.Registry.get(net.minecraft.resources.ResourceKey)'
    at net.werdei.biome_replacer.replacer.VanillaReplacer.getBiomeHolder(VanillaReplacer.java:168)
```

Root cause:

- The patched Biome Replacer was still calling `Registry.get(ResourceKey)` with an `Optional` return.
- In Minecraft `1.21.1`, `Registry.get(ResourceKey)` returns the registry value, not `Optional`.
- The matching holder-returning method for this mod's existing logic is `Registry.getHolder(ResourceKey)`, which returns `Optional<Holder.Reference<T>>`.

Applied compatibility fix:

| Change | Reason |
|---|---|
| Patched `mods/biomereplacer-2.2.1-pinkeen-neo.jar` in place | Keeps Biome Replacer active while changing only the mismatched registry holder lookups. |
| Rewrote `VanillaReplacer` Registry lookup | `getBiomeHolder(...)` now calls `Registry.getHolder(ResourceKey)`. |
| Rewrote `BlueprintReplacer` Registry lookup | `originalSourceMarker(...)` now calls `Registry.getHolder(ResourceKey)`. |

Backups are in `_factor_moon_reports/replaced_mod_backups/2026-06-06-biomereplacer-registry-getholder`.

Verification:

- `javap` confirms both patched call sites now invoke `Registry.getHolder(ResourceKey)`.
- Static check after the patch:
  - Installed active jar files: 677
  - Duplicate primary mod ids: 0
  - Missing required dependencies: 0
  - Fabric-only active jars: 0

## Twelfth launch Replay removal, CPM restore, and Biome Replacer Identifier fix

The 2026-06-06 10:19 world-creation crash report advanced further into Biome Replacer and failed with:

```text
java.lang.NoClassDefFoundError: net/minecraft/resources/Identifier
    at net.werdei.biome_replacer.replacer.VanillaReplacer.getBiomeResourceKey(VanillaReplacer.java:178)
```

Root cause:

- `biomereplacer-2.2.1-pinkeen-neo.jar` still referenced `net.minecraft.resources.Identifier`, which is not present in Minecraft `1.21.1`.
- In Minecraft `1.21.1`, the matching class is `net.minecraft.resources.ResourceLocation`.
- The jar also referenced `ResourceKey.identifier()`, while `1.21.1` exposes `ResourceKey.location()`.

Applied changes:

| Change | Reason |
|---|---|
| Moved `reforgedplaymod-1.21.1-0.3.jar` out of active `mods` | User requested Replay Mod removal. |
| Moved `config/replaymod.json` and `.replay_cache/` out of active pack | Keeps Replay's config/cache from being loaded or reused while preserving files in backup. |
| Removed Replay keybind entries from `options.txt` | Clears inactive Replay controls from the active client options file. |
| Left `replay_recordings/` in place | User recordings are data, not an active mod or config path. |
| Set `config/cpm.json:titleScreenButton=true` | Restores the `Open Skin Editor` title-screen button. |
| Patched `biomereplacer-2.2.1-pinkeen-neo.jar` in place again | Rewrote remaining `Identifier` references to `ResourceLocation` and `ResourceKey.identifier()` to `ResourceKey.location()` in `VanillaReplacer`, `BlueprintReplacer`, and `ModdedBiomeSlicesManagerMixin`. |

Backups are in `_factor_moon_reports/replaced_mod_backups/2026-06-06-remove-replay-restore-cpm`.

Verification:

- Active `mods` contains no `reforgedplaymod` / Replay jar.
- Active `options.txt`, `config`, and `resourcepacks` contain no `replaymod` / `reforgedplay` references.
- `config/cpm.json` has `"titleScreenButton": true`.
- The patched Biome Replacer jar contains no `net/minecraft/resources/Identifier` or `lookupOrThrow` references.
- `javap` confirms `VanillaReplacer` now calls `ResourceLocation.tryParse`, `ResourceKey.create(..., ResourceLocation)`, `TagKey.create(..., ResourceLocation)`, and `ResourceKey.location()`.
- Static check after the patch:
  - Installed active jar files: 677
  - Duplicate primary mod ids: 0
  - Missing required dependencies: 0
  - Fabric-only active jars: 0

## Eleventh launch Biome Replacer 1.21.11 ABI fix

The 2026-06-06 10:04 world-creation crash report was:

```text
Description: mouseClicked event handler
java.lang.NoSuchMethodError: 'net.minecraft.core.Registry net.minecraft.core.RegistryAccess$Frozen.lookupOrThrow(net.minecraft.resources.ResourceKey)'
    at net.minecraft.server.WorldStem.handler$dnh000$biome_replacer$onStemCreated(WorldStem.java:1530)
```

Root cause:

- Active `biomereplacer-2.2.1-pinkeen-neo.jar` was marked for Minecraft `1.21.11`.
- Its `WorldStemMixin` called `RegistryAccess$Frozen.lookupOrThrow(ResourceKey)`, which does not exist in Minecraft `1.21.1`.
- The matching 1.21.1 method is `registryOrThrow(ResourceKey)`.

Applied compatibility fix:

| Change | Reason |
|---|---|
| Patched `mods/biomereplacer-2.2.1-pinkeen-neo.jar` in place | Kept Biome Replacer active and rewrote the single mixin method reference from `lookupOrThrow` to `registryOrThrow`. |
| Updated the jar metadata Minecraft range to `[1.21.1,1.21.2)` | Documents the local compatibility target instead of the original 1.21.11 target. |
| Patched `kubejs/server_scripts/mods/Handcrafted/Recipes.js` | Removed a non-fatal KubeJS recipe-script error by reading `recipe.json.toString()` and guarding unexpected recipe shapes while preserving the intended sheet recipe rebalance. |

Backups are in `_factor_moon_reports/replaced_mod_backups/2026-06-06-biomereplacer-1211-abi`.

Verification:

- `javap` confirms `WorldStemMixin` now invokes `RegistryAccess$Frozen.registryOrThrow(...)`.
- The patched class no longer contains `lookupOrThrow`.
- `node --check` passes for the patched Handcrafted KubeJS script.
- Static check after the patch:
  - Installed active jar files: 678
  - Duplicate primary mod ids: 0
  - Missing required dependencies: 0
  - Fabric-only active jars: 0

## Tenth launch worldgen registry / menu cleanup fix

The 2026-06-06 09:48 crash happened when opening/creating the world list:

```text
Description: mouseClicked event handler
java.lang.IllegalStateException: Failed to load registries due to above errors
```

The root registry errors were:

```text
Unbound values in registry ResourceKey[minecraft:root / minecraft:worldgen/structure]:
[bca:village/dark_mid, bca:village/dark_small, bca:village/default_large,
 bca:village/default_mid, bca:village/default_small, bca:village/fighting_large,
 bca:village/fighting_mid, bca:village/fighting_small, bca:village/witch_hut]
```

and:

```text
Failed to parse cobblemonraiddens:worldgen/biome/raid_den.json
Caused by: Failed to get element ResourceKey[minecraft:sound_event / lumymon:music.raid]
```

Root cause:

- `COBBLEVERSE-DP-v18-CF.zip` expected newer/different BCA structure ids (`default_*`, `dark_*`, `fighting_*`, `witch_hut`), but the active `BCA-Datapack-3.8_CE_norm_M1.21.1_C1.6.1.zip` only provides `bca:village/small`, `bca:village/mid`, and `bca:village/large`.
- The same Cobbleverse datapack referenced LumyMon's `lumymon:music.raid` sound event while LumyMon is not active yet.

Applied fix:

| Change | Reason |
|---|---|
| Patched `datapacks/COBBLEVERSE-DP-v18-CF.zip:data/minecraft/worldgen/structure_set/villages.json` | Replaced missing BCA structure variants with the existing `bca:village/small`, `bca:village/mid`, and `bca:village/large` entries. |
| Patched `datapacks/COBBLEVERSE-DP-v18-CF.zip:data/minecraft/worldgen/structure_set/swamp_huts.json` | Removed the missing `bca:village/witch_hut` entry and kept vanilla `minecraft:swamp_hut`. |
| Patched `datapacks/COBBLEVERSE-DP-v18-CF.zip:data/cobblemonraiddens/worldgen/biome/raid_den.json` | Replaced missing `lumymon:music.raid` with vanilla `minecraft:music.game` until LumyMon is ported. |

Menu cleanup applied in the same pass:

| Change | Reason |
|---|---|
| Moved `fancymenu_neoforge_3.8.1_MC_1.21.1.jar` and `drippyloadingscreen_neoforge_3.1.0_MC_1.21.1.jar` out of active mods | Removes the foreign Cobbleverse/CurseForge/ATM main-menu layouts and extra title-screen mixins. |
| Moved `config/fancymenu/` and `config/drippyloadingscreen/` out of active config | Preserves the old layout assets for reference while restoring a cleaner vanilla-style menu. |
| Set `config/cpm.json:titleScreenButton` to `false` | Removes the `Open Skin Editor` title-screen button. |
| Set `config/create-client.toml:mainMenuConfigButtonRow` to `0` | Removes Create's config button from the main menu. |
| Set Mod Menu `modify_title_screen` to `false` in both active Mod Menu config files | Prevents Mod Menu from replacing/altering the title screen. |

Backups are in `_factor_moon_reports/replaced_mod_backups/2026-06-06-worldgen-menu-cleanup`.

Post-fix checks:

- No active datapack/jar text references remain for the missing `bca:village/default_*`, `bca:village/dark_*`, `bca:village/fighting_*`, `bca:village/witch_hut`, or `lumymon:music.raid` ids.
- Installed active jar files: 678
- Duplicate primary mod ids: 0
- Missing required dependencies: 0
- Fabric jars expected through Sinytra Connector: 3

## Ninth launch Accessories compatibility layer / stale BCC override fix

The 23:07 launch stopped during NeoForge mod loading with two issue messages:

```text
Unknown mod bcc referenced in dependency overrides for mod allthetweaks
```

and:

```text
Incompatible mod loaded: accessories_compat_layer
 - Reason: This mod can cause Curio compatibility issues with other mods
```

Root cause:

- `better-compatability-checker` / `bcc` had already been removed from the active pack, but `config/fml.toml` still forced `allthetweaks` to load after `bcc`.
- `accessories_compat_layer-neoforge-0.1.12+1.21.1.jar` was active together with the real `curios-neoforge-9.5.1+1.21.1.jar`. `kubejstweaks` explicitly rejects that combination because the compatibility layer can break Curios integration.

Applied fix:

| Change | Reason |
|---|---|
| Moved `accessories_compat_layer-neoforge-0.1.12+1.21.1.jar` out of active mods | Compatibility layer is not needed while Curios itself is installed and was the hard loading blocker. |
| Removed `allthetweaks = ["+bcc"]` from `config/fml.toml` | The referenced `bcc` mod is no longer active, so the override produced a stale dependency warning/loading issue. |

Backups are in `_factor_moon_reports/replaced_mod_backups/2026-06-05-accessories-compat-layer-curios-conflict`.

Post-fix static check:

- Installed active jar files: 680
- Duplicate primary mod ids: 0
- Missing required dependencies: 0
- Fabric jars expected through Sinytra Connector: 3

## Eighth launch Moonlight / Supplementaries ABI fix

The 22:57 launch still ended with the same visible recovery crash:

```text
java.lang.IllegalStateException: Missing layer definitions: [legendarymonuments:distortion_portal#main]
```

However, `latest.log` showed why the local Legendary Monuments layer patch did not get a chance to run. NeoForge had already put ModLoader into a broken state during mod construction:

```text
Failed to create mod instance. ModID: supplementaries, class net.mehvahdjukaar.supplementaries.platform.SupplementariesForge
java.lang.NoSuchMethodError: 'java.lang.String net.mehvahdjukaar.moonlight.api.platform.configs.ConfigBuilder.parentCategory()'
```

Root cause:

- Active `supplementaries-neoforge-1.21.1-3.6.7.jar` calls the newer Moonlight `ConfigBuilder.parentCategory()` API.
- Active `moonlight-neoforge-1.21.1-3.0.5.jar` did not contain that method.
- CurseForge lists `moonlight-neoforge-1.21.1-3.0.16.jar` as the current 1.21.1 NeoForge Moonlight file, and local `javap` confirmed that `ConfigBuilder.parentCategory()` exists in 3.0.16.

Applied fix:

| Removed from active pack | Active replacement |
|---|---|
| `moonlight-neoforge-1.21.1-3.0.5.jar` | `moonlight-neoforge-1.21.1-3.0.16.jar` |

Backups are in `_factor_moon_reports/replaced_mod_backups/2026-06-05-moonlight-for-supplementaries-367`.

Post-fix static check:

- Installed active jar files: 681
- Duplicate primary mod ids: 0
- Missing required dependencies: 0
- Fabric jars expected through Sinytra Connector: 3

The log also contains an Aether `skyroot_log` exception while the crash handler was already unwinding. Treat it as secondary for now; if the next launch still crashes on Aether after Music Notification/NEC are gone, Aether should be handled as the next blocker.

## Seventh launch Sound Physics / Legendary Monuments client-resource fix

The 22:42 launch produced a clean crash report at `crash-reports/crash-2026-06-05_22.42.45-client.txt`.

The visible crash report headline was:

```text
Description: Rendering overlay
java.lang.IllegalStateException: Cannot get config value before config is loaded.
    at com.aetherteam.cumulus.client.event.hooks.MenuHooks.trackFallbacks(MenuHooks.java:45)
```

This happened while Minecraft was opening its resource-pack recovery screen, so it was not the first failure. The recovery reason was:

```text
java.lang.IllegalStateException: Missing layer definitions: [legendarymonuments:distortion_portal#main]
```

The earlier log also showed `Sound Physics Remastered` breaking the ModLoader client event state before model-layer events could finish:

```text
java.lang.NullPointerException: Cannot read field "reverbGain" because "com.sonicether.soundphysics.SoundPhysicsMod.CONFIG" is null
    at com.sonicether.soundphysics.config.ReverbParams.globalReverbMultiplier(ReverbParams.java:92)
```

Applied fix:

| Change | Reason |
|---|---|
| Added `factormoon-legendarymonuments-patch-1.0.0.jar` | Small local NeoForge helper mod. It registers `legendarymonuments:distortion_portal#main` during `EntityRenderersEvent.RegisterLayerDefinitions` and calls Legendary Monuments' existing `distortion_portal.getTexturedModelData()` via reflection after Connector remapping. |
| Moved `sound-physics-remastered-neoforge-1.21.1-1.5.1.jar` out of active mods | Optional client audio mod; its null config access put ModLoader into broken state and caused many later client events to be refused. |
| Moved `config/sound_physics_remastered/` out of active config | Config for removed Sound Physics Remastered. |

Patch source and jar:

- `_factor_moon_reports/patch_sources/factormoon_legendarymonuments_patch`
- `_factor_moon_reports/replacement_candidates/factormoon-legendarymonuments-patch-1.0.0.jar`

Backups are in `_factor_moon_reports/replaced_mod_backups/2026-06-05-sound-physics-legendary-layer`.

Post-fix static check:

- Installed active jar files: 681
- Duplicate primary mod ids: 0
- Missing required dependencies: 0
- Fabric jars expected through Sinytra Connector: 3
