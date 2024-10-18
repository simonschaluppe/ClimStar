import pygame as pg
import sys
from functools import partial
from pathlib import Path

sys.path.append("../engine")

from engine import Engine, Scene, Option
from gameworld import District, Game, Action

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

        self.engine.renderer.camera.set_rotation(10)
        self.engine.renderer.camera.set_isometry(0.3)
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

    def show_districts_screen(self, index: int = 0):
        district_list = self.game.city.list_districts()
        district = district_list[index]
        scene = Scene(f"{district.id}")
        scene.text = f"""Block {district}
Location: {district.position}
Support: {district.support}"""

        for action in district.available_actions():
            cb = partial(
                self.execute_action, action, partial(self.show_districts_screen, index)
            )
            scene.add_options(Option(action.name, cb))
        scene.add_options(
            Option(
                "Next district",
                partial(self.show_districts_screen, (index + 1) % len(district_list)),
            )
        )
        scene.add_options(
            Option(
                "Previous district",
                partial(self.show_districts_screen, (index - 1) % len(district_list)),
            )
        )
        scene.add_options(Option("Back", self.show_main_scene))
        self.engine.show_scene(scene)

    def show_main_scene(self):

        tilemap = create_tilemap(config.colors, self.game.city.districts)
        main_data = dict(tilemap=tilemap, grid=True)
        main_renderer = self.engine.renderer.render_tilemap

        self.engine.set_rendering_callback(main_renderer, main_data)
        # add input handling for tile clicks:
        # self.engine.input_handler.register_collidermasks()

        ui_renderer = self.engine.renderer.draw_text
        ui_data = dict(text=self.game.city.get_ui(), pos=(50, 50))
        self.engine.add_rendering_callbacks((ui_renderer, ui_data))

        self.engine.input_handler.bind_keypress(pg.K_d, self.show_districts_screen)

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
