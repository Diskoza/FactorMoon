package com.openai.stardewfishingfabric.client;

import com.openai.stardewfishingfabric.network.CompleteMinigamePayload;
import com.openai.stardewfishingfabric.network.StartMinigamePayload;
import java.util.Random;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;

public final class FishingMinigameScreen extends Screen {
    private static final ResourceLocation OVERWORLD_TEXTURE = ResourceLocation.fromNamespaceAndPath(
        "stardew_fishing_fabric",
        "textures/gui/minigame_backgrounds/minecraft/overworld.png"
    );
    private static final ResourceLocation NETHER_TEXTURE = ResourceLocation.fromNamespaceAndPath(
        "stardew_fishing_fabric",
        "textures/gui/minigame_backgrounds/minecraft/the_nether.png"
    );
    private final StartMinigamePayload payload;
    private final Component title = Component.literal("Fishing");
    private final Random random = new Random();
    private double bobberPos;
    private double bobberVelocity;
    private double fishPos;
    private double fishVelocity;
    private int fishTarget = -1;
    private int fishIdleTicks;
    private boolean fishIdle;
    private boolean inputDown;
    private float progress = 0.38F;
    private int successTicks;
    private int totalTicks;
    private int resultTicks = -1;
    private boolean success;
    private boolean submitted;

    public FishingMinigameScreen(StartMinigamePayload payload) {
        super(Component.literal("Fishing"));
        this.payload = payload;
    }

    @Override
    protected void init() {
        this.bobberPos = 58.0D;
        this.fishPos = 70.0D;
    }

    @Override
    public void tick() {
        if (resultTicks >= 0) {
            if (--resultTicks == 0) {
                onClose();
            }
            return;
        }

        if (inputDown) {
            if (bobberVelocity < 0.0D) {
                bobberVelocity *= 0.9D;
            }
            bobberVelocity += 0.7D;
        } else if (bobberPos > 0.0D) {
            bobberVelocity -= 0.7D;
        }

        bobberPos += bobberVelocity;
        if (bobberPos > 142 - payload.barSize()) {
            bobberPos = 142 - payload.barSize();
            bobberVelocity = 0.0D;
        } else if (bobberPos < 0.0D) {
            bobberPos = 0.0D;
            bobberVelocity = bobberVelocity < -1.4D ? bobberVelocity * -0.4D : 0.0D;
        }

        if (fishTarget < 0 || shouldPickTarget()) {
            fishTarget = nextFishTarget();
            fishIdle = false;
            fishIdleTicks = 0;
        }

        if (fishIdle) {
            fishIdleTicks++;
            if (Math.abs(fishVelocity) > 0.0D) {
                boolean movingUp = fishVelocity > 0.0D;
                fishVelocity -= (movingUp ? payload.upAcceleration() : payload.downAcceleration()) * Math.signum(fishVelocity);
                if ((movingUp && fishVelocity < 0.0D) || (!movingUp && fishVelocity > 0.0D)) {
                    fishVelocity = 0.0D;
                }
            }
        } else {
            double distance = fishTarget - fishPos;
            double acceleration = (distance > 0.0D ? payload.upAcceleration() : payload.downAcceleration()) * Math.signum(distance);
            fishVelocity = Mth.clamp(fishVelocity + acceleration, -payload.topSpeed(), payload.topSpeed());
        }

        fishPos += fishVelocity;
        if (Math.abs(fishTarget - fishPos) < Math.max(1.0D, Math.abs(fishVelocity))) {
            fishIdle = true;
        }

        if (fishPos < 0.0D) {
            fishPos = 0.0D;
            fishVelocity = 0.0D;
            fishIdle = true;
        } else if (fishPos > 127.0D) {
            fishPos = 127.0D;
            fishVelocity = 0.0D;
            fishIdle = true;
        }

        int min = Mth.floor(bobberPos) - 2;
        int max = Mth.ceil(bobberPos) + payload.barSize() - 12;
        boolean onFish = fishPos >= min && fishPos <= max;
        totalTicks++;
        if (onFish) {
            successTicks++;
            progress = Math.min(1.0F, progress + 1.0F / 80.0F);
        } else {
            progress = Math.max(0.0F, progress - Math.max(0.0018F, (1.0F - payload.lineStrength()) / 240.0F));
        }

        if (progress <= 0.0F) {
            finish(false);
        } else if (progress >= 1.0F) {
            finish(true);
        }
    }

    private boolean shouldPickTarget() {
        if (payload.idleTime() <= 0) {
            return true;
        }

        int variation = Math.max(1, fishIdleTicks / 2);
        return fishIdleTicks >= payload.idleTime() - variation && this.minecraft != null && this.minecraft.level != null
            ? this.minecraft.level.random.nextFloat() <= 1.0F / variation
            : false;
    }

    private int nextFishTarget() {
        int shortest = Math.max(10, payload.avgDistance() - payload.moveVariation());
        int longest = Math.min(127, payload.avgDistance() + payload.moveVariation());
        boolean canGoDown = (int) fishPos - shortest >= 0;
        boolean canGoUp = (int) fishPos + shortest <= 127;
        boolean goUp = canGoUp && (!canGoDown || this.random.nextBoolean());
        int distance = shortest + this.random.nextInt(Math.max(1, longest - shortest + 1));
        return Mth.clamp((int) fishPos + distance * (goUp ? 1 : -1), 0, 127);
    }

    private void finish(boolean success) {
        this.success = success;
        this.resultTicks = 20;
    }

    @Override
    public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        renderBackground(graphics, mouseX, mouseY, partialTick);

        ResourceLocation texture = getMinigameTexture();
        int leftPos = (width - 38) / 2;
        int topPos = (height - 152) / 2;
        graphics.blit(texture, leftPos, topPos, 0, 0, 38, 152, 256, 256);
        graphics.renderItem(payload.displayStack(), leftPos + 45, topPos + 8);

        int barBottom = topPos + 142 - (int) bobberPos;
        int bobberTop = topPos + 4 - payload.barSize() + (142 - (int) bobberPos);
        graphics.blit(texture, leftPos + 18, bobberTop, 38, 0, 9, 2, 256, 256);
        for (int i = 0; i < Math.max(0, payload.barSize() - 4); i++) {
            graphics.blit(texture, leftPos + 18, bobberTop + 2 + i, 38, 2, 9, 1, 256, 256);
        }
        graphics.blit(texture, leftPos + 18, barBottom - 2, 38, 3, 9, 2, 256, 256);

        int fishY = topPos + 130 - (int) fishPos;
        graphics.blit(texture, leftPos + 14, fishY, 55, 0, 16, 15, 256, 256);

        int progressHeight = (int) (progress * 145.0F);
        int progressColor = Mth.hsvToRgb(progress / 3.0F, 1.0F, 1.0F) | 0xFF000000;
        graphics.fill(leftPos + 33, topPos + 148, leftPos + 37, topPos + 148 - progressHeight, progressColor);
        graphics.blit(texture, leftPos + 5, topPos + 129, 47, 0, 8, 3, 256, 256);

        String help = resultTicks >= 0
            ? (success ? "Success!" : "Missed!")
            : "Hold LMB or SPACE";
        graphics.drawCenteredString(font, title, width / 2, topPos - 14, 0xF7D66B);
        graphics.drawCenteredString(font, Component.literal(help), width / 2, topPos + 160, success ? 0x9CFF9C : 0xF3E7C0);
    }

    private ResourceLocation getMinigameTexture() {
        Minecraft client = this.minecraft;
        if (client != null && client.level != null && "the_nether".equals(client.level.dimension().location().getPath())) {
            return NETHER_TEXTURE;
        }
        return OVERWORLD_TEXTURE;
    }

    @Override
    public boolean mouseClicked(double mouseX, double mouseY, int button) {
        if (button == 0 && resultTicks < 0) {
            inputDown = true;
            return true;
        }
        return super.mouseClicked(mouseX, mouseY, button);
    }

    @Override
    public boolean mouseReleased(double mouseX, double mouseY, int button) {
        if (button == 0) {
            inputDown = false;
            return true;
        }
        return super.mouseReleased(mouseX, mouseY, button);
    }

    @Override
    public boolean keyPressed(int keyCode, int scanCode, int modifiers) {
        if (keyCode == 32 && resultTicks < 0) {
            inputDown = true;
            return true;
        }
        return super.keyPressed(keyCode, scanCode, modifiers);
    }

    @Override
    public boolean keyReleased(int keyCode, int scanCode, int modifiers) {
        if (keyCode == 32) {
            inputDown = false;
            return true;
        }
        return super.keyReleased(keyCode, scanCode, modifiers);
    }

    @Override
    public void onClose() {
        if (!submitted) {
            submitted = true;
            double accuracy = totalTicks == 0 ? 0.0D : (double) successTicks / (double) totalTicks;
            ClientPlayNetworking.send(new CompleteMinigamePayload(success, accuracy));
        }
        super.onClose();
    }

    @Override
    public boolean shouldCloseOnEsc() {
        return true;
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }
}
