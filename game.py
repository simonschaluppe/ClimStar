import pygame
import pandas as pd
from components import Player, Tile, ResearchCard
from constants import tile_size, screen_width, screen_height, player_dark_shades, player_light_shades
from renderer import Renderer

# --- Load Cards Data --- #
cards_df = pd.read_excel('cards.xlsx', sheet_name='TECH')
quartiere_df = pd.read_excel('cards.xlsx', sheet_name='Quartiere')

# --- Game World Setup --- #
class Game:
    def __init__(self):
        pygame.init()
        self.setup_game()
        self.load_assets()
        self.initialize_game_elements()
        self.renderer = Renderer(self.screen, self.font, self.bold_font, self.colors, self.player_colors)

    def setup_game(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("District Energy Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.colors = self.get_colors()
        self.player_colors = list(zip(player_dark_shades, player_light_shades))  # Dark and light shades for each player

    def load_assets(self):
        # Load cards from dataframes
        self.tech_cards = [ResearchCard(row.get('Name', 'Unknown'), row.get('K ', 0), row.get('Typ', 'None'), row.get('?', 'None'))
                           for index, row in cards_df.iterrows()]
        self.quartiere_cards = [ResearchCard(row.get('Name', 'Unknown'), row.get('K ', 0), row.get('Typ', 'None'), row.get('?', 'None'))
                                for index, row in quartiere_df.iterrows()]
        # Load font
        self.font = pygame.font.Font(pygame.font.match_font('arial'), 16)
        self.bold_font = pygame.font.Font(pygame.font.match_font('arial'), 16)
        self.bold_font.set_bold(True)

    def initialize_game_elements(self):
        # Create players and tiles
        self.players = [Player(name=f"Player {i+1}", player_id=i) for i in range(4)]
        self.tiles = [Tile(id=i, tile_size=tile_size) for i in range(9)]
        # Set up revealed cards and colors
        self.setup_card_positions()
        self.revealed_tech_card = None
        self.revealed_quartiere_card = None
        self.current_player_index = 0
        self.current_player = self.players[self.current_player_index]
        self.turn_phase = "action"

        # Set up action and end turn buttons
        self.action_buttons = {
            "End Turn": pygame.Rect(screen_width - 200, screen_height - 100, 150, 50),
        }

    def setup_card_positions(self):
        # Adjust card stack and discard pile positions to be in the top middle of the screen, evenly spaced
        stack_width = 100
        stack_height = 150
        spacing = 10
        total_width = 3 * stack_width + 2 * spacing
        start_x = (screen_width - total_width) // 2
        y_position = 20

        self.tech_card_rect = pygame.Rect(start_x, y_position, stack_width, stack_height)
        self.quartiere_card_rect = pygame.Rect(start_x + stack_width + spacing, y_position, stack_width, stack_height)
        self.discard_rect = pygame.Rect(start_x + 2 * (stack_width + spacing), y_position, stack_width, stack_height)

        # Adjust tiles to be in the middle of the screen, arranged in a 3x3 grid
        tile_start_x = (screen_width - (3 * tile_size + 2 * spacing)) // 2
        tile_start_y = (screen_height - (3 * tile_size + 2 * spacing)) // 2

        for i, tile in enumerate(self.tiles):
            row = i // 3
            col = i % 3
            tile.position = (tile_start_x + col * (tile_size + spacing), tile_start_y + row * (tile_size + spacing))

    def get_colors(self):
        return {
            "background": (191, 183, 143),
            "tile": (165, 166, 146),
            "tile_border": (0, 0, 0),
            "meeple": (0, 100, 200),
            "text": (0, 0, 0),
            "card": (150, 150, 250),
            "discard": (1, 31, 38),
            "tech": (2, 94, 115),
            "district": (165, 166, 146),
            "orange":(242, 167, 27),


        }

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, position):
        # Handle the click events for different components
        if self.tech_card_rect.collidepoint(position) and self.tech_cards:
            self.revealed_tech_card = self.tech_cards.pop(0)
        elif self.quartiere_card_rect.collidepoint(position) and self.quartiere_cards:
            self.revealed_quartiere_card = self.quartiere_cards.pop(0)
        elif self.discard_rect.collidepoint(position):
            self.revealed_tech_card = None
            self.revealed_quartiere_card = None
        elif self.action_buttons["End Turn"].collidepoint(position):
            self.end_turn()

    def end_turn(self):
        # Move to the next player's turn
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.current_player = self.players[self.current_player_index]
        self.turn_phase = "action"

    def update(self):
        pass

    def draw(self):
        self.screen.fill(self.colors["background"])
        # Delegate drawing responsibilities to Renderer
        for tile in self.tiles:
            self.renderer.draw_tile(tile)
        self.renderer.draw_player_boards(self.players)
        self.renderer.draw_card_stack(self.tech_card_rect, "Tech Stack", self.revealed_tech_card)
        self.renderer.draw_card_stack(self.quartiere_card_rect, "Quartiere Stack", self.revealed_quartiere_card)
        self.renderer.draw_discard_pile(self.discard_rect)
        self.renderer.draw_turn_info(self.current_player.name)
        self.renderer.draw_action_buttons(self.action_buttons)
        pygame.display.flip()

# --- Main Execution ---
if __name__ == "__main__":
    game = Game()
    game.run()