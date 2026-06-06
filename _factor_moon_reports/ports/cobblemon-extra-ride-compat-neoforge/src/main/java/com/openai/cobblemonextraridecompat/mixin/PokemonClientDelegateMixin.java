package com.openai.cobblemonextraridecompat.mixin;

import com.cobblemon.mod.common.api.riding.RidingProperties;
import com.cobblemon.mod.common.api.riding.Seat;
import com.cobblemon.mod.common.client.entity.PokemonClientDelegate;
import com.cobblemon.mod.common.entity.PoseType;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.cobblemon.mod.common.pokemon.Species;
import java.util.List;
import java.util.Set;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.phys.Vec3;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(PokemonClientDelegate.class)
public abstract class PokemonClientDelegateMixin {
    private static final Set<Integer> FALLBACK_SPECIES = Set.of(988, 990, 992, 993, 995, 1005, 1022);
    private static final int ROARING_MOON = 1005;
    private static final int IRON_BOULDER = 1022;
    private static final Vec3 ROARING_MOON_AIR_OFFSET = new Vec3(0.05, 6.7, -0.4);
    private static final Vec3 IRON_BOULDER_OFFSET = new Vec3(0.0, 2.1, -0.05);

    @Shadow
    public abstract PokemonEntity getEntity();

    @Inject(method = "positionRider", at = @At("HEAD"), cancellable = true)
    private void cobblemonExtraRideCompat$positionRiderFallback(
        Entity passenger,
        Entity.MoveFunction positionUpdater,
        CallbackInfo ci
    ) {
        PokemonEntity entity = this.getEntity();
        if (entity == null) {
            return;
        }

        Pokemon pokemon = entity.getPokemon();
        if (pokemon == null) {
            return;
        }

        Species species = pokemon.getSpecies();
        if (species == null || !FALLBACK_SPECIES.contains(species.getNationalPokedexNumber())) {
            return;
        }

        int seatIndex = findSeatIndex(entity.getOccupiedSeats(), passenger);
        if (seatIndex < 0) {
            return;
        }

        RidingProperties rideProperties = entity.getRideProp();
        List<Seat> seats = rideProperties.getSeats();
        if (seatIndex >= seats.size()) {
            return;
        }

        Seat seat = seats.get(seatIndex);
        Vec3 seatOffset = getSeatOffset(entity, species, seat);
        Vec3 rotatedOffset = seatOffset.yRot((float) Math.toRadians(-entity.getYRot()));

        positionUpdater.accept(
            passenger,
            entity.getX() + rotatedOffset.x,
            entity.getY() + rotatedOffset.y,
            entity.getZ() + rotatedOffset.z
        );
        ci.cancel();
    }

    private static int findSeatIndex(Entity[] occupiedSeats, Entity passenger) {
        for (int i = 0; i < occupiedSeats.length; i++) {
            if (occupiedSeats[i] == passenger) {
                return i;
            }
        }

        return -1;
    }

    private static Vec3 getSeatOffset(PokemonEntity entity, Species species, Seat seat) {
        int speciesId = species.getNationalPokedexNumber();
        PoseType poseType = entity.getCurrentPoseType();
        if (speciesId == IRON_BOULDER) {
            return IRON_BOULDER_OFFSET;
        }

        if (speciesId == ROARING_MOON && isRoaringMoonAirborne(entity, poseType)) {
            return ROARING_MOON_AIR_OFFSET;
        }

        return seat.getOffset(poseType);
    }

    private static boolean isRoaringMoonAirborne(PokemonEntity entity, PoseType poseType) {
        return poseType == PoseType.HOVER
            || poseType == PoseType.FLY
            || poseType == PoseType.GLIDE
            || !entity.onGround();
    }
}
