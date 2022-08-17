import pygame

class Controls:
    
    def __init__(self, game) -> None:
        self.game = game
        self.defaults = {"E": pygame.K_e, "I": pygame.K_i, "N": pygame.K_n}