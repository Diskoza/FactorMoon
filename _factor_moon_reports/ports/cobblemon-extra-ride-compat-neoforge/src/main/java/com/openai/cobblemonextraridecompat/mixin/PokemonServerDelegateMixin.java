package com.openai.cobblemonextraridecompat.mixin;

import com.cobblemon.mod.common.api.riding.Seat;
import com.cobblemon.mod.common.entity.PoseType;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.entity.pokemon.PokemonServerDelegate;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.cobblemon.mod.common.pokemon.Species;
import net.minecraft.world.phys.Vec3;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

@Mixin(PokemonServerDelegate.class)
public abstract class PokemonServerDelegateMixin {
    private static final int IRON_BOULDER = 1022;
    private static final Vec3 IRON_BOULDER_OFFSET = new Vec3(0.0, 2.1, -0.05);

    @Shadow
    public abstract PokemonEntity getEntity();

    @Redirect(
        method = "positionRider",
        at = @At(
            value = "INVOKE",
            target = "Lcom/cobblemon/mod/common/api/riding/Seat;getOffset(Lcom/cobblemon/mod/common/entity/PoseType;)Lnet/minecraft/world/phys/Vec3;"
        )
    )
    private Vec3 cobblemonExtraRideCompat$overrideSeatOffset(Seat seat, PoseType poseType) {
        PokemonEntity entity = this.getEntity();
        if (entity != null) {
            Pokemon pokemon = entity.getPokemon();
            if (pokemon != null) {
                Species species = pokemon.getSpecies();
                if (species != null && species.getNationalPokedexNumber() == IRON_BOULDER) {
                    return IRON_BOULDER_OFFSET;
                }
            }
        }

        return seat.getOffset(poseType);
    }
}
