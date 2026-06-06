package com.openai.stardewfishingfabric;

import com.openai.stardewfishingfabric.network.CompleteMinigamePayload;
import com.openai.stardewfishingfabric.network.StartMinigamePayload;
import com.openai.stardewfishingfabric.server.MinigameManager;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.networking.v1.PayloadTypeRegistry;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.resources.ResourceLocation;

public final class StardewFishingFabric implements ModInitializer {
    public static final String MOD_ID = "stardew_fishing_fabric";

    public static ResourceLocation id(String path) {
        return ResourceLocation.fromNamespaceAndPath(MOD_ID, path);
    }

    @Override
    public void onInitialize() {
        PayloadTypeRegistry.playS2C().register(StartMinigamePayload.ID, StartMinigamePayload.CODEC);
        PayloadTypeRegistry.playC2S().register(CompleteMinigamePayload.ID, CompleteMinigamePayload.CODEC);

        ServerPlayNetworking.registerGlobalReceiver(CompleteMinigamePayload.ID, (payload, context) ->
            context.server().execute(() -> MinigameManager.complete(context.player(), payload))
        );
    }
}
