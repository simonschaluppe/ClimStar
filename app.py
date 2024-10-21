import pygame as pg
from functools import partial

from deengi import Engine, Scene, Option
from gameworld import Game
import config

# --- Load Cards Data --- #
# cards_df = pd.read_excel("cards.xlsx", sheet_name="TECH")
# quartiere_df = pd.read_excel("cards.xlsx", sheet_name="Quartiere")


# --- Game World Setup --- #
class App:

    def __init__(self):
        self.engine = Engine()
        self.game = Game()

        self.engine.setup_camera(
            rotation=45,
            isometry=0.3,
            zoom=30,
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
        positions, sizes = self.game.city.get_tilemap_info()
        colors = [config.colors[d.type_name] for d in self.game.city.list_districts()]
        self.engine.create_tilemap(positions, sizes, colors)
        self.engine.show_tilemap()
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


# --- Main Execution ---
if __name__ == "__main__":
    game = App()
    game.engine.renderer.colors = config.colors
    game.engine.renderer.debug = False
    game.start()
