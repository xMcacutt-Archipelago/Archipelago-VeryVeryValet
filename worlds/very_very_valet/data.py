# Design Spec:
# 50 stars in pool
# Option to deprioritize third star
# Option to require red stars
# Levels are randomized
# Always start with two levels open in each set
# The first level is completely random, the second is a random bonus level
# The next three levels are random
# The final level from each zone is randomized except the final level
# Star requirements are changed to increments of 2 for each level
# Thus requiring 2 stars minimum on each level when solo randomized
# Items are:
# Star
# Power Up Box (optional) filled in with stars otherwise
from dataclasses import dataclass, field
from typing import Optional

Z1 = "Zone 1"
Z1L1 = "Rooftop Parking"
Z1L2 = "Across the Street"
Z1L3 = "Alley Avenue"
Z1L4 = "Cliffside Overlook"
Z1LF = "The Observatory"
Z1LB = "Bowled Over"
Z2 = "Zone 2"
Z2L1 = "Hotel No Vacancy"
Z2L2 = "Quartz Quarry"
Z2L3 = "Up and Down"
Z2L4 = "Overpass Galleria"
Z2LF = "Now Departing"
Z2LB = "Cleanup Crew"
Z3 = "Zone 3"
Z3L1 = "Rinse and Return"
Z3L2 = "Downtown"
Z3L3 = "Macho Motors"
Z3L4 = "Double Parking"
Z3LF = "Seismic Stories"
Z3LB = "Home Sweep Home"
Z4 = "Zone 4"
Z4L1 = "Dueling Venues"
Z4L2 = "The Lot"
Z4L3 = "Sharing Spaces"
Z4L4 = "Chaos Caboose"
Z4LF = "Auto Recall"
Z4LB = "Three In One"
LEVEL = "Level"
BONUS = "Bonus"
FINAL = "Final"
STAR = "Star"
RANDOM_POWER_UP = "Random Power-Up"
GAME_NAME = "Very Very Valet"

@dataclass
class ValetZone:
    zone_name: str
    levels: list[str]
    bonus: str
    final: str
    previous: Optional["ValetZone"] = field(default=None, repr=False)
    next: Optional["ValetZone"] = field(default=None, repr=False)

valet_levels: list[ValetZone] = [
    ValetZone(Z1, [Z1L1, Z1L2, Z1L3, Z1L4], Z1LB, Z1LF),
    ValetZone(Z2, [Z2L1, Z2L2, Z2L3, Z2L4], Z2LB, Z2LF),
    ValetZone(Z3, [Z3L1, Z3L2, Z3L3, Z3L4], Z3LB, Z3LF),
    ValetZone(Z4, [Z4L1, Z4L2, Z4L3, Z4L4], Z4LB, Z4LF)
]

def create_map(shuffled_levels: list[str], shuffled_bonus: list[str], shuffled_final: list[str]):
    zones = [
        ValetZone(
            Z1 if i == 0 else Z2 if i == 1 else Z3 if i == 2 else Z4,
            shuffled_levels[i*4:(i+1)*4],
            shuffled_bonus[i],
            shuffled_final[i] if i < 3 else Z4LF
        )
        for i in range(4)
    ]
    for i in range(len(zones)):
        if i > 0:
            zones[i].previous = zones[i - 1]
        if i < len(zones) - 1:
            zones[i].next = zones[i + 1]
    return zones