from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from .items import ScratchcardHeroItem

from .regions import REGIONS

if TYPE_CHECKING:
    from .world import ScratchcardHeroWorld

class LOCATIONS:
    guyde = "Guyde"
    spacer = "Spacer"
    hawaiian_shirt = "Hawaiian Shirt Guy"
    ghoul = "Gasoline Ghoul"
    hooded = "Hooded Hophead"
    shopkeep = "Shopkeep Diane"
    alchemist = "Alchemist"
    violinist = "Vacant Violinist"
    saphead = "Suspicious Saphead"
    politician = "The People's Politician"
    lena = "Lena Lee"
    manny = "Manny Moe"
    druid = "Dreamy Druid"
    zeb = "Degen Zeb"
    ears = "Ears McGuffin"
    activist = "Anonymous Activist"

class EVENTS:
    map_1_boss = ["Map 1 Boss Defeated", "Map 1 Completed"]
    map_2_boss = ["Map 2 Boss Defeated", "Map 2 Completed"]
    map_3_boss = ["Map 3 Boss Defeated", "Map 3 Completed"]
    endless = []

LOCATION_NAME_TO_ID = {}

def initialize():
    i = 1
    for attr in dir(LOCATIONS):
        if not attr.startswith("__"):
            location = getattr(LOCATIONS, attr)
            LOCATION_NAME_TO_ID[location] = i
            i += 1
    for j in range(0,99):
        k = j+1
        EVENTS.endless[j] = ["Endless Level %d Defeated" % k, "Endless Level %d Completed" % k]


class ScratchcardHeroLocation(Location):
    game = "Scratchcard Hero"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: ScratchcardHeroWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: ScratchcardHeroWorld) -> None:
    map_1 = world.get_region(REGIONS.map_1)
    map_2 = world.get_region(REGIONS.map_2)
    map_3 = world.get_region(REGIONS.map_3)
    endless = world.get_region(REGIONS.endless)

    map_1_locations = get_location_names_with_ids(
        [
            LOCATIONS.activist,
            LOCATIONS.alchemist,
            LOCATIONS.ghoul,
            LOCATIONS.guyde,
            LOCATIONS.hawaiian_shirt,
            LOCATIONS.hooded,
            LOCATIONS.shopkeep,
            LOCATIONS.spacer,
        ]
    )
    map_1.add_locations(map_1_locations, ScratchcardHeroLocation)

    map_2_locations = get_location_names_with_ids(
        [
            LOCATIONS.druid,
            LOCATIONS.lena,
            LOCATIONS.manny,
            LOCATIONS.politician,
            LOCATIONS.saphead,
            LOCATIONS.violinist,
            LOCATIONS.zeb
        ]
    )
    map_2.add_locations(map_2_locations, ScratchcardHeroLocation)

    map_3_locations = get_location_names_with_ids(
        [
          LOCATIONS.ears
        ]
    )
    map_3.add_locations(map_3_locations, ScratchcardHeroLocation)


def create_events(world: ScratchcardHeroWorld) -> None:
    map_1 = world.get_region(REGIONS.map_1)
    map_2 = world.get_region(REGIONS.map_2)
    map_3 = world.get_region(REGIONS.map_3)
    endless = world.get_region(REGIONS.endless)

    map_1.add_event(
        EVENTS.map_1_boss[0], EVENTS.map_1_boss[1], location_type=ScratchcardHeroLocation, item_type=ScratchcardHeroItem
    )
    map_2.add_event(
        EVENTS.map_2_boss[0], EVENTS.map_2_boss[1], location_type=ScratchcardHeroLocation, item_type=ScratchcardHeroItem
    )
    map_3.add_event(
        EVENTS.map_3_boss[0], EVENTS.map_3_boss[1], location_type=ScratchcardHeroLocation, item_type=ScratchcardHeroItem
    )
    for event in EVENTS.endless:
      endless.add_event(
        event[0], event[1], location_type=ScratchcardHeroLocation, item_type=items.ScratchcardHeroItem
      )
