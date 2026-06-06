package ru.factormoon.connectorpatch.fightthemall;

import net.fabricmc.api.ModInitializer;

public final class FightThemAllEntrypoint implements ModInitializer {
    @Override
    public void onInitialize() {
        com.zero_delusions.fight_them_all.core.CobblemonFightThemAll.INSTANCE.onInitialize();
    }
}
