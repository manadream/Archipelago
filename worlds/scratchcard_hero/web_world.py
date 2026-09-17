from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .options import option_groups, option_presets


class ScratchcardHeroWebWorld(WebWorld):
    game = "Scratchcard Hero"

    # You can choose between dirt, grass, grassFlowers, ice, jungle, ocean, partyTime, and stone.
    theme = "partyTime"

    bug_report_page = "https://github.com/manadream/Archipelago/issues"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Scratchcard Hero for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["NewSoupVi"],
    )

    tutorials = [setup_en]

    option_groups = option_groups
    options_presets = option_presets
