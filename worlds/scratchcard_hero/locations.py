from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from .items import ScratchcardHeroItem, ITEMS, CARD_ADDONS

from .regions import REGIONS

if TYPE_CHECKING:
    from .world import ScratchcardHeroWorld

class LOCATIONS:
    menu = "Menu"
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
    map_1_nodes = []
    map_2_nodes = []
    map_3_nodes = []
    shop_locations = []

class EVENTS:
    map_1_boss = ["Map 1 Boss Defeated", "Map 1 Completed"]
    map_2_boss = ["Map 2 Boss Defeated", "Map 2 Completed"]
    map_3_boss = ["Map 3 Boss Defeated", "Map 3 Completed"]
    endless = [None] * 99

LOCATION_NAME_TO_ID = {}

def _initialize():
  num_map_1_nodes = 15
  num_map_2_nodes = 16
  num_map_3_nodes = 19
  for n in range(0,num_map_1_nodes):
      LOCATIONS.map_1_nodes.append("Map 1 Node %d" % (n+1))
  for n in range(0,num_map_2_nodes):
      LOCATIONS.map_2_nodes.append("Map 2 Node %d" % (n+1))
  for n in range(0,num_map_3_nodes):
      LOCATIONS.map_3_nodes.append("Map 3 Node %d" % (n+1))
  for attr in dir(LOCATIONS):
      if not attr.startswith("__"):
          location = getattr(LOCATIONS, attr)
          if isinstance(location, list):
              for loc in location:
                  LOCATION_NAME_TO_ID[loc] = len(LOCATION_NAME_TO_ID) + 1
          else:
              LOCATION_NAME_TO_ID[location] = len(LOCATION_NAME_TO_ID) + 1
  num_shop_locations = 10 + len(ITEMS) + len(CARD_ADDONS) - len(LOCATION_NAME_TO_ID)
  for i in range(1,num_shop_locations):
      name = "Shop Item %d" % i
      LOCATIONS.shop_locations.append(name)
      LOCATION_NAME_TO_ID[name] = len(LOCATION_NAME_TO_ID) + 1
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

    menu_locations = get_location_names_with_ids(["Menu"])
    menu.add_locations(menu_locations, ScratchcardHeroLocation)

    shop_locations_index = 0
    shop_locations_num_regions = 3
    if world.options.endless_victory > 0:
        shop_locations_num_regions = 4
    shop_locations_per_region = int(len(LOCATIONS.shop_locations) / shop_locations_num_regions)

    map_1_location_names = [
        LOCATIONS.activist,
        LOCATIONS.alchemist,
        LOCATIONS.ghoul,
        LOCATIONS.guyde,
        LOCATIONS.hawaiian_shirt,
        LOCATIONS.hooded,
        LOCATIONS.shopkeep,
        LOCATIONS.spacer,
    ]
    map_1_location_names += LOCATIONS.map_1_nodes
    for i in range(shop_locations_index,shop_locations_index+shop_locations_per_region):
        map_1_location_names.append(LOCATIONS.shop_locations[i])
    shop_locations_index += shop_locations_per_region
    map_1_locations = get_location_names_with_ids(map_1_location_names)
    map_1.add_locations(map_1_locations, ScratchcardHeroLocation)

    map_2_location_names = [
        LOCATIONS.druid,
        LOCATIONS.lena,
        LOCATIONS.manny,
        LOCATIONS.politician,
        LOCATIONS.saphead,
        LOCATIONS.violinist,
        LOCATIONS.zeb
    ]
    map_2_location_names += LOCATIONS.map_2_nodes
    for i in range(shop_locations_index,shop_locations_index+shop_locations_per_region):
        map_2_location_names.append(LOCATIONS.shop_locations[i])
    shop_locations_index += shop_locations_per_region
    map_2_locations = get_location_names_with_ids(map_2_location_names)
    map_2.add_locations(map_2_locations, ScratchcardHeroLocation)

    map_3_location_names = [
        LOCATIONS.ears
    ]
    map_3_location_names += LOCATIONS.map_3_nodes
    for i in range(shop_locations_index,shop_locations_index+shop_locations_per_region):
        map_3_location_names.append(LOCATIONS.shop_locations[i])
    shop_locations_index += shop_locations_per_region

    if world.options.endless_victory > 0:
        endless_location_names = []
        for i in range(shop_locations_index,len(LOCATIONS.shop_locations)):
            endless_location_names.append(LOCATIONS.shop_locations[i])
        endless_locations = get_location_names_with_ids(endless_location_names)
        endless.add_locations(endless_locations, ScratchcardHeroLocation)
    else:
        for i in range(shop_locations_index,len(LOCATIONS.shop_locations)):
            map_3_location_names.append(LOCATIONS.shop_locations[i])

    map_3_locations = get_location_names_with_ids(map_3_location_names)
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
    for i in range(0,world.options.endless_victory):
      event = EVENTS.endless[i]
      endless.add_event(
        event[0], event[1], location_type=ScratchcardHeroLocation, item_type=ScratchcardHeroItem
      )
