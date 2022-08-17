import pygame

class Controls:
    
    def __init__(self, game) -> None:
        self.game = game
        self.defaults = {"E": pygame.K_e, "I": pygame.K_i, "N": pygame.K_n}
        
    def set_control(self, key: str, new_value):
        '''
        key -> control to set\n
        new_value -> new control to be the key for from the defaults e.g (pygame.K_i)
        '''
        self.defaults[key] = new_value