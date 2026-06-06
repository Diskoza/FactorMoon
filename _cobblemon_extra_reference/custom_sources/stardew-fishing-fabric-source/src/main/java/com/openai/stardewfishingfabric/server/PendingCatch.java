package com.openai.stardewfishingfabric.server;

import com.cobblemon.mod.common.api.spawning.detail.SpawnAction;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import net.minecraft.world.item.ItemStack;

public record PendingCatch(
    UUID hookId,
    List<ItemStack> rewards,
    SpawnAction<?> spawnAction,
    ItemStack displayStack,
    float topSpeed,
    float upAcceleration,
    float downAcceleration,
    int avgDistance,
    int moveVariation,
    float lineStrength,
    int barSize
) {
    public PendingCatch {
        rewards = new ArrayList<>(rewards);
        displayStack = displayStack.copy();
    }

    public boolean hasPokemon() {
        return spawnAction != null;
    }
}
