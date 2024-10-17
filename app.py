from functools import partial
import pygame
import pandas as pd
import pygame as pg
from constants import (
    tile_size,
    screen_width,
    screen_height,
    player_dark_shades,
    player_light_shades,
)

import sys
from pathlib import Path

sys.path.append("../engine")

from renderer import Renderer
from text_engine import Engine, Scene, Option

from gameworld import Block, Game

# --- Load Cards Data --- #
# cards_df = pd.read_excel("cards.xlsx", sheet_name="TECH")
# quartiere_df = pd.read_excel("cards.xlsx", sheet_name="Quartiere")


# --- Game World Setup --- #
class App:

    def __init__(self):
        self.engine = Engine()
        self.input_handler = self.engine.input_handler

        self.game = Game()

    def load_assets(self):
        # Load cards from dataframes
        self.tech_cards = [
            ResearchCard(
                row.get("Name", "Unknown"),
                row.get("K ", 0),
                row.get("Typ", "None"),
                row.get("?", "None"),
            )
            for index, row in cards_df.iterrows()
        ]
        self.quartiere_cards = [
            ResearchCard(
                row.get("Name", "Unknown"),
                row.get("K ", 0),
                row.get("Typ", "None"),
                row.get("?", "None"),
            )
            for index, row in quartiere_df.iterrows()
        ]

    def start_block_scene(self, block: Block):
        scene = Scene(f"{block.id}")
        scene.text = f"Block {block}\nLocation: {block.position}"
        scene.add_options(Option("Back", self.start_main_scene))
        self.engine.switch_to(scene)

    def start_main_scene(self):
        main_scene = Scene()
        main_scene.title = f"The city of {self.game.city.name}"

        main_scene.text = str(self.game.city)
        # this is where the game stats are arranged etc

        # then comes the logic
        o1 = Option("Quit Game", self.engine.quit)
        block = self.game.city.blocks[(0, 0)]
        o2 = Option(f"Goto Block {block.id}", partial(self.start_block_scene, block))
        main_scene.add_options(o2, o1)
        self.engine.switch_to(main_scene)

    def start(self):
        # create starting scene
        self.game.create_city()
        print(self.game.city)
        scene = self.start_main_scene()

        self.engine.run()

    def quit(self):
        pg.quit()
        quit()


# --- Main Execution ---
if __name__ == "__main__":
    game = App()
    game.start()
