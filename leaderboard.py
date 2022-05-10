import json, pygame
from config import *

class Leaderboard:
   
    def __init__(self, game):
        """
        For leaderboard
        """
        
        self.game = game
        self.player_info: str = "Database/progress.json"
        
    def show_leaderboard(self):
        """
        Opens leaderboard
        """
        
        leaderboarding: bool = True
        is_up: bool = True
        scroll: bool = True
        
        row = pygame.image.load("img/leaderboard_row.png")
        bg = pygame.image.load("img/leaderboard_bg.jpg")
        first_medal = pygame.image.load("img/first_medal.png")
        second_medal = pygame.image.load("img/second_medal.png")
        third_medal = pygame.image.load("img/third_medal.png")
        players: int = len(json.load(open(self.player_info)))
        player_names: List = json.load(open(self.player_info))
        
        name_ending: list[tuple] = []
        for player in range(players): name_ending.append((len(player_names[player]['endings']), player_names[player]['name']))
        name_ending.sort(reverse=True)
        
        while leaderboarding:
            
            # Events
            for event in pygame.event.get():
                
                # Close button
                if event.type == pygame.QUIT: quit()
                
                # Keyboard
                if event.type == pygame.KEYDOWN:
                    
                    # WHAT THE HELL
                    if event.key == pygame.K_DOWN and is_up: scroll = not scroll
                    
                    # Escape
                    elif event.key == pygame.K_ESCAPE: leaderboarding = False
                        
            
            if scroll:
                self.game.screen.blit(bg, (0, 0))
                # len(json.load(open(self.player_info, "r")))
                if players <= 6:
                    for player in range(players):
                        self.game.screen.blit(row, (0, player * row.get_height()))
                        if player == 0: self.game.screen.blit(first_medal, (WIN_WIDTH // 2 - 247, player * row.get_height() + 10))
                        elif player == 1: self.game.screen.blit(second_medal, (WIN_WIDTH // 2 - 245, player * row.get_height() + 10))
                        elif player == 2: self.game.screen.blit(third_medal, (WIN_WIDTH // 2 - 245, player * row.get_height() + 10))
                        player_name = self.game.font.render(name_ending[player][1], True, BLACK)
                        endings = self.game.font.render("Endings: " + str(name_ending[player][0]), True, BLACK)
                        self.game.screen.blit(player_name, (WIN_WIDTH // 2 - 160, player * row.get_height() + 23))
                        self.game.screen.blit(endings, (WIN_WIDTH // 2 + 60, player * row.get_height() + 23))
                else:
                    for player in range(6):
                        self.game.screen.blit(row, (0, player * row.get_height()))
                        if player == 0: self.game.screen.blit(first_medal, (WIN_WIDTH // 2 - 234, player * row.get_height() + 10))
                        elif player == 1: self.game.screen.blit(second_medal, (WIN_WIDTH // 2 - 234, player * row.get_height() + 10))
                        elif player == 2: self.game.screen.blit(third_medal, (WIN_WIDTH // 2 - 234, player * row.get_height() + 10))
                        player_name = self.game.font.render(name_ending[player][1], True, BLACK)
                        endings = self.game.font.render("Endings: " + str(name_ending[player][0]), True, BLACK)
                        self.game.screen.blit(player_name, (WIN_WIDTH // 2 - 160, player * row.get_height() + 23))
                        self.game.screen.blit(endings, (WIN_WIDTH // 2 + 60, player * row.get_height() + 23))
                    
                
            elif not scroll:
                self.game.screen.blit(bg, (0, 0))
                for player in range(players):
                    self.game.screen.blit(row, (0, player * row.get_height()))
                    
            # Updates
            self.game.clock.tick(FPS)
            pygame.display.update()