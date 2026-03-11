from dataclasses import dataclass

from Options import Choice, Range, Toggle, DeathLink, DefaultOnToggle, OptionGroup, PerGameCommonOptions


class LimitStars(DefaultOnToggle):
    """
    Prevents required items from being placed on the third star check of each level.
    """
    display_name = "Limit Stars"


class RequireRedStars(Toggle):
    """
    Determines if red stars (hard mode) are required for checks to send.
    """
    display_name = "Require Red Stars"


class RequireLevelCompletions(Toggle):
    """
    Determines if all levels in each zone must be completed to unlock the final level of the zone.
    """
    display_name = "Require Level Completions"


valet_option_groups = [
    OptionGroup("General", [
        LimitStars,
        RequireRedStars,
        RequireLevelCompletions,
        DeathLink
    ])
]

@dataclass
class VeryVeryValetOptions(PerGameCommonOptions):
    limit_stars: LimitStars
    require_red_stars: RequireRedStars
    require_level_completions: RequireLevelCompletions
    death_link: DeathLink