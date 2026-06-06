package com.openai.stardewfishingfabric.mixin;

import com.cobblemon.mod.common.api.spawning.detail.SpawnAction;
import com.cobblemon.mod.common.entity.fishing.PokeRodFishingBobberEntity;
import com.openai.stardewfishingfabric.server.MinigameManager;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.projectile.FishingHook;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(PokeRodFishingBobberEntity.class)
public abstract class PokeRodFishingBobberEntityMixin {
    private PokeRodFishingBobberEntity self() {
        return (PokeRodFishingBobberEntity) (Object) this;
    }

    @Inject(method = "tickFishingLogic", at = @At("HEAD"), cancellable = true)
    private void stardewFishingFabric$pauseCobblemonFishing(BlockPos pos, CallbackInfo ci) {
        if (MinigameManager.hasPending(self())) {
            ci.cancel();
        }
    }

    @Inject(
        method = "retrieve",
        at = @At(
            value = "INVOKE",
            target = "Lcom/cobblemon/mod/common/entity/fishing/PokeRodFishingBobberEntity;spawnPokemonFromFishing(Lnet/minecraft/server/level/ServerPlayer;Lnet/minecraft/world/item/ItemStack;Lcom/cobblemon/mod/common/api/spawning/detail/SpawnAction;)Z"
        ),
        cancellable = true
    )
    private void stardewFishingFabric$startCobblemonPokemonMinigame(ItemStack rodStack, CallbackInfoReturnable<Integer> cir) {
        if (!(((FishingHook) (Object) this).getPlayerOwner() instanceof ServerPlayer player)) {
            return;
        }

        SpawnAction<?> spawnAction = self().getPlannedSpawnAction();
        if (spawnAction == null) {
            return;
        }

        if (MinigameManager.startForPokemon(player, self(), spawnAction, rodStack)) {
            cir.setReturnValue(0);
        }
    }
}
