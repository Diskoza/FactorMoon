package com.openai.stardewfishingfabric.network;

import com.openai.stardewfishingfabric.StardewFishingFabric;
import com.openai.stardewfishingfabric.server.PendingCatch;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.world.item.ItemStack;

public record StartMinigamePayload(
    int idleTime,
    float topSpeed,
    float upAcceleration,
    float downAcceleration,
    int avgDistance,
    int moveVariation,
    ItemStack displayStack,
    float lineStrength,
    int barSize
) implements CustomPacketPayload {
    public static final CustomPacketPayload.Type<StartMinigamePayload> ID =
        new CustomPacketPayload.Type<>(StardewFishingFabric.id("start_minigame"));

    public static final StreamCodec<RegistryFriendlyByteBuf, StartMinigamePayload> CODEC = StreamCodec.of(
        (buf, payload) -> payload.encode(buf),
        StartMinigamePayload::decode
    );

    public static StartMinigamePayload fromPending(PendingCatch pending) {
        return new StartMinigamePayload(
            18,
            pending.topSpeed(),
            pending.upAcceleration(),
            pending.downAcceleration(),
            pending.avgDistance(),
            pending.moveVariation(),
            pending.displayStack(),
            pending.lineStrength(),
            pending.barSize()
        );
    }

    private static StartMinigamePayload decode(RegistryFriendlyByteBuf buf) {
        return new StartMinigamePayload(
            buf.readVarInt(),
            buf.readFloat(),
            buf.readFloat(),
            buf.readFloat(),
            buf.readVarInt(),
            buf.readVarInt(),
            ItemStack.STREAM_CODEC.decode(buf),
            buf.readFloat(),
            buf.readVarInt()
        );
    }

    private void encode(RegistryFriendlyByteBuf buf) {
        buf.writeVarInt(idleTime);
        buf.writeFloat(topSpeed);
        buf.writeFloat(upAcceleration);
        buf.writeFloat(downAcceleration);
        buf.writeVarInt(avgDistance);
        buf.writeVarInt(moveVariation);
        ItemStack.STREAM_CODEC.encode(buf, displayStack);
        buf.writeFloat(lineStrength);
        buf.writeVarInt(barSize);
    }

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return ID;
    }
}
