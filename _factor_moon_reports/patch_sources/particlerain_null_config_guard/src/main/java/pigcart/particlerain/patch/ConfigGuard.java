package pigcart.particlerain.patch;

import java.util.List;

import pigcart.particlerain.config.ConfigData;
import pigcart.particlerain.config.ConfigManager;

public final class ConfigGuard {
    private ConfigGuard() {
    }

    public static boolean waterTint() {
        ConfigData config = ConfigManager.config;
        return config != null && config.compat != null && config.compat.waterTint;
    }

    public static int getRippleResolution(List<?> spriteContentsList) {
        ConfigData config = ConfigManager.config;
        ConfigData.RippleOptions ripple = config != null && config.ripple != null
            ? config.ripple
            : new ConfigData().ripple;

        if (ripple.useResourcepackResolution && spriteContentsList != null) {
            for (Object sprite : spriteContentsList) {
                try {
                    Object name = sprite.getClass().getMethod("name").invoke(sprite);
                    if ("minecraft:big_smoke_0".equals(String.valueOf(name))) {
                        Object width = sprite.getClass().getMethod("width").invoke(sprite);
                        if (width instanceof Number number) {
                            return Math.min(number.intValue(), 256);
                        }
                    }
                } catch (ReflectiveOperationException ignored) {
                    break;
                }
            }
        }

        if (ripple.resolution < 4) {
            ripple.resolution = 4;
        }
        if (ripple.resolution > 256) {
            ripple.resolution = 256;
        }
        return ripple.resolution;
    }
}
