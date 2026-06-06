# Mandatory NeoForge Ports

Updated: 2026-06-05 15:25

User-confirmed mandatory manual ports from `cobblemon-extra` to FactorMoon NeoForge 1.21.1.

## Done / Installed

| Mod | Installed jar | Status |
|---|---|---|
| Poke Clothing | `FactorMoon/mods/poke-clothing-neoforge-1.1.2-port.1.jar` | Base NeoForge port installed: cloth items, wearable armor, armor materials, tailoring station block/item, assets, tags, safe vanilla recipes. Custom tailoring GUI and `poke-clothing:tailoring` recipes still need the second pass. |

## Still Mandatory

| Mod | Fabric source jar | Port notes |
|---|---|---|
| Cardinal Components API | `cardinal-components-api-6.1.3.jar` | Fabric/Quilt library container with 8 nested modules. Needed mainly because Fight Them All uses entity components. Best NeoForge path is a compatibility layer over NeoForge attachments or a Fight Them All rewrite that replaces CCA usage. |
| Cobblemon: Fight Them All | `cobblemon-fight-them-all-1.0.4-cobblemon-1.7.3.jar` | Kotlin/Fabric mod with Cobblemon battle mixins and CCA entity components. Needs CCA replacement first. |
| Cobblemon Battle Positions | `cobblemon-battle-positions-1.1.3.jar` | Smaller mixin + block port. Depends on Cobblemon and RCT API. |
| CobbleCuisine | `cobblecuisine-2.0.1-1.7-rc1.jar` | Content and food addon with many assets/data files; no mixin file in the original, so likely a registry/config port. |
| Pokeblocks | `pokeblocks-1.4.0-1.21.1.jar` | Large decorative block/entity port with 361 classes, Geckolib dependency, 615 data entries, and 1267 assets. |
| LumyMon | `LumyMon-0.6.3.jar` | Large Cobbleverse system mod with blocks/items, legendary/altar logic, dimensions/features, client code, and mixins. |
| LumyREI | `LumyREI-1.1.2.jar` | REI integration for LumyMon/Cobbleverse recipes. Should be ported after the corresponding content/recipe types exist. |

## Non-Mandatory / Unknown For Later

| Mod | Fabric source jar | Current thought |
|---|---|---|
| Debugify | `Debugify-1.21.1+1.0.jar` | Utility/mixin bugfix mod; likely skip or replace with native NeoForge alternatives after runtime testing. |
| Interactic | `interactic-0.2.3+1.21.jar` | Item interaction/QoL mod; optional unless a gameplay dependency appears. |
| Cozy Home | `Luckys-Cozyhome-Refurnished-1.1.20.jar` | Unknown content mod; inspect later. |
| Resource Pack Options | `respackopts-4.11.3.jar` | Client/resource option utility; likely optional. |
| StackDeobfuscator | `StackDeobfuscatorFabric-1.4.3+08e71cc.jar` | Debug utility; likely optional for normal players. |

## Trinkets

`trinkets-4.0.0-beta.2+26.1.jar` is installed in FactorMoon. Its primary mod id is `trinkets_updated`, and its Fabric metadata provides `trinkets` and `trinkets-updated`; static dependency validation now counts those provided IDs. Its own metadata still declares `minecraft: 26.1.x`, so it needs runtime testing, but it is no longer a pending download item.
