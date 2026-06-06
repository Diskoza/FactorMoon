package ru.factormoon.connectorpatch.fightthemall;

import net.fabricmc.api.ClientModInitializer;

public final class FightThemAllClientEntrypoint implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        com.zero_delusions.fight_them_all.CobblemonFightThemAllClient.INSTANCE.onInitializeClient();
    }
}
