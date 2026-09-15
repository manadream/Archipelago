from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle


class MustFindMaps(Toggle):
    """
    Toggling this on locks Maps 2, 3 and Endless Mode behind checks.
    Toggling this off does not restrict access to any Maps or Endless Mode behind checks.
    """

    display_name = "Must Find Maps"


class MapVictory(Range):
    """
    Number of Maps that must be completed to win the game.
    Setting `Endless Level Victory` to anything other than 0 overrides this setting.
    """

    display_name = "Maps Completed To Win"

    range_start = 1
    range_end = 3
    default = 3


class EndlessVictory(Range):
    """
    Number of Levels of Endless Mode that must be completed to win the game.
    Setting this to 0 disables Endless Mode and uses the Maps Completed To Win setting for Victory.
    """

    display_name = "Map Level Victory"

    range_start = 0
    range_end = 99
    default = 0


@dataclass
class ScratchcardHeroOptions(PerGameCommonOptions):
    must_find_maps: MustFindMaps
    map_victory: MapVictory
    endless_victory: EndlessVictory


option_groups = [
    OptionGroup(
        "Gameplay Options",
        [MustFindMaps],
    ),
    OptionGroup(
        "Completion Options",
        [MapVictory, EndlessVictory],
    ),
]


option_presets = {
    "Standard": {
        "must_find_maps": False,
        "map_victory": 3,
        "endless_victory": 0
    },
    "Standard + Maps as checks": {
        "must_find_maps": True,
        "map_victory": 3,
        "endless_victory": 0
    },
    "Endless Level 5 + Maps as checks": {
        "must_find_maps": True,
        "map_victory": 3,
        "endless_victory": 5
    },
}
