package ru.factormoon.connectorpatch.fightthemall;

import org.ladysnake.cca.api.v3.entity.EntityComponentFactoryRegistry;
import org.ladysnake.cca.api.v3.entity.EntityComponentInitializer;

public final class FightThemAllCardinalEntrypoint implements EntityComponentInitializer {
    @Override
    public void registerEntityComponentFactories(EntityComponentFactoryRegistry registry) {
        com.zero_delusions.fight_them_all.nbt.NbtComponents.INSTANCE.registerEntityComponentFactories(registry);
    }
}
