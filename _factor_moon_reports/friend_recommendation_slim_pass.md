# Friend Recommendation Slim Pass

Date: 2026-06-06

This pass applies the user's friend's recommendation to stop treating FactorMoon like a full ATM-style mega-pack and refocus it around:

- Create / Create Aeronautics and its required support stack
- Cobblemon and the Cobblemon expansion layer
- AE2 as the main storage/automation backbone
- The existing `aeronaftics` JEI baseline
- A smaller set of worldgen, structure, QoL, and performance mods

## What Changed

- Active mod count went from 671 to 482 jar files.
- Active `mods` size went from about 1.80 GiB to about 0.92 GiB.
- 189 active jar files were moved out of `mods`.
- 385 KubeJS script/data files tied to disabled mod namespaces were moved out of active `kubejs`.
- Backup path: `_disabled_mods/2026-06-06-friend-slim-pass`.

The backup folder is intentionally local-only and ignored by Git, so the repository tracks the active pack state and reports while keeping the removable files available on this machine.

## Major Disabled Areas

- All The Mods leftovers: Allthemodium, AllTheOres, AllTheTweaks, ATM star/progression scripts, ATM recipe overrides.
- Refined Storage stack: Refined Storage, Extra Disks, RS addons, and RS integration scripts.
- Extra tech systems: Mekanism, Modern Industrialization, Industrial Foregoing, Ender IO, Immersive Engineering, Draconic Evolution, Extreme Reactors, Oritech, XyCraft, Hostile Neural Networks, Flux Networks, and dependent addons.
- Logic/network side systems: Integrated Dynamics, RFTools, XNet, and dependent scripts.
- MineColonies stack.
- Extra dimensions beyond the pack's current core direction: Aether, BetterNether, Bumblezone, DeeperDarker, Eternal Starlight, Twilight Forest, Undergarden, Nullscape, and related scripts.
- Large magic/progression systems: Ars Nouveau stack, Iron's Spells, Occultism, Forbidden Arcanus, EvilCraft, Theurgy, Mystical Agriculture, Nature's Aura, Mahou Tsukai, and related recipe/data files.
- Extra food/decor/map/UI layers called out as bloat or duplicates, including Pam's, Aquaculture, Sushi Go Crafting, Stardew Fishing, JourneyMap, Voxy, and related scripts where present.

## Kept Direction

- Create / Create Aeronautics remains the core technical identity.
- AE2 remains active; Refined Storage was removed to avoid a duplicate storage axis.
- JEI remains the recipe browser baseline. Active recipe-browser jars are `jei`, `ae2jeiintegration`, and `ftb-jei-extras`.
- Cobblemon remains active with the currently transferred NeoForge-compatible layer.
- The Fabric `trinkets-3.10.0.jar` remains the only expected Connector-loaded Fabric jar.

## Validation

Post-pass static validation:

- Installed active jar files: 482
- Unique primary mod ids: 479
- Duplicate primary mod ids: 0
- Missing required dependencies: 0
- Fabric-only active jars without Connector support: 0
- Fabric jars expected through Sinytra Connector: 1 (`trinkets-3.10.0.jar`)
- Weapon/artillery suspects: 0
- Unsupported dependency-version warnings: 71

The unsupported dependency-version report is intentionally broad and should be treated as a warning queue, not as a launch blocker by itself.

## Follow-Up Notes

- No new optimization mods were downloaded in this pass. The next launch log should decide whether to add Noisiumed, Ksyxis, ScalableLux, Let Me Despawn, Alternate Current, Distant Horizons, or C2ME.
- Some inactive translation assets under `kubejs/assets/.../lang/ru_ru.json` may still mention removed namespaces. They are passive resource files and were left in place for now to avoid losing the user's translation work.
- The generated plan is `_factor_moon_reports/friend_slim_pass_plan.json`.
- The move manifest is `_factor_moon_reports/friend_slim_pass_moved.json`.
