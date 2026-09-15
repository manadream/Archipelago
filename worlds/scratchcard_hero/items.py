from __future__ import annotations

import json
import os

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import ScratchcardHeroWorld

ITEM_NAME_TO_ID = {}
ITEM_NAME_TO_CLASSIFICATION = {}
ITEMS = []
TRAPS = []
FILLER = []

def _add_items_from_json(data, id_start, classification):
    i = id_start
    for item in data:
        ITEM_NAME_TO_ID[item] = i
        ITEM_NAME_TO_CLASSIFICATION[item] = classification
        i += 1
        if classification == ItemClassification.trap:
          TRAPS.append(item)
        elif classification == ItemClassification.filler:
          FILLER.append(item)
        else:
          ITEMS.append(item)


def _initialize():
    with open(os.path.join(os.path.dirname(__file__), 'items_progression.json'), 'r') as file:
        _add_items_from_json(json.loads(file.read()), 1000, ItemClassification.progression)
    with open(os.path.join(os.path.dirname(__file__), 'items_card.json'), 'r') as file:
        _add_items_from_json(json.loads(file.read()), 2000, ItemClassification.useful)
    with open(os.path.join(os.path.dirname(__file__), 'items_gadget.json'), 'r') as file:
        _add_items_from_json(json.loads(file.read()), 3000, ItemClassification.useful)
    with open(os.path.join(os.path.dirname(__file__), 'items_filler.json'), 'r') as file:
        _add_items_from_json(json.loads(file.read()), 4000, ItemClassification.filler)
    with open(os.path.join(os.path.dirname(__file__), 'items_trap.json'), 'r') as file:
        _add_items_from_json(json.loads(file.read()), 5000, ItemClassification.trap)

_initialize()

class ScratchcardHeroItem(Item):
    game = "Scratchcard Hero"


def get_random_filler_item_name(world: ScratchcardHeroWorld) -> str:
    if world.random.randint(0, 99) < world.options.trap_chance:
        return TRAPS[world.random.randint(0, len(TRAPS)-1)]
    return FILLER[world.random.randint(0, len(FILLER)-1)]


def create_item_with_correct_classification(world: ScratchcardHeroWorld, name: str) -> ScratchcardHeroItem:
    classification = ITEM_NAME_TO_CLASSIFICATION[name]
    return ScratchcardHeroItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: ScratchcardHeroWorld) -> None:
    itempool: list[Item] = []

    for item in ITEMS:
      itempool.append(world.create_item(item))

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool

    world.push_precollected(world.create_item("3DD3"))
    if not world.options.must_find_maps:
        world.push_precollected(world.create_item("Map 1"))
        world.push_precollected(world.create_item("Map 2"))
        world.push_precollected(world.create_item("Map 3"))
        world.push_precollected(world.create_item("Endless"))
    else:
      if world.options.start_with_first_map:
        world.push_precollected(world.create_item("Map 1"))
