from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import ScratchcardHeroWorld

class ITEMS:
  filler = ["Filler",ItemClassification.filler]
  trap = ["Trap",ItemClassification.trap]
  map_2 = ["Map 2",ItemClassification.progression]
  map_3 = ["Map 3",ItemClassification.progression]
  endless = ["Endless",ItemClassification.progression]
  d3 = ["3DD3",ItemClassification.progression]

ITEM_NAME_TO_ID = {}
ITEM_NAME_TO_CLASSIFICATION = {}

def initialize():
    i = 1
    for attr in dir(ITEMS):
        if not attr.startswith("__"):
            item = getattr(ITEMS, attr)
            ITEM_NAME_TO_ID[item[0]] = i
            ITEM_NAME_TO_CLASSIFICATION[item[0]] = item[1]
            i += 1

class ScratchcardHeroItem(Item):
    game = "Scratchcard Hero"


def get_random_filler_item_name(world: ScratchcardHeroWorld) -> str:
    if world.random.randint(0, 99) < world.options.trap_chance:
        return ITEMS.trap[0]
    return ITEMS.filler[0]


def create_item_with_correct_classification(world: ScratchcardHeroWorld, name: str) -> ScratchcardHeroItem:
    classification = ITEM_NAME_TO_CLASSIFICATION[name]
    return ScratchcardHeroItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: ScratchcardHeroWorld) -> None:
    itempool: list[Item] = [
        world.create_item(ITEMS.d3[0])
    ]

    if world.options.must_find_maps:
        itempool.append([
            world.create_item(ITEMS.map_2[0]),
            world.create_item(ITEMS.map_3[0]),
            world.create_item(ITEMS.endless[0]),
        ])


    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool

    starting_card = world.create_item(ITEMS.d3[0])
    world.push_precollected(starting_card)
