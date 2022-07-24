import pygame
from config import *


class Lyziarsky:
    
    def __init__(self, game) -> None:
        self.game = game
        self.first = firstDay(self.game)
        self.day: int = 1
        
    def new_day(self): self.day += 1 
        
    def unlock_room(self):
        '''
        Getting inside own room
        '''
        
        unlocking = True
        locker = pygame.image.load("img/reader.png")
        unlock_rect = pygame.Rect(191, 134, 52, 38)
        hand_unlocking = pygame.image.load("img/unlocker_hand.png")
        
        while unlocking:
            
            # Position of the mouse
            mouse_pos = pygame.mouse.get_pos()
            
            # Events
            for event in pygame.event.get():

                # Close button/Esc
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: unlocking = False
                
            if unlock_rect.collidepoint(mouse_pos):
                tmp = self.game.talking_speed_number
                self.game.talking_speed_number = 120
                self.game.talking("Wait a moment...", True, BRITISH_WHITE)
                self.game.talking("Unlocked", True, BRITISH_WHITE)
                unlocking = False
                self.game.talking_speed_number = tmp
                
            self.game.screen.blit(locker, (0, 0))
            self.game.screen.blit(hand_unlocking, (mouse_pos[0] - 50, mouse_pos[1] - 50))
            # Updates
            self.game.clock.tick(FPS)
            pygame.display.update()
        
class firstDay:
    
    def __init__(self, game) -> None: self.game = game
    
    def vybalit(self):
        '''
        If player is inside his lodge then he should vybalit sa
        ''' 
        return True if self.game.lyz_in_room == self.game.lyz_rooms[LYZ_FIRST] else False
            