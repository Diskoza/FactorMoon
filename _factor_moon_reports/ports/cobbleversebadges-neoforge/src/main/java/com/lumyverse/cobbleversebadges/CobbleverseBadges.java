package com.lumyverse.cobbleversebadges;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

@Mod(CobbleverseBadges.MOD_ID)
public final class CobbleverseBadges {
    public static final String MOD_ID = "cobbleversebadges";

    private static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(MOD_ID);
    private static final DeferredRegister<CreativeModeTab> TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MOD_ID);
    private static final List<DeferredItem<Item>> ALL_ITEMS = new ArrayList<>();

    private static final String[] BADGES = {
            "kanto_boulder_badge",
            "kanto_cascade_badge",
            "kanto_thunder_badge",
            "kanto_rainbow_badge",
            "kanto_soul_badge",
            "kanto_marsh_badge",
            "kanto_volcano_badge",
            "kanto_earth_badge",
            "johto_zephyr_badge",
            "johto_hive_badge",
            "johto_plain_badge",
            "johto_fog_badge",
            "johto_storm_badge",
            "johto_mineral_badge",
            "johto_glacier_badge",
            "johto_rising_badge",
            "hoenn_stone_badge",
            "hoenn_knuckle_badge",
            "hoenn_dynamo_badge",
            "hoenn_heat_badge",
            "hoenn_balance_badge",
            "hoenn_feather_badge",
            "hoenn_mind_badge",
            "hoenn_rain_badge",
            "sinnoh_coal_badge",
            "sinnoh_forest_badge",
            "sinnoh_cobble_badge",
            "sinnoh_fen_badge",
            "sinnoh_relic_badge",
            "sinnoh_mine_badge",
            "sinnoh_icicle_badge",
            "sinnoh_beacon_badge",
    };

    private static final String[] TROPHIES_AND_BOXES = {
            "kanto_league_trophy",
            "johto_league_trophy",
            "hoenn_league_trophy",
            "sinnoh_league_trophy",
            "kanto_badge_box",
            "johto_badge_box",
            "hoenn_badge_box",
            "sinnoh_badge_box",
    };

    private static DeferredItem<Item> iconItem;

    static {
        for (String id : BADGES) {
            register(id, Rarity.EPIC);
        }
        for (String id : TROPHIES_AND_BOXES) {
            DeferredItem<Item> item = register(id, Rarity.RARE);
            if ("sinnoh_league_trophy".equals(id)) {
                iconItem = item;
            }
        }
    }

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> GYM_BADGES_GROUP =
            TABS.register("gym_badges", () -> CreativeModeTab.builder(CreativeModeTab.Row.BOTTOM, 1)
                    .title(Component.translatable("itemgroup.cobbleversebadges.badges_and_trophies"))
                    .icon(() -> new ItemStack(iconItem.get()))
                    .displayItems((parameters, output) -> ALL_ITEMS.forEach(item -> output.accept(item.get())))
                    .build());

    public CobbleverseBadges(IEventBus modBus) {
        ITEMS.register(modBus);
        TABS.register(modBus);
    }

    private static DeferredItem<Item> register(String id, Rarity rarity) {
        DeferredItem<Item> item = ITEMS.register(id, () -> new Item(new Item.Properties()
                .rarity(rarity)
                .fireResistant()
                .stacksTo(1)));
        ALL_ITEMS.add(item);
        return item;
    }
}
