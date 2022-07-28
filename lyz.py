import pygame
from config import *


class Lyziarsky:
    
    def __init__(self, game) -> None:
        self.game = game
        self.first = firstDay(self.game)
        self.day: int = 1
        
    def __new_day(self): self.day += 1
    
    def unlock_room(self):
        '''
        Getting inside own room
        '''
        
        unlocking = True
        locker = pygame.image.load("img/reader.png").convert_alpha()
        unlock_rect = pygame.Rect(191, 134, 52, 38)
        hand_unlocking = pygame.image.load("img/unlocker_hand.png").convert_alpha()
        
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
                self.game.door_info("Unlocked", "room")
                unlocking = False
                self.game.talking_speed_number = tmp
                
            self.game.screen.blit(locker, (0, 0))
            self.game.screen.blit(hand_unlocking, (mouse_pos[0] - 30, mouse_pos[1] - 50))
            # Updates
            self.game.clock.tick(FPS)
            pygame.display.update()
        
class firstDay:
    
    def __init__(self, game) -> None: 
        self.game = game
        self.notes = {1: "Unpack your things next to your bed.", 2: "Take a nap and wait for evening.", 3: "Go get yourself a nice dinner."}
    
    def vybalit(self):
        '''
        If player is inside his lodge then he should unpack his things
        ''' 
        return True if self.game.lyz_in_room == self.game.lyz_rooms[LYZ_FIRST] else False
    
    def open_bag(self):
        return True if self.game.interacted[1] in (4, 5, 6) and self.game.interacted[2] == 4 else False
    
    def unpack_things(self):
        things_in_bag = [pygame.image.load('img/shirts.png'), pygame.image.load('img/ski_boots.png'), pygame.image.load('img/pants.png'), pygame.image.load('img/backpack.png'), pygame.image.load('img/stacked_towels.png')]
        things_in_bag_rects = [things_in_bag[i].get_rect(x=(200 * i) // 2 + 180 if i < 3 else ((200 * i) // 2 + 200) - 250, y=230 - i * 20 if i < 3 else 350 - i * 20) for i in range(len(things_in_bag))]
        bag = pygame.image.load('img/travel_bag.png')
        possible_placements = [pygame.Rect(0, 0, 134, 480), pygame.Rect(372 + 100, 0, 161, 181), pygame.Rect(234, 381, 640 - 234, 99)]
        unpacking = True
        if self.open_bag() and self.game.vybalenie:
            pygame.image.save(self.game.screen, "img/screen.png")
            bg = pygame.image.load("img/screen.png")
            while unpacking:
                # Position of the mouse
                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()
                
                # Events
                for event in pygame.event.get():

                    # Close button/Esc
                    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: unpacking = False
                    
                if mouse_pressed[0]:
                    for clothing in things_in_bag_rects:
                        if clothing.collidepoint(mouse_pos): clothing.center = mouse_pos
                        
                self.game.screen.blit(bg, (0, 0))
                self.game.screen.blit(bag, (40, 0))
                for item in range(len(things_in_bag)): self.game.screen.blit(things_in_bag[item], (things_in_bag_rects[item].x, things_in_bag_rects[item].y))
                
                elements_done = 0
                
                for x in possible_placements:
                    for c in things_in_bag_rects:
                        if pygame.Rect.colliderect(x, c): elements_done += 1
                
                if elements_done >= len(things_in_bag): self.game.info("That should be everything", GREEN); unpacking = False; self.game.vybalenie = False
                        
                # Updates
                self.game.clock.tick(FPS)
                pygame.display.update()