# FactorMoon

FactorMoon is a NeoForge 1.21.1 modpack merge draft based on the `aeronaftics` / CreateAERO direction plus a Cobblemon expansion layer.

This repository is meant for analysis and iteration. It tracks configs, KubeJS scripts, datapack/resource-pack metadata, reports, and active mod manifests. Large third-party mod jars, save data, logs, caches, and local backups are intentionally ignored.

## Current Target

- Minecraft: 1.21.1
- NeoForge: 21.1.228
- Pack focus: Create / Create Aeronautics + Cobblemon + AE2
- Recipe browser baseline: JEI stack from `aeronaftics`
- Active jar count after the friend recommendation slim pass: 482
- Balance exclusions: firearms, artillery, Immersive Aircraft, Small Ships, NiftyCarts, Infinite Music

## Important Files

- `FACTOR_MOON_CHANGELOG.md` - human-readable chronology of the merge and fixes.
- `FACTOR_MOON_BUILD_REPORT.md` - current state and repair notes.
- `_factor_moon_reports/create_and_first_launch_audit.md` - detailed launch/crash audit.
- `_factor_moon_reports/friend_recommendation_slim_pass.md` - slimming pass based on the friend's recommendations.
- `ACTIVE_MODS.md` / `ACTIVE_MODS.json` - active jar manifest with sizes and SHA-1 hashes.
- `RESOURCEPACKS.md` / `RESOURCEPACKS.json` - active resource-pack manifest with sizes and SHA-1 hashes.
- `_factor_moon_reports/mandatory_neoforge_ports.md` - manual Fabric-to-NeoForge port queue.

## Not Tracked

The active `mods/*.jar`, `resourcepacks/*`, and local `_disabled_mods/` backups are not committed to Git because the pack includes third-party binaries and large local recovery copies. Rebuild/reconstruction should use the manifests, the reports, and local backups.
