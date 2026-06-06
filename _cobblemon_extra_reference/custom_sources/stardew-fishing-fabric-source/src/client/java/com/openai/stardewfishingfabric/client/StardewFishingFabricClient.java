package com.openai.stardewfishingfabric.client;

import com.openai.stardewfishingfabric.network.StartMinigamePayload;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;

public final class StardewFishingFabricClient implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        ClientPlayNetworking.registerGlobalReceiver(StartMinigamePayload.ID, (payload, context) ->
            context.client().execute(() -> context.client().setScreen(new FishingMinigameScreen(payload)))
        );
    }
}
