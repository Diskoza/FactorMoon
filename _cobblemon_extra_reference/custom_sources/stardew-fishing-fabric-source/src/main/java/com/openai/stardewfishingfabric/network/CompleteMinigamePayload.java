package com.openai.stardewfishingfabric.network;

import com.openai.stardewfishingfabric.StardewFishingFabric;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;

public record CompleteMinigamePayload(boolean success, double accuracy) implements CustomPacketPayload {
    public static final CustomPacketPayload.Type<CompleteMinigamePayload> ID =
        new CustomPacketPayload.Type<>(StardewFishingFabric.id("complete_minigame"));

    public static final StreamCodec<ByteBuf, CompleteMinigamePayload> CODEC = StreamCodec.composite(
        ByteBufCodecs.BOOL,
        CompleteMinigamePayload::success,
        ByteBufCodecs.DOUBLE,
        CompleteMinigamePayload::accuracy,
        CompleteMinigamePayload::new
    );

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return ID;
    }
}
