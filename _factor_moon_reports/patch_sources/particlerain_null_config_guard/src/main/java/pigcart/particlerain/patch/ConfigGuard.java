package pigcart.particlerain.patch;

import pigcart.particlerain.config.ConfigData;
import pigcart.particlerain.config.ConfigManager;

public final class ConfigGuard {
    private ConfigGuard() {
    }

    public static boolean waterTint() {
        ConfigData config = ConfigManager.config;
        return config != null && config.compat != null && config.compat.waterTint;
    }
}
