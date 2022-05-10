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
        scroll: bool = False
        
        row = pygame.image.load("img/leaderboard_row.png")
        players: int = len(json.load(open(self.player_info, "r")))
        
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
                # len(json.load(open(self.player_info, "r")))
                for player in range(1):
                    self.game.screen.blit(row, (0, player))
                
            elif not scroll:
                for player in range(1):
                    self.game.screen.blit(row, (0, player))
                    
            # Updates
            self.game.clock.tick(FPS)
            pygame.display.update()