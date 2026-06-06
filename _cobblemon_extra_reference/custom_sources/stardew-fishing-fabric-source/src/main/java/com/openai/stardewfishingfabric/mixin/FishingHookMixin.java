package com.openai.stardewfishingfabric.mixin;

import com.openai.stardewfishingfabric.server.MinigameManager;
import java.util.Collection;
import java.util.Collections;
import net.minecraft.advancements.CriteriaTriggers;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.stats.Stats;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.ExperienceOrb;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.FishingHook;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.storage.loot.BuiltInLootTables;
import net.minecraft.world.level.storage.loot.LootParams;
import net.minecraft.world.level.storage.loot.LootTable;
import net.minecraft.world.level.storage.loot.parameters.LootContextParamSets;
import net.minecraft.world.level.storage.loot.parameters.LootContextParams;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Overwrite;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(FishingHook.class)
public abstract class FishingHookMixin {
    @Shadow private Entity hookedIn;
    @Shadow private int nibble;
    @Shadow private int luck;
    @Shadow public abstract Player getPlayerOwner();
    @Shadow protected abstract void pullEntity(Entity entity);
    @Shadow protected abstract boolean shouldStopFishing(Player player);

    private FishingHook self() {
        return (FishingHook) (Object) this;
    }

    @Inject(method = "catchingFish", at = @At("HEAD"), cancellable = true)
    private void stardewFishingFabric$pauseVanillaFishing(BlockPos pos, CallbackInfo ci) {
        if (MinigameManager.hasPending(self())) {
            ci.cancel();
        }
    }

    /**
     * @author OpenAI
     * @reason Replace fragile local-capture injection with a stable implementation for 1.21.1.
     */
    @Overwrite
    public int retrieve(ItemStack itemStack) {
        Player player = this.getPlayerOwner();
        if (self().level().isClientSide || player == null || this.shouldStopFishing(player)) {
            return 0;
        }

        int result = 0;
        if (this.hookedIn != null) {
            this.pullEntity(this.hookedIn);
            CriteriaTriggers.FISHING_ROD_HOOKED.trigger((ServerPlayer) player, itemStack, self(), Collections.emptyList());
            self().level().broadcastEntityEvent(self(), (byte) 31);
            result = this.hookedIn instanceof ItemEntity ? 3 : 5;
        } else if (this.nibble > 0) {
            LootParams lootParams = new LootParams.Builder((ServerLevel) self().level())
                .withParameter(LootContextParams.ORIGIN, self().position())
                .withParameter(LootContextParams.TOOL, itemStack)
                .withParameter(LootContextParams.THIS_ENTITY, self())
                .withLuck((float) this.luck + player.getLuck())
                .create(LootContextParamSets.FISHING);
            LootTable lootTable = self().level().getServer().reloadableRegistries().getLootTable(BuiltInLootTables.FISHING);
            var list = lootTable.getRandomItems(lootParams);

            if (list.stream().anyMatch(stack -> stack.is(ItemTags.FISHES))
                && MinigameManager.startForItems((ServerPlayer) player, self(), list)) {
                return 0;
            }

            CriteriaTriggers.FISHING_ROD_HOOKED.trigger((ServerPlayer) player, itemStack, self(), (Collection<ItemStack>) list);
            for (ItemStack caught : list) {
                ItemEntity itemEntity = new ItemEntity(self().level(), self().getX(), self().getY(), self().getZ(), caught);
                double d = player.getX() - self().getX();
                double e = player.getY() - self().getY();
                double f = player.getZ() - self().getZ();
                itemEntity.setDeltaMovement(d * 0.1, e * 0.1 + Math.sqrt(Math.sqrt(d * d + e * e + f * f)) * 0.08, f * 0.1);
                self().level().addFreshEntity(itemEntity);
                player.level().addFreshEntity(new ExperienceOrb(player.level(), player.getX(), player.getY() + 0.5, player.getZ() + 0.5, self().getRandom().nextInt(6) + 1));
                if (caught.is(ItemTags.FISHES)) {
                    player.awardStat(Stats.FISH_CAUGHT, 1);
                }
            }
            result = 1;
        }

        if (self().onGround()) {
            result = 2;
        }

        self().discard();
        return result;
    }
}
