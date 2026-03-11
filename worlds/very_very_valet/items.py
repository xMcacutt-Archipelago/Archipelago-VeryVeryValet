from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from BaseClasses import Item, ItemClassification
from worlds.very_very_valet.data import *

if TYPE_CHECKING:
    from . import VeryVeryValetWorld


class VeryVeryValetItem(Item):
    game: str = GAME_NAME


def create_single(name: str, world, item_class: ItemClassification = ItemClassification.filler):
    world.item_pool.append(VeryVeryValetItem(name, item_class, valet_item_dict[name].code, world.player))


def create_multiple(name: str, amount: int, world, item_class: ItemClassification = ItemClassification.filler):
    for i in range(amount):
        create_single(name, world, item_class)


def create_items(world: VeryVeryValetWorld):
    total_location_count = len(world.multiworld.get_unfilled_locations(world.player))
    create_multiple(STAR, 46, world, valet_item_dict[STAR].classification)
    remaining_locations = total_location_count - len(world.item_pool)
    create_multiple(RANDOM_POWER_UP, remaining_locations, world, valet_item_dict[RANDOM_POWER_UP].classification)
    world.multiworld.itempool += world.item_pool


@dataclass
class ItemData:
    code: Optional[int]
    classification: ItemClassification


valet_item_dict = {
    STAR: ItemData(0x100, ItemClassification.progression_skip_balancing),
    RANDOM_POWER_UP: ItemData(0x101, ItemClassification.filler)
}