package github.dagoncs;

import com.mojang.serialization.MapCodec;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.Mirror;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.DirectionProperty;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

@Mod(PokeClothing.MOD_ID)
public final class PokeClothing {
    public static final String MOD_ID = "poke_clothing";
    public static final String NAMESPACE = "poke-clothing";

    private static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(NAMESPACE);
    private static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(NAMESPACE);
    private static final DeferredRegister<ArmorMaterial> ARMOR_MATERIALS =
            DeferredRegister.create(Registries.ARMOR_MATERIAL, NAMESPACE);
    private static final DeferredRegister<CreativeModeTab> TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, NAMESPACE);

    private static final TagKey<Item> CLOTH_TAG = TagKey.create(Registries.ITEM, id("cloth"));
    private static final List<DeferredItem<Item>> TAB_ITEMS = new ArrayList<>();
    private static final Map<String, DeferredItem<Item>> REGISTERED_ITEMS = new LinkedHashMap<>();

    private static final String[] CLOTH_COLORS = {
            "white", "light_gray", "gray", "black", "brown", "red", "orange", "yellow", "lime", "green", "cyan",
            "light_blue", "blue", "purple", "magenta", "pink"
    };

    public static final DeferredBlock<Block> TAILORING_STATION =
            BLOCKS.register("tailoring_station", () -> new TailoringStationBlock(BlockBehaviour.Properties.of()
                    .strength(2.0F)
                    .sound(SoundType.WOOD)));

    static {
        for (String color : CLOTH_COLORS) {
            registerSimpleItem(color + "_cloth");
        }

        registerArmorSet("kanto_ash", true, true, true, true);
        registerArmorSet("misty", false, true, true, true);
        registerArmorSet("brock", false, true, true, true);
        registerArmorSet("jessie", false, true, true, true);
        registerArmorSet("james", false, true, true, true);
        registerArmorSet("may", true, true, true, true);
        registerArmorSet("emerald_may", true, true, true, true);
        registerArmorSet("dawn", true, true, true, true);
        registerArmorSet("platinum_dawn", false, true, true, true);
        registerArmorSet("brendan", true, true, true, true);
        registerArmorSet("emerald_brendan", true, true, true, true);
        registerArmorSet("red", true, true, true, true);
        registerArmorSet("team_rocket_grunt", true, true, true, true);

        DeferredItem<Item> stationItem = ITEMS.register("tailoring_station", () -> new BlockItem(
                TAILORING_STATION.get(),
                new Item.Properties()
        ));
        REGISTERED_ITEMS.put("tailoring_station", stationItem);
        TAB_ITEMS.add(stationItem);
    }

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> TAB =
            TABS.register("poke_clothing", () -> CreativeModeTab.builder(CreativeModeTab.Row.BOTTOM, 2)
                    .title(Component.translatable("itemGroup.poke-clothing"))
                    .icon(() -> new ItemStack(REGISTERED_ITEMS.get("red_chestplate").get()))
                    .displayItems((parameters, output) -> TAB_ITEMS.forEach(item -> output.accept(item.get())))
                    .build());

    public PokeClothing(IEventBus modBus) {
        BLOCKS.register(modBus);
        ITEMS.register(modBus);
        ARMOR_MATERIALS.register(modBus);
        TABS.register(modBus);
    }

    public static ResourceLocation id(String path) {
        return ResourceLocation.fromNamespaceAndPath(NAMESPACE, path);
    }

    private static DeferredItem<Item> registerSimpleItem(String name) {
        DeferredItem<Item> item = ITEMS.register(name, () -> new Item(new Item.Properties()));
        REGISTERED_ITEMS.put(name, item);
        TAB_ITEMS.add(item);
        return item;
    }

    private static void registerArmorSet(String baseName, boolean helmet, boolean chest, boolean legs, boolean boots) {
        DeferredHolder<ArmorMaterial, ArmorMaterial> material = ARMOR_MATERIALS.register(baseName, () -> armorMaterial(baseName));
        if (helmet) {
            registerArmor(baseName + "_helmet", material, ArmorItem.Type.HELMET);
        }
        if (chest) {
            registerArmor(baseName + "_chestplate", material, ArmorItem.Type.CHESTPLATE);
        }
        if (legs) {
            registerArmor(baseName + "_leggings", material, ArmorItem.Type.LEGGINGS);
        }
        if (boots) {
            registerArmor(baseName + "_boots", material, ArmorItem.Type.BOOTS);
        }
    }

    private static DeferredItem<Item> registerArmor(String name, Holder<ArmorMaterial> material, ArmorItem.Type type) {
        DeferredItem<Item> item = ITEMS.register(name, () -> new ArmorItem(
                material,
                type,
                new Item.Properties().durability(type.getDurability(50))
        ));
        REGISTERED_ITEMS.put(name, item);
        TAB_ITEMS.add(item);
        return item;
    }

    private static ArmorMaterial armorMaterial(String id) {
        Map<ArmorItem.Type, Integer> defense = Map.of(
                ArmorItem.Type.HELMET, 1,
                ArmorItem.Type.CHESTPLATE, 3,
                ArmorItem.Type.LEGGINGS, 2,
                ArmorItem.Type.BOOTS, 1
        );
        return new ArmorMaterial(
                defense,
                15,
                SoundEvents.ARMOR_EQUIP_LEATHER,
                () -> Ingredient.of(CLOTH_TAG),
                List.of(new ArmorMaterial.Layer(id(id))),
                0.0F,
                0.0F
        );
    }

    public static final class TailoringStationBlock extends HorizontalDirectionalBlock {
        public static final DirectionProperty FACING = HorizontalDirectionalBlock.FACING;
        private static final MapCodec<TailoringStationBlock> CODEC = simpleCodec(TailoringStationBlock::new);

        public TailoringStationBlock(BlockBehaviour.Properties properties) {
            super(properties);
            this.registerDefaultState(this.stateDefinition.any().setValue(FACING, net.minecraft.core.Direction.NORTH));
        }

        @Override
        protected MapCodec<? extends HorizontalDirectionalBlock> codec() {
            return CODEC;
        }

        @Override
        public BlockState getStateForPlacement(BlockPlaceContext context) {
            return this.defaultBlockState().setValue(FACING, context.getHorizontalDirection().getOpposite());
        }

        @Override
        protected BlockState rotate(BlockState state, Rotation rotation) {
            return state.setValue(FACING, rotation.rotate(state.getValue(FACING)));
        }

        @Override
        protected BlockState mirror(BlockState state, Mirror mirror) {
            return state.rotate(mirror.getRotation(state.getValue(FACING)));
        }

        @Override
        protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
            builder.add(FACING);
        }
    }
}
