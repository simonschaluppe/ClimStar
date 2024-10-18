import pygame as pg
import sys
from functools import partial
from pathlib import Path

sys.path.append("../engine")

from engine import Engine, Scene, Option
from gameworld import Block, Game, Action

import config
from util import create_tilemap

# --- Load Cards Data --- #
# cards_df = pd.read_excel("cards.xlsx", sheet_name="TECH")
# quartiere_df = pd.read_excel("cards.xlsx", sheet_name="Quartiere")


# --- Game World Setup --- #
class App:

    def __init__(self):
        self.engine = Engine()
        self.game = Game()

        self.engine.renderer.camera.set_isometry_angle(30)
        self.engine.renderer.camera.zoom(30)
        self.engine.input_handler.bind_camera_zoom_to_mousewheel(
            self.engine.renderer.camera
        )
        self.engine.input_handler.bind_camera_pan_to_mousedrag(
            self.engine.renderer.camera, button=1
        )

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

    def execute_action(self, action, next_scene):
        action.execute()
        scene = Scene(f"{action.name} executed")
        scene.add_options(Option("Ok", next_scene))
        self.engine.show_dialog(scene)
        # self.engine.switch_to(scene)

    def start_block_scene(self, block: Block):
        scene = Scene(f"{block.id}")
        scene.text = f"""Block {block}
Location: {block.position}
Support: {block.support}"""

        for action in block.available_actions():
            cb = partial(
                self.execute_action, action, partial(self.start_block_scene, block)
            )
            scene.add_options(Option(action.name, cb))
        scene.add_options(Option("Back", self.show_main_scene))
        self.engine.switch_to(scene)

    def show_main_scene(self):

        main_renderer = self.engine.renderer.render_tilemap
        tilemap = create_tilemap(config.colors, self.game.city.blocks)
        main_data = dict(tilemap=tilemap, grid=True)

        self.engine.set_rendering_callback(main_renderer, main_data)
        # add input handling for tile clicks:
        # self.engine.input_handler.register_collidermasks()
        # if mousepos collides with tilemask
        # show_scene

        ui_renderer = self.engine.renderer.draw_text
        ui_data = dict(text=self.game.city.get_ui(), pos=(50, 50))
        self.engine.add_rendering_callbacks((ui_renderer, ui_data))

        #  c

    def start(self):
        # create starting scene
        self.game.create_city()

        self.show_main_scene()

        self.engine.run()

    def quit(self):
        pg.quit()
        quit()


# --- Main Execution ---
if __name__ == "__main__":
    game = App()
    game.engine.renderer.colors = config.colors
    game.engine.renderer.debug = False
    game.start()
