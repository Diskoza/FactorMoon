package com.pcrgaming.obc;

import com.cobblemon.mod.common.api.battles.model.actor.BattleActor;
import com.cobblemon.mod.common.api.item.PokemonSelectingItem;
import com.cobblemon.mod.common.api.pokemon.stats.Stat;
import com.cobblemon.mod.common.api.pokemon.stats.Stats;
import com.cobblemon.mod.common.battles.pokemon.BattlePokemon;
import com.cobblemon.mod.common.item.battle.BagItem;
import com.cobblemon.mod.common.pokemon.Pokemon;
import java.util.List;
import java.util.Set;
import net.minecraft.ChatFormatting;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

@Mod(Obc.MOD_ID)
public final class Obc {
    public static final String MOD_ID = "obc";

    private static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(MOD_ID);
    private static final DeferredRegister<CreativeModeTab> TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MOD_ID);

    public static final DeferredItem<Item> BOTTLE_CAP = ITEMS.register("bottle_cap", () -> new BaseBottleCapItem());
    public static final DeferredItem<Item> BOTTLE_CAP_HP =
            ITEMS.register("bottle_cap_hp", () -> new BottleCapItem(Stats.HP, false));
    public static final DeferredItem<Item> BOTTLE_CAP_ATTACK =
            ITEMS.register("bottle_cap_attack", () -> new BottleCapItem(Stats.ATTACK, false));
    public static final DeferredItem<Item> BOTTLE_CAP_DEFENCE =
            ITEMS.register("bottle_cap_defence", () -> new BottleCapItem(Stats.DEFENCE, false));
    public static final DeferredItem<Item> BOTTLE_CAP_SPECIAL_ATTACK =
            ITEMS.register("bottle_cap_special_attack", () -> new BottleCapItem(Stats.SPECIAL_ATTACK, false));
    public static final DeferredItem<Item> BOTTLE_CAP_SPECIAL_DEFENCE =
            ITEMS.register("bottle_cap_special_defence", () -> new BottleCapItem(Stats.SPECIAL_DEFENCE, false));
    public static final DeferredItem<Item> BOTTLE_CAP_SPEED =
            ITEMS.register("bottle_cap_speed", () -> new BottleCapItem(Stats.SPEED, false));
    public static final DeferredItem<Item> BOTTLE_CAP_GOLD =
            ITEMS.register("bottle_cap_gold", () -> new BottleCapItem(null, false));
    public static final DeferredItem<Item> BOTTLE_CAP_HP_WITHERED =
            ITEMS.register("bottle_cap_hp_withered", () -> new BottleCapItem(Stats.HP, true));
    public static final DeferredItem<Item> BOTTLE_CAP_ATTACK_WITHERED =
            ITEMS.register("bottle_cap_attack_withered", () -> new BottleCapItem(Stats.ATTACK, true));
    public static final DeferredItem<Item> BOTTLE_CAP_DEFENCE_WITHERED =
            ITEMS.register("bottle_cap_defence_withered", () -> new BottleCapItem(Stats.DEFENCE, true));
    public static final DeferredItem<Item> BOTTLE_CAP_SPECIAL_ATTACK_WITHERED =
            ITEMS.register("bottle_cap_special_attack_withered", () -> new BottleCapItem(Stats.SPECIAL_ATTACK, true));
    public static final DeferredItem<Item> BOTTLE_CAP_SPECIAL_DEFENCE_WITHERED =
            ITEMS.register("bottle_cap_special_defence_withered", () -> new BottleCapItem(Stats.SPECIAL_DEFENCE, true));
    public static final DeferredItem<Item> BOTTLE_CAP_SPEED_WITHERED =
            ITEMS.register("bottle_cap_speed_withered", () -> new BottleCapItem(Stats.SPEED, true));
    public static final DeferredItem<Item> BOTTLE_CAP_GOLD_WITHERED =
            ITEMS.register("bottle_cap_gold_withered", () -> new BottleCapItem(null, true));

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> OBC_TAB =
            TABS.register("obc_tab", () -> CreativeModeTab.builder(CreativeModeTab.Row.BOTTOM, 0)
                    .title(Component.translatable("itemGroup.OBC"))
                    .icon(() -> new ItemStack(BOTTLE_CAP_GOLD.get()))
                    .displayItems((parameters, output) -> {
                        output.accept(BOTTLE_CAP.get());
                        output.accept(BOTTLE_CAP_HP.get());
                        output.accept(BOTTLE_CAP_ATTACK.get());
                        output.accept(BOTTLE_CAP_DEFENCE.get());
                        output.accept(BOTTLE_CAP_SPECIAL_ATTACK.get());
                        output.accept(BOTTLE_CAP_SPECIAL_DEFENCE.get());
                        output.accept(BOTTLE_CAP_SPEED.get());
                        output.accept(BOTTLE_CAP_GOLD.get());
                        output.accept(BOTTLE_CAP_HP_WITHERED.get());
                        output.accept(BOTTLE_CAP_ATTACK_WITHERED.get());
                        output.accept(BOTTLE_CAP_DEFENCE_WITHERED.get());
                        output.accept(BOTTLE_CAP_SPECIAL_ATTACK_WITHERED.get());
                        output.accept(BOTTLE_CAP_SPECIAL_DEFENCE_WITHERED.get());
                        output.accept(BOTTLE_CAP_SPEED_WITHERED.get());
                        output.accept(BOTTLE_CAP_GOLD_WITHERED.get());
                    })
                    .build());

    public Obc(IEventBus modBus) {
        ITEMS.register(modBus);
        TABS.register(modBus);
    }

    private static Item.Properties bottleCapProperties() {
        return new Item.Properties().stacksTo(16);
    }

    private static final class BaseBottleCapItem extends Item {
        private BaseBottleCapItem() {
            super(bottleCapProperties());
        }

        @Override
        public Component getName(ItemStack stack) {
            return super.getName(stack).copy().withStyle(ChatFormatting.AQUA, ChatFormatting.ITALIC);
        }

        @Override
        public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
            tooltip.add(Component.translatable("item.obc.bottle_cap_tooltip.1").withStyle(ChatFormatting.GRAY));
            super.appendHoverText(stack, context, tooltip, flag);
        }
    }

    private static final class BottleCapItem extends Item implements PokemonSelectingItem {
        private final Stats stat;
        private final boolean withered;

        private BottleCapItem(Stats stat, boolean withered) {
            super(bottleCapProperties());
            this.stat = stat;
            this.withered = withered;
        }

        @Override
        public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
            ItemStack stack = player.getItemInHand(hand);
            if (player instanceof ServerPlayer serverPlayer) {
                return this.use(serverPlayer, stack);
            }
            return InteractionResultHolder.success(stack);
        }

        @Override
        public Component getName(ItemStack stack) {
            ChatFormatting color = this.statColor();
            return super.getName(stack).copy().withStyle(style -> style.withColor(color).withItalic(this.withered));
        }

        @Override
        public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
            String key = this.stat == null
                    ? "item.obc.bottle_cap_gold" + (this.withered ? "_withered" : "") + "_tooltip.1"
                    : "item.obc.bottle_cap_" + this.stat.name().toLowerCase() + (this.withered ? "_withered" : "") + "_tooltip.1";
            tooltip.add(Component.translatable(key).withStyle(ChatFormatting.GRAY));
            super.appendHoverText(stack, context, tooltip, flag);
        }

        @Override
        public BagItem getBagItem() {
            return null;
        }

        @Override
        public InteractionResultHolder<ItemStack> applyToPokemon(ServerPlayer player, ItemStack stack, Pokemon pokemon) {
            if (pokemon.getEntity() != null && pokemon.getEntity().isBattling()) {
                return InteractionResultHolder.pass(stack);
            }
            if (pokemon.getOwnerPlayer() != player) {
                return InteractionResultHolder.pass(stack);
            }

            boolean changed = this.stat == null ? this.applyToAllStats(pokemon) : this.applyToOneStat(pokemon, this.stat);
            if (!changed) {
                player.displayClientMessage(this.errorMessage(), true);
                return InteractionResultHolder.fail(stack);
            }

            player.displayClientMessage(this.successMessage(), true);
            stack.shrink(1);
            return InteractionResultHolder.consume(stack);
        }

        @Override
        public void applyToBattlePokemon(ServerPlayer player, ItemStack stack, BattlePokemon battlePokemon) {
        }

        @Override
        public InteractionResultHolder<ItemStack> interactWithSpecificBattle(
                ServerPlayer player, ItemStack stack, BattlePokemon battlePokemon) {
            return InteractionResultHolder.fail(stack);
        }

        @Override
        public InteractionResultHolder<ItemStack> interactGeneralBattle(
                ServerPlayer player, ItemStack stack, BattleActor battleActor) {
            return InteractionResultHolder.fail(stack);
        }

        private boolean applyToAllStats(Pokemon pokemon) {
            boolean changed = false;
            Set<Stat> stats = Stats.Companion.getPERMANENT();
            for (Stat stat : stats) {
                changed |= this.applyToOneStat(pokemon, stat);
            }
            return changed;
        }

        private boolean applyToOneStat(Pokemon pokemon, Stat stat) {
            int target = this.withered ? 0 : 31;
            if (pokemon.getIvs().getOrDefault(stat) == target) {
                return false;
            }
            pokemon.setIV(stat, target);
            return true;
        }

        private Component successMessage() {
            if (this.stat == null) {
                return Component.translatable("success.obc.maxed_pokemon" + (this.withered ? "_withered" : "") + ".message")
                        .withStyle(ChatFormatting.GREEN);
            }
            return Component.translatable("success.obc.maxed_" + this.stat.name().toLowerCase() + (this.withered ? "_withered" : "") + ".message")
                    .withStyle(ChatFormatting.GREEN);
        }

        private Component errorMessage() {
            if (this.stat == null) {
                return Component.translatable("error.obc.maxed_pokemon" + (this.withered ? "_withered" : "") + ".message")
                        .withStyle(ChatFormatting.RED);
            }
            return Component.translatable("error.obc.maxed_" + this.stat.name().toLowerCase() + (this.withered ? "_withered" : "") + ".message")
                    .withStyle(ChatFormatting.RED);
        }

        private ChatFormatting statColor() {
            if (this.stat == null) {
                return ChatFormatting.GOLD;
            }
            return switch (this.stat) {
                case HP -> ChatFormatting.GREEN;
                case ATTACK -> ChatFormatting.DARK_RED;
                case DEFENCE -> ChatFormatting.BLUE;
                case SPECIAL_ATTACK -> ChatFormatting.LIGHT_PURPLE;
                case SPECIAL_DEFENCE -> ChatFormatting.YELLOW;
                case SPEED -> ChatFormatting.AQUA;
                default -> ChatFormatting.GOLD;
            };
        }
    }
}
