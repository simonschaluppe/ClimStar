import pygame as pg
from functools import partial

from deengi import Engine
from deengi.renderables import Tile, Tilemap, Grid, Dialog, PopupMenu, Label
import gameworld as gw
import config

# --- Load Cards Data --- #
# cards_df = pd.read_excel("cards.xlsx", sheet_name="TECH")
# quartiere_df = pd.read_excel("cards.xlsx", sheet_name="Quartiere")


# --- Game World Setup --- #
class App:

    def __init__(self):
        self.engine = Engine()
        self.game = gw.Game()

        self.engine.setup_camera(
            rotation=45,
            isometry=0.5,
            zoom=30,
        )

    def execute_action(self, action, next_scene):
        action.execute()
        scene = PopupMenu(f"{action.name} executed")
        scene.add_option("Ok", next_scene)
        self.engine.show_dialog(scene)
        # self.engine.switch_to(scene)

    def show_districts_screen(self, index: int = 0):
        district_list = self.game.city.list_districts()
        district = district_list[index]
        scene = Dialog(f"{district.id}")
        scene.text = f"""Block {district}
Location: {district.pos}
Support: {district.support}"""

        for action in district.available_actions():
            cb = partial(
                self.execute_action, action, partial(self.show_districts_screen, index)
            )
            scene.add_option(action.name, cb)
        scene.add_option(
            "Next district",
            partial(self.show_districts_screen, (index + 1) % len(district_list)),
        )
        scene.add_option(
            "Previous district",
            partial(self.show_districts_screen, (index - 1) % len(district_list)),
        )
        scene.add_option("Back", self.show_main_scene)
        self.engine.show_scene(scene)

    def show_main_scene(self):
        self.engine.clear_layer("ui")
        self.engine.show_background(config.colors["background"])

        tilemap = Tilemap()
        for district in self.game.city.list_districts():
            color = config.colors[district.type_name]
            if district.type == gw.DistrictType.INDUSTRY:
                tile = Tile(
                    district.pos,
                    (1, 1),
                    img="assets/images/tile.png",
                    color=color,
                    use_mask=True,
                )
            else:
                tile = Tile(district.pos, (1, 1), color=color, use_mask=True)
            self.engine.input_handler.register_clickable(
                tile, partial(self.show_districts_screen, district.id)
            )
            self.engine.add_tooltip(tile, str(district), color)
            tilemap.add(tile)

        self.engine.add_to_layer("main", tilemap)

        (xmin, xmax), (ymin, ymax) = self.game.city.bounds()
        grid = Grid(xrange=(xmin - 1, xmax + 2), yrange=(ymin - 1, ymax + 2))
        self.engine.add_to_layer("main", grid)

        label = Label(
            pos=(50, 50),
            text=self.game.city.get_ui(),
        )
        self.engine.add_to_layer("ui", label)
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
    game.engine.input_handler.debug = True

    game.start()
