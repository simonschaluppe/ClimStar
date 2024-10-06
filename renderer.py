import pygame

class Renderer:
    def __init__(self, screen, font, bold_font, colors, player_colors):
        self.screen = screen
        self.font = font
        self.bold_font = bold_font
        self.colors = colors
        self.player_colors = player_colors

    def draw_tile(self, tile):
        position = tile.position
        pygame.draw.rect(self.screen, (200, 200, 200), (*position, *tile.size))
        pygame.draw.rect(self.screen, (0, 0, 0), (*position, *tile.size), 2)

    def draw_player_boards(self, players):
        board_width = 250
        board_height = 100
        positions = [(10, 10), (self.screen.get_width() - board_width - 10, 10),
                     (10, self.screen.get_height() - board_height - 10),
                     (self.screen.get_width() - board_width - 10, self.screen.get_height() - board_height - 10)]
        
        for i, player in enumerate(players):
            pygame.draw.rect(self.screen, self.player_colors[i][1], (*positions[i], board_width, board_height))
            pygame.draw.rect(self.screen, (0, 0, 0), (*positions[i], board_width, board_height), 2)

            player_info = [f"{player.name}", f"$: {player.resources['money']}", f"KH: {player.resources['knowhow']}",
                           f"SUP: {player.resources['support']}", f"MP: {player.meeples}"]
            for j, info in enumerate(player_info):
                text = self.bold_font.render(info, True, self.player_colors[i][0])
                self.screen.blit(text, (positions[i][0] + 10, positions[i][1] + 10 + j * 20))

    def draw_card_stack(self, rect, label, revealed_card):
        pygame.draw.rect(self.screen, (150, 150, 250), rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
        text_surface = self.font.render(label, True, (0, 0, 0))
        self.screen.blit(text_surface, (rect.x + 10, rect.y + 10))
        if revealed_card:
            pygame.draw.rect(self.screen, (150, 150, 250), rect)
            text_surface = self.font.render(f"{revealed_card.name} (Cost: {revealed_card.cost})", True, (0, 0, 0))
            self.screen.blit(text_surface, (rect.x + 10, rect.y + 50))
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)

    def draw_discard_pile(self, discard_rect):
        pygame.draw.rect(self.screen, (250, 100, 100), discard_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), discard_rect, 2)
        text_surface = self.font.render("Discard Pile", True, (0, 0, 0))
        self.screen.blit(text_surface, (discard_rect.x + 10, discard_rect.y + 10))

    def draw_turn_info(self, current_player_name):
        # Display current player's turn information
        turn_text = f"Current Turn: {current_player_name}"
        text_surface = self.bold_font.render(turn_text, True, self.colors["text"])
        self.screen.blit(text_surface, (10, self.screen.get_height() - 50))

    def draw_action_buttons(self, action_buttons):
        for label, rect in action_buttons.items():
            pygame.draw.rect(self.screen, (180, 180, 180), rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
            text_surface = self.font.render(label, True, (0, 0, 0))
            self.screen.blit(text_surface, (rect.x + 10, rect.y + 10))
