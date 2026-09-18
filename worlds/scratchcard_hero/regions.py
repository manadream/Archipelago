from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import ScratchcardHeroWorld


class REGIONS:
    menu = "Menu"
    map_1 = "Map 1"
    map_2 = "Map 2"
    map_3 = "Map 3"
    endless = "Endless"


class ENTRANCES:
    menu_map_1 = "Menu to Map 1"
    map_1_2 = "Map 1 to Map 2"
    map_2_3 = "Map 2 to Map 3"
    map_3_endless = "Map 3 to Endless"


def create_and_connect_regions(world: ScratchcardHeroWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: ScratchcardHeroWorld) -> None:
    menu = Region(REGIONS.menu, world.player, world.multiworld)
    map_1 = Region(REGIONS.map_1, world.player, world.multiworld)
    map_2 = Region(REGIONS.map_2, world.player, world.multiworld)
    map_3 = Region(REGIONS.map_3, world.player, world.multiworld)
    endless = Region(REGIONS.endless, world.player, world.multiworld)

    regions = [menu, map_1, map_2, map_3, endless]

    world.multiworld.regions += regions


def connect_regions(world: ScratchcardHeroWorld) -> None:
    menu = world.get_region(REGIONS.menu)
    map_1 = world.get_region(REGIONS.map_1)
    map_2 = world.get_region(REGIONS.map_2)
    map_3 = world.get_region(REGIONS.map_3)
    endless = world.get_region(REGIONS.endless)

    menu.connect(map_1, ENTRANCES.menu_map_1)
    map_1.connect(map_2, ENTRANCES.map_1_2)
    map_2.connect(map_3, ENTRANCES.map_2_3)
    map_3.connect(endless, ENTRANCES.map_3_endless)
