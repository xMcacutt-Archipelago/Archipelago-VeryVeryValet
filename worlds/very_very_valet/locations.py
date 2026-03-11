from worlds.very_very_valet import *

def generate_locations():
    loc_dict = {}
    loc_id = 0x100
    for zone in valet_levels:
        for level_name in [*zone.levels, zone.bonus, zone.final]:
            if level_name != Z4LF:
                for star_index in range(1, 4):
                    star_pluralisation = "Star" if star_index == 1 else "Stars"
                    loc_dict[f"{level_name} - {star_index} {star_pluralisation}"]  = loc_id
                    loc_id += 1
    return loc_dict

valet_location_dict = generate_locations()