from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

from .items import ITEMS
from .regions import ENTRANCES
from .locations import EVENTS

if TYPE_CHECKING:
    from .world import ScratchcardHeroWorld

def set_all_rules(world: ScratchcardHeroWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: ScratchcardHeroWorld) -> None:
    map_1_to_map_2 = world.get_entrance(ENTRANCES.map_1_2)
    map_2_to_map_3 = world.get_entrance(ENTRANCES.map_2_3)
    map_3_to_endless = world.get_entrance(ENTRANCES.map_3_endless)

    can_proceed_to_map_2 = Has(EVENTS.map_1_boss)
    if world.options.must_find_maps:
      can_proceed_to_map_2 = can_proceed_to_map_2 & Has(ITEMS.map_2[0])
    world.set_rule(map_1_to_map_2, can_proceed_to_map_2)

    can_proceed_to_map_3 = Has(EVENTS.map_2_boss)
    if world.options.must_find_maps:
      can_proceed_to_map_3 = can_proceed_to_map_3 & Has(ITEMS.map_3[0])
    world.set_rule(map_2_to_map_3, can_proceed_to_map_3)

    can_proceed_to_endless = Has(EVENTS.map_3_boss)
    if world.options.must_find_maps:
      can_proceed_to_endless = can_proceed_to_endless & Has(ITEMS.endless[0])
    world.set_rule(map_3_to_endless, can_proceed_to_endless)


def set_all_location_rules(world: ScratchcardHeroWorld) -> None:
    pass


def set_completion_condition(world: ScratchcardHeroWorld) -> None:
    endless_win = world.options.endless_victory
    if endless_win > 0:
      world.set_completion_rule(Has(EVENTS.endless[endless_win-1][1]))
    else:
      map_win = world.options.map_victory
      if map_win == 1:
          world.set_completion_rule(Has(EVENTS.map_1_boss[1]))
      elif map_win == 2:
          world.set_completion_rule(Has(EVENTS.map_2_boss[1]))
      else:
          world.set_completion_rule(Has(EVENTS.map_3_boss[1]))
