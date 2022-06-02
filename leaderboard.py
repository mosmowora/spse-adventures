# Imports
import json, pygame, sys
import math
from typing import Any
from config import *
from save_progress import SaveProgress

class Leaderboard:
   
    def __init__(self, game):
        """
        For leaderboard
        """
        
        self.game = game
        
    def show_leaderboard(self):
        """
        Opens leaderboard
        """
        
        leaderboarding: bool = True
        is_up: bool = True
        page_number: int = 1
        
        row = pygame.image.load("img/leaderboard_row.png")
        bg = pygame.image.load("img/leaderboard_bg.jpg")
        first_medal = pygame.image.load("img/first_medal.png")
        second_medal = pygame.image.load("img/second_medal.png")
        third_medal = pygame.image.load("img/third_medal.png")
        
        db = SaveProgress.load_data("")

        players: int = len(db)
        max_page_number = math.ceil(players / 6)
        player_names = db
        
        name_ending: list[tuple] = []

        for player in range(players): 
            if 'endings' not in player_names[player].keys(): player_names[player]['endings'] = []
            name_ending.append((len(player_names[player]['endings']), player_names[player]['name']))
        name_ending.sort(reverse=True)
        
        while leaderboarding:
            
            # Events
            for event in pygame.event.get():
                
                # Close button
                if event.type == pygame.QUIT: sys.exit()
                
                # Keyboard
                if event.type == pygame.KEYDOWN:
                    
                    # WHAT THE HELL
                    if event.key == pygame.K_DOWN and is_up: page_number += 1
                    elif event.key == pygame.K_UP and is_up: page_number -= 1 if page_number > 1 else 0
                    
                    # Escape
                    elif event.key == pygame.K_ESCAPE: leaderboarding = False
                        
            # First page 
            if page_number <= max_page_number and page_number == 1:
                self.game.screen.blit(bg, (0, 0))
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
                    
            # Second page   
            elif page_number <= max_page_number and page_number == 2:
                self.game.screen.blit(bg, (0, 0))
                if players - 6 <= 6:
                    for player in range(6, players):
                        self.game.screen.blit(row, (0, (player - 6) * row.get_height()))
                        player_name = self.game.font.render(name_ending[player][1], True, BLACK)
                        endings = self.game.font.render("Endings: " + str(name_ending[player][0]), True, BLACK)
                        self.game.screen.blit(player_name, (WIN_WIDTH // 2 - 160, (player - 6) * row.get_height() + 23))
                        self.game.screen.blit(endings, (WIN_WIDTH // 2 + 60, (player - 6) * row.get_height() + 23))
                else:
                    for player in range(6):
                        self.game.screen.blit(row, (0, player * row.get_height()))
                        player_name = self.game.font.render(name_ending[player + 6][1], True, BLACK)
                        endings = self.game.font.render("Endings: " + str(name_ending[player + 6][0]), True, BLACK)
                        self.game.screen.blit(player_name, (WIN_WIDTH // 2 - 160, player * row.get_height() + 23))
                        self.game.screen.blit(endings, (WIN_WIDTH // 2 + 60, player * row.get_height() + 23))
            # Third page   
            elif page_number <= max_page_number and page_number == 3:
                self.game.screen.blit(bg, (0, 0))
                if players - 12 <= 6:
                    for player in range(12, players):
                        self.game.screen.blit(row, (0, (player - 12) * row.get_height()))
                        player_name = self.game.font.render(name_ending[player][1], True, BLACK)
                        endings = self.game.font.render("Endings: " + str(name_ending[player][0]), True, BLACK)
                        self.game.screen.blit(player_name, (WIN_WIDTH // 2 - 160, (player - 12) * row.get_height() + 23))
                        self.game.screen.blit(endings, (WIN_WIDTH // 2 + 60, (player - 12) * row.get_height() + 23))
                else:
                    for player in range(6):
                        self.game.screen.blit(row, (0, player * row.get_height()))
                        player_name = self.game.font.render(name_ending[player + 12][1], True, BLACK)
                        endings = self.game.font.render("Endings: " + str(name_ending[player + 12][0]), True, BLACK)
                        self.game.screen.blit(player_name, (WIN_WIDTH // 2 - 160, player * row.get_height() + 23))
                        self.game.screen.blit(endings, (WIN_WIDTH // 2 + 60, player * row.get_height() + 23))
            # Fourth page 
            elif page_number <= max_page_number and page_number == 4:
                self.game.screen.blit(bg, (0, 0))
                if players - 18 <= 6:
                    for player in range(18, players):
                        self.game.screen.blit(row, (0, (player - 18) * row.get_height()))
                        player_name = self.game.font.render(name_ending[player][1], True, BLACK)
                        endings = self.game.font.render("Endings: " + str(name_ending[player][0]), True, BLACK)
                        self.game.screen.blit(player_name, (WIN_WIDTH // 2 - 160, (player - 18) * row.get_height() + 23))
                        self.game.screen.blit(endings, (WIN_WIDTH // 2 + 60, (player - 18) * row.get_height() + 23))
                else:
                    for player in range(6):
                        self.game.screen.blit(row, (0, player * row.get_height()))
                        player_name = self.game.font.render(name_ending[player + 18][1], True, BLACK)
                        endings = self.game.font.render("Endings: " + str(name_ending[player + 18][0]), True, BLACK)
                        self.game.screen.blit(player_name, (WIN_WIDTH // 2 - 160, player * row.get_height() + 23))
                        self.game.screen.blit(endings, (WIN_WIDTH // 2 + 60, player * row.get_height() + 23))
            # Fifth page    
            elif page_number <= max_page_number and page_number == 5:
                self.game.screen.blit(bg, (0, 0))
                if players - 24 <= 6:
                    for player in range(24, players):
                        self.game.screen.blit(row, (0, (player - 24) * row.get_height()))
                        player_name = self.game.font.render(name_ending[player][1], True, BLACK)
                        endings = self.game.font.render("Endings: " + str(name_ending[player][0]), True, BLACK)
                        self.game.screen.blit(player_name, (WIN_WIDTH // 2 - 160, (player - 24) * row.get_height() + 23))
                        self.game.screen.blit(endings, (WIN_WIDTH // 2 + 60, (player - 24) * row.get_height() + 23))
                else:
                    for player in range(6):
                        self.game.screen.blit(row, (0, player * row.get_height()))
                        player_name = self.game.font.render(name_ending[player + 24][1], True, BLACK)
                        endings = self.game.font.render("Endings: " + str(name_ending[player + 24][0]), True, BLACK)
                        self.game.screen.blit(player_name, (WIN_WIDTH // 2 - 160, player * row.get_height() + 23))
                        self.game.screen.blit(endings, (WIN_WIDTH // 2 + 60, player * row.get_height() + 23))
            # Sixth page     
            elif page_number <= max_page_number and page_number == 6:
                self.game.screen.blit(bg, (0, 0))
                if players - 30 <= 6:
                    for player in range(30, players):
                        self.game.screen.blit(row, (0, (player - 30) * row.get_height()))
                        player_name = self.game.font.render(name_ending[player][1], True, BLACK)
                        endings = self.game.font.render("Endings: " + str(name_ending[player][0]), True, BLACK)
                        self.game.screen.blit(player_name, (WIN_WIDTH // 2 - 160, (player - 30) * row.get_height() + 23))
                        self.game.screen.blit(endings, (WIN_WIDTH // 2 + 60, (player - 30) * row.get_height() + 23))
                else:
                    for player in range(6):
                        self.game.screen.blit(row, (0, player * row.get_height()))
                        player_name = self.game.font.render(name_ending[player + 30][1], True, BLACK)
                        endings = self.game.font.render("Endings: " + str(name_ending[player + 30][0]), True, BLACK)
                        self.game.screen.blit(player_name, (WIN_WIDTH // 2 - 160, player * row.get_height() + 23))
                        self.game.screen.blit(endings, (WIN_WIDTH // 2 + 60, player * row.get_height() + 23))
                        
            else: page_number = max_page_number

            # Updates
            self.game.clock.tick(FPS)
            pygame.display.update()

