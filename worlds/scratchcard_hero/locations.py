from __future__ import annotations

import json
import os

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from .items import ScratchcardHeroItem

from .regions import REGIONS

if TYPE_CHECKING:
    from .world import ScratchcardHeroWorld

MENU_LOCATIONS = []
MAP_1_LOCATIONS = []
MAP_2_LOCATIONS = []
MAP_3_LOCATIONS = []
GLOBAL_LOCATIONS = []
LOCATION_NAME_TO_ID = {}
LOCATION_NAME_TO_REGION = {}

class EVENTS:
    map_1_boss = ["Map 1 Boss Defeated", "Map 1 Completed"]
    map_2_boss = ["Map 2 Boss Defeated", "Map 2 Completed"]
    map_3_boss = ["Map 3 Boss Defeated", "Map 3 Completed"]
    endless = [None] * 99


def _initialize():
    with open(os.path.join(os.path.dirname(__file__), 'ap_locations.json'), 'r') as file:
        data = json.loads(file.read())
        for location in data:
            l_name = location["name"]
            l_id = location["id"]
            l_region = location["region"]
            match l_region:
                case "Global":
                    GLOBAL_LOCATIONS.append(l_name)
                case REGIONS.menu:
                    MENU_LOCATIONS.append(l_name)
                case REGIONS.map_1:
                    MAP_1_LOCATIONS.append(l_name)
                case REGIONS.map_2:
                    MAP_2_LOCATIONS.append(l_name)
                case REGIONS.map_3:
                    MAP_3_LOCATIONS.append(l_name)
                case REGIONS.endless:
                    ENDLESS_LOCATIONS.append(l_name)
            LOCATION_NAME_TO_ID[l_name] = l_id
            LOCATION_NAME_TO_REGION[l_name] = l_region
    for j in range(0,99):
        k = j+1
        EVENTS.endless[j] = ["Endless Level %d Defeated" % k, "Endless Level %d Completed" % k]


_initialize()


class ScratchcardHeroLocation(Location):
    game = "Scratchcard Hero"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: ScratchcardHeroWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: ScratchcardHeroWorld) -> None:    
    menu = world.get_region(REGIONS.menu)
    map_1 = world.get_region(REGIONS.map_1)
    map_2 = world.get_region(REGIONS.map_2)
    map_3 = world.get_region(REGIONS.map_3)
    endless = world.get_region(REGIONS.endless)

    menu_locations = get_location_names_with_ids(MENU_LOCATIONS)
    menu.add_locations(menu_locations, ScratchcardHeroLocation)

    num_globals = len(GLOBAL_LOCATIONS)
    global_locations_index = 0
    global_locations_num_regions = world.options.map_victory
    if world.options.endless_victory > 0:
        global_locations_num_regions = 4
    global_locations_per_region = int(num_globals / global_locations_num_regions) + 1

    
    map_1_locations = get_location_names_with_ids(MAP_1_LOCATIONS)
    map_1.add_locations(map_1_locations, ScratchcardHeroLocation)
    map_1_global_location_names = []
    for i in range(global_locations_index, min(global_locations_index+global_locations_per_region,num_globals)):
        map_1_global_location_names.append(GLOBAL_LOCATIONS[i])
    map_1_global_locations = get_location_names_with_ids(map_1_global_location_names)
    map_1.add_locations(map_1_global_locations)
    global_locations_index += global_locations_per_region

    if global_locations_num_regions > 1:
        map_2_locations = get_location_names_with_ids(MAP_2_LOCATIONS)
        map_2.add_locations(map_2_locations, ScratchcardHeroLocation)
        map_2_global_location_names = []
        for i in range(global_locations_index, min(global_locations_index+global_locations_per_region,num_globals)):
            map_2_global_location_names.append(GLOBAL_LOCATIONS[i])
        map_2_global_locations = get_location_names_with_ids(map_2_global_location_names)
        map_2.add_locations(map_2_global_locations)
        global_locations_index += global_locations_per_region

    
    if global_locations_num_regions > 2:
        map_3_locations = get_location_names_with_ids(MAP_3_LOCATIONS)
        map_3.add_locations(map_3_locations, ScratchcardHeroLocation)
        map_3_global_location_names = []
        for i in range(global_locations_index, min(global_locations_index+global_locations_per_region,num_globals)):
            map_3_global_location_names.append(GLOBAL_LOCATIONS[i])
        map_3_global_locations = get_location_names_with_ids(map_3_global_location_names)
        map_3.add_locations(map_3_global_locations)
        global_locations_index += global_locations_per_region

    if global_locations_num_regions > 3:
        endless_location_names = []
        for i in range(global_locations_index, num_globals):
            endless_location_names.append(GLOBAL_LOCATIONS[i])
        endless_locations = get_location_names_with_ids(endless_location_names)
        endless.add_locations(endless_locations, ScratchcardHeroLocation)

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
    for i in range(0, world.options.endless_victory):
        event = EVENTS.endless[i]
        endless.add_event(
            event[0], event[1], location_type=ScratchcardHeroLocation, item_type=ScratchcardHeroItem
        )
