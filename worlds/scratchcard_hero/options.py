from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle


class MustFindAddonStamps(Toggle):
    """
    Toggling this on locks card addon stamps behind checks (the cards themselves are already behind checks).
    Toggling this off does not restrict the use of cards' addon stamps behind checks.
    """

    display_name = "Must Find Card Addon Stamps"


class MustFindMaps(Toggle):
    """
    Toggling this on locks Maps 2, 3 and Endless Mode behind checks.
    Toggling this off does not restrict access to any Maps or Endless Mode behind checks.
    """

    display_name = "Must Find Maps"


class StartWithFirstMap(Toggle):
    """
    Toggling this on gives you the first map when `Must Find Maps` is toggled on.
    Toggling this off will mean your first map has to be in someone else's game.
    """

    display_name = "Start With First Map"


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

    display_name = "Endless Level Victory"

    range_start = 0
    range_end = 99
    default = 0


class TrapChance(Range):
    """
    Percentage chance that any given Filler item will be replaced by a Trap.
    """

    display_name = "Trap Chance"

    range_start = 0
    range_end = 100
    default = 0


@dataclass
class ScratchcardHeroOptions(PerGameCommonOptions):
    must_find_maps: MustFindMaps
    start_with_first_map: StartWithFirstMap
    map_victory: MapVictory
    endless_victory: EndlessVictory
    trap_chance: TrapChance
    must_find_addon_stamps: MustFindAddonStamps


option_groups = [
    OptionGroup(
        "Gameplay Options",
        [TrapChance, MustFindAddonStamps, MustFindMaps, StartWithFirstMap],
    ),
    OptionGroup(
        "Completion Options",
        [MapVictory, EndlessVictory],
    ),
]


option_presets = {
    "Simple": {
        "must_find_maps": False,
        "start_with_first_map": False,
        "map_victory": 3,
        "endless_victory": 0,
        "trap_chance": 50,
        "must_find_addon_stamps": False,
    },
    "Maps and Addons in Item Pool": {
        "must_find_maps": True,
        "start_with_first_map": True,
        "map_victory": 3,
        "endless_victory": 0,
        "trap_chance": 50,
        "must_find_addon_stamps": True,
    },
    "Endless Level 5 + Maps & Addons in Item Pool": {
        "must_find_maps": True,
        "start_with_first_map": True,
        "map_victory": 3,
        "endless_victory": 5,
        "trap_chance": 50,
        "must_find_addon_stamps": True,
    },
    "All Possible Items in Pool + Endless Level 10": {
        "must_find_maps": True,
        "start_with_first_map": False,
        "map_victory": 3,
        "endless_victory": 10,
        "trap_chance": 50,
        "must_find_addon_stamps": True,
    }
}
