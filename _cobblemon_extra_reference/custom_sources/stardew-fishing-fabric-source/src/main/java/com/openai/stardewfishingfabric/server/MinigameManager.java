package com.openai.stardewfishingfabric.server;

import com.cobblemon.mod.common.api.spawning.detail.SpawnAction;
import com.cobblemon.mod.common.entity.fishing.PokeRodFishingBobberEntity;
import com.openai.stardewfishingfabric.network.CompleteMinigamePayload;
import com.openai.stardewfishingfabric.network.StartMinigamePayload;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.stats.Stats;
import net.minecraft.tags.ItemTags;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.ExperienceOrb;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.FishingHook;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.phys.Vec3;

public final class MinigameManager {
    private static final Map<UUID, PendingCatch> PENDING = new ConcurrentHashMap<>();

    private MinigameManager() {
    }

    public static boolean hasPending(FishingHook hook) {
        return hook != null && PENDING.containsKey(hook.getUUID());
    }

    public static boolean startForItems(ServerPlayer player, FishingHook hook, List<ItemStack> rewards) {
        if (player == null || hook == null || rewards.isEmpty() || hasPending(hook)) {
            return false;
        }

        ItemStack display = rewards.stream()
            .filter(stack -> stack.is(ItemTags.FISHES))
            .findFirst()
            .orElse(rewards.getFirst())
            .copy();

        PendingCatch pending = new PendingCatch(
            hook.getUUID(),
            rewards,
            null,
            display,
            2.6F,
            0.42F,
            0.32F,
            34,
            16,
            0.15F,
            26
        );
        PENDING.put(hook.getUUID(), pending);
        ServerPlayNetworking.send(player, StartMinigamePayload.fromPending(pending));
        return true;
    }

    public static boolean startForPokemon(ServerPlayer player, PokeRodFishingBobberEntity hook, SpawnAction<?> spawnAction, ItemStack displayStack) {
        if (player == null || hook == null || spawnAction == null || hasPending(hook)) {
            return false;
        }

        PendingCatch pending = new PendingCatch(
            hook.getUUID(),
            List.of(),
            spawnAction,
            displayStack,
            3.1F,
            0.5F,
            0.36F,
            42,
            20,
            0.1F,
            22
        );
        PENDING.put(hook.getUUID(), pending);
        ServerPlayNetworking.send(player, StartMinigamePayload.fromPending(pending));
        return true;
    }

    public static void complete(ServerPlayer player, CompleteMinigamePayload payload) {
        FishingHook hook = player.fishing;
        if (hook == null) {
            return;
        }

        PendingCatch pending = PENDING.remove(hook.getUUID());
        if (pending == null) {
            return;
        }

        damageRod(player);

        if (payload.success()) {
            if (pending.hasPokemon() && hook instanceof PokeRodFishingBobberEntity pokeHook) {
                pokeHook.spawnPokemonFromFishing(player, player.getMainHandItem(), pending.spawnAction());
            } else {
                giveRewards(player, hook, pending.rewards(), payload.accuracy());
            }
        }

        hook.discard();
    }

    private static void damageRod(ServerPlayer player) {
        ItemStack stack = player.getMainHandItem();
        if (stack.isDamageableItem()) {
            stack.hurtAndBreak(1, player, Player.getSlotForHand(player.getUsedItemHand()));
        }
    }

    private static void giveRewards(ServerPlayer player, FishingHook hook, List<ItemStack> rewards, double accuracy) {
        List<ItemStack> copies = new ArrayList<>(rewards.size());
        for (ItemStack reward : rewards) {
            ItemStack copy = reward.copy();
            copies.add(copy);
            if (copy.is(ItemTags.FISHES)) {
                player.awardStat(Stats.FISH_CAUGHT);
            }

            ItemEntity itemEntity = new ItemEntity(player.level(), hook.getX(), hook.getY(), hook.getZ(), copy);
            Vec3 velocity = player.position().subtract(hook.position()).scale(0.1D);
            double lift = Math.sqrt(player.distanceToSqr(hook)) * 0.08D;
            itemEntity.setDeltaMovement(velocity.x, velocity.y * 0.1D + lift, velocity.z);
            player.level().addFreshEntity(itemEntity);
        }

        int xp = Mth.clamp((int) Math.round(1 + accuracy * 6.0D), 1, 7);
        player.level().addFreshEntity(new ExperienceOrb(player.level(), player.getX(), player.getY() + 0.5D, player.getZ() + 0.5D, xp));
    }
}
