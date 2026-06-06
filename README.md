# FactorMoon

FactorMoon is a NeoForge 1.21.1 modpack merge draft based on the `aeronaftics` / CreateAERO direction plus a Cobblemon expansion layer.

This repository is meant for analysis and iteration. It tracks configs, KubeJS scripts, datapack/resource-pack metadata, reports, and active mod manifests. Large third-party mod jars, save data, logs, caches, and local backups are intentionally ignored.

## Current Target

- Minecraft: 1.21.1
- NeoForge: 21.1.228
- Recipe browser baseline: JEI stack from `aeronaftics`
- Balance exclusions: firearms, artillery, Immersive Aircraft, Small Ships, NiftyCarts, Infinite Music

## Important Files

- `FACTOR_MOON_CHANGELOG.md` - human-readable chronology of the merge and fixes.
- `FACTOR_MOON_BUILD_REPORT.md` - current state and repair notes.
- `_factor_moon_reports/create_and_first_launch_audit.md` - detailed launch/crash audit.
- `ACTIVE_MODS.md` / `ACTIVE_MODS.json` - active jar manifest with sizes and SHA-1 hashes.
- `RESOURCEPACKS.md` / `RESOURCEPACKS.json` - active resource-pack manifest with sizes and SHA-1 hashes.
- `_factor_moon_reports/mandatory_neoforge_ports.md` - manual Fabric-to-NeoForge port queue.

## Not Tracked

The active `mods/*.jar` and `resourcepacks/*` binary files are not committed to Git because the pack is several gigabytes, includes third-party binaries, and contains files above GitHub's normal file-size limits. Rebuild/reconstruction should use the manifests, the reports, and local backups.
