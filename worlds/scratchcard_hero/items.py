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


def _initialize():
    with open(os.path.join(os.path.dirname(__file__), 'ap_items.json'), 'r') as file:
        data = json.loads(file.read())
        for item in data:
            i_name = item["name"]
            i_id = item["id"]
            i_classification = None
            match item["type"]:
                case "progression":
                    i_classification = ItemClassification.progression
                case "filler":
                    i_classification = ItemClassification.filler
                    FILLER.append(i_name)
                case "trap":
                    i_classification = ItemClassification.trap
                    TRAPS.append(i_name)
                case _:
                    i_classification = ItemClassification.useful
            ITEMS.append(i_name)
            ITEM_NAME_TO_ID[i_name] = i_id
            ITEM_NAME_TO_CLASSIFICATION[i_name] = i_classification


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
        if "Addon" not in item or world.options.must_find_addon_stamps:
            itempool.append(world.create_item(item))

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool

    world.push_precollected(world.create_item("3DD3"))
    world.push_precollected(world.create_item("Spinner Slot"))
    world.push_precollected(world.create_item("Simple Spinner"))
    if not world.options.must_find_maps:
        world.push_precollected(world.create_item("Map 1"))
        world.push_precollected(world.create_item("Map 2"))
        world.push_precollected(world.create_item("Map 3"))
        world.push_precollected(world.create_item("Endless"))
    else:
        if world.options.start_with_first_map:
            world.push_precollected(world.create_item("Map 1"))
