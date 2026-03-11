from __future__ import annotations

from typing import Dict, TYPE_CHECKING

from BaseClasses import Region, Location, Entrance, LocationProgressType
from worlds.very_very_valet.data import *

if TYPE_CHECKING:
    from . import VeryVeryValetWorld


def create_location(world, region: Region, name: str, code: int, progress_type: LocationProgressType = LocationProgressType.DEFAULT):
    location = Location(world.player, name, code, region)
    location.progress_type = progress_type
    region.locations.append(location)


def create_region(world, name: str):
    region = Region(name, world.player, world.multiworld)
    world.multiworld.regions.append(region)
    return region


def connect_regions(world, from_name: str, to_name: str, entrance_name: str):
    from_region = world.get_region(from_name)
    to_region = world.get_region(to_name)
    entrance = from_region.connect(to_region, entrance_name)
    return entrance


def create_regions(world: VeryVeryValetWorld):
    create_region(world, "Menu")

    level_index = 0

    for zone in world.level_map:
        create_region(world, zone.zone_name)
        if zone.zone_name == Z1:
            connect_regions(world, "Menu", zone.zone_name, f"Menu -> {zone.zone_name}")
        else:
            connect_regions(world, zone.previous.final, zone.zone_name, f"{zone.previous.final} -> {zone.zone_name}")
        for level_name in [*zone.levels, zone.bonus, zone.final]:
            level = create_region(world, level_name)
            if level_name != Z4LF:
                for star_index in range(1, 4):
                    star_pluralisation = "Star" if star_index == 1 else "Stars"
                    loc_name = f"{level_name} - {star_index} {star_pluralisation}"
                    progress_type = LocationProgressType.EXCLUDED \
                        if world.options.limit_stars and star_index == 3 else LocationProgressType.PRIORITY
                    create_location(world, level, loc_name, world.location_name_to_id[loc_name], progress_type)
            entrance = connect_regions(world, zone.zone_name, level_name, f"{zone.zone_name} -> {level_name}")
            entrance.access_rule = lambda state, index=level_index: state.has("Star", world.player, index * 2)
            level_index += 1
