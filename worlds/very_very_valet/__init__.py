from operator import truediv
from typing import Dict, Optional, Any, TextIO

from BaseClasses import Tutorial, MultiWorld, ItemClassification, Item, Location
from worlds.AutoWorld import WebWorld, World
from worlds.very_very_valet.data import *
from worlds.very_very_valet.items import valet_item_dict, create_items, VeryVeryValetItem
from worlds.very_very_valet.locations import valet_location_dict
from worlds.very_very_valet.options import *
from worlds.very_very_valet.regions import create_regions
from worlds.very_very_valet.rules import set_rules


class VeryVeryValetWeb(WebWorld):
    theme = "partyTime"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Very Very Valet randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["xMcacutt"]
    )

    tutorials = [setup_en]
    option_groups = valet_option_groups

class VeryVeryValetWorld(World):
    """
    Up to 4 players must work together to solve the world's severe parking crisis!
    Your puppety crew of valets will redefine what "parking space" means as you drive, boost, and crash your way to victory.
    It's time to buckle up and become a Very Very Valet!
    """
    game = GAME_NAME
    options_dataclass = VeryVeryValetOptions
    options: VeryVeryValetOptions
    topology_present = True
    item_name_to_id = {item_name: item_data.code for item_name, item_data in valet_item_dict.items()}
    location_name_to_id = valet_location_dict

    web = VeryVeryValetWeb()
    ut_can_gen_without_yaml = True

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.level_map: list[ValetZone] = []
        self.item_pool = []

    def generate_early(self):
        normal_levels = [level for zone in valet_levels for level in zone.levels]
        self.random.shuffle(normal_levels)
        bonus_levels = [zone.bonus for zone in valet_levels]
        self.random.shuffle(bonus_levels)
        final_levels = [zone.final for zone in valet_levels if zone.zone_name != Z4]
        self.random.shuffle(final_levels)
        self.level_map = data.create_map(normal_levels, bonus_levels, final_levels)
        pass

    def create_regions(self):
        create_regions(self)

    def create_items(self):
        create_items(self)

    def set_rules(self):
        set_rules(self)
        self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_region(Z4LF, self.player)

    def fill_slot_data(self):
        # from Utils import visualize_regions
        # state = self.multiworld.get_all_state(False)
        # state.update_reachable_regions(self.player)
        # visualize_regions(self.get_region("Menu"), f"{self.player}_world.puml",
        #   show_entrance_names=True, regions_to_highlight=state.reachable_regions[self.player])
        normal_levels = [level for zone in valet_levels for level in zone.levels]
        remapped_normal_levels = [level for zone in self.level_map for level in zone.levels]
        bonus_levels = [zone.bonus for zone in valet_levels]
        remapped_bonus_levels = [zone.bonus for zone in self.level_map]
        final_levels = [zone.final for zone in valet_levels]
        remapped_final_levels = [zone.final for zone in self.level_map]
        level_mapping = { normal_level: remapped_normal_levels[idx] for idx, normal_level in enumerate(normal_levels) }
        bonus_mapping = { bonus_level: remapped_bonus_levels[idx] for idx, bonus_level in enumerate(bonus_levels) }
        final_mapping = { final_level: remapped_final_levels[idx] for idx, final_level in enumerate(final_levels) }
        return {
            "LimitStars": self.options.limit_stars.value,
            "RequireRedStars": self.options.require_red_stars.value,
            "RequireLevelCompletions": self.options.require_level_completions.value,
            "LevelMapping": level_mapping,
            "BonusMapping": bonus_mapping,
            "FinalMapping": final_mapping,
            "DeathLink": self.options.death_link.value
        }

    def handle_ut_yamless(self, slot_data: Optional[dict[str, Any]]) -> Optional[dict[str, Any]]:
        if not slot_data \
                and hasattr(self.multiworld, "re_gen_passthrough") \
                and isinstance(self.multiworld.re_gen_passthrough, dict) \
                and self.game in self.multiworld.re_gen_passthrough:
            slot_data = self.multiworld.re_gen_passthrough[self.game]
        if not slot_data:
            return None
        self.options.require_red_stars.value = slot_data["RequireRedStars"]
        self.options.require_level_completions.value = slot_data["RequireLevelCompletions"]
        self.options.limit_stars.value = slot_data["LimitStars"]
        level_mapping = slot_data["LevelMapping"]
        bonus_mapping = slot_data["BonusMapping"]
        final_mapping = slot_data["FinalMapping"]

        normal_levels = [level for zone in valet_levels for level in zone.levels]
        bonus_levels = [zone.bonus for zone in valet_levels]
        final_levels = [zone.final for zone in valet_levels if zone.zone_name != Z4]

        remapped_normal_levels = [
            level_mapping[level.lower()]
            for level in normal_levels
        ]

        remapped_bonus_levels = [
            bonus_mapping[level.lower()]
            for level in bonus_levels
        ]

        remapped_final_levels = [
            final_mapping[level.lower()]
            for level in final_levels
        ]

        self.level_map = create_map(
            remapped_normal_levels,
            remapped_bonus_levels,
            remapped_final_levels
        )

        return slot_data

    def create_item(self, name: str):
        item_info = valet_item_dict[name]
        return VeryVeryValetItem(name, item_info.classification, item_info.code, self.player)

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        new_hint_data = {}
        for location in self.get_locations():
            origin_zone = location.parent_region.entrances[0].parent_region.name
            new_hint_data[location.address] = f"{origin_zone}"
        hint_data[self.player] = new_hint_data

    def get_filler_item_name(self) -> str:
        return RANDOM_POWER_UP