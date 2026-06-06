package ru.factormoon.legendarypatch;

import java.lang.reflect.Method;
import java.util.function.Supplier;

import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

@Mod(FactorMoonLegendaryMonumentsPatch.MODID)
public final class FactorMoonLegendaryMonumentsPatch {
    public static final String MODID = "factormoon_legendarymonuments_patch";

    private static final ModelLayerLocation DISTORTION_PORTAL_LAYER = new ModelLayerLocation(
            ResourceLocation.fromNamespaceAndPath("legendarymonuments", "distortion_portal"),
            "main");

    public FactorMoonLegendaryMonumentsPatch(IEventBus modBus) {
        modBus.addListener(FactorMoonLegendaryMonumentsPatch::registerLayerDefinitions);
    }

    private static void registerLayerDefinitions(EntityRenderersEvent.RegisterLayerDefinitions event) {
        event.registerLayerDefinition(DISTORTION_PORTAL_LAYER, distortionPortalLayerSupplier());
    }

    private static Supplier<LayerDefinition> distortionPortalLayerSupplier() {
        return () -> {
            try {
                Class<?> modelClass = Class.forName("github.jorgaomc.entities.distortion_portal");
                Method factory = modelClass.getMethod("getTexturedModelData");
                return (LayerDefinition) factory.invoke(null);
            } catch (ReflectiveOperationException e) {
                throw new IllegalStateException("Could not load Legendary Monuments distortion portal model layer", e);
            }
        };
    }
}
