import pygame
from config import *


class Lyziarsky:
    
    def __init__(self, game, day: int) -> None:
        self.game = game
        self.first = firstDay(self.game)
        self.day: int = day
        
    def new_day(self):
        print("new day")
        match self.day:
            case 1:
                if self.first.go_sleep(end_day=True): self.day += 1; self.game.lyz_day_number += 1
            case 2: ...
            case 3: ...
            case 4: ...
            case 5: ...
    
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
        self.notes = {1: "Unpack your things next to your bed.", 2: "Take a nap and wait for evening.", 3: "Go visit friends on the top floor", 4: "Tomorrow is another day"}
    
    def open_bag(self): return True if self.game.interacted[1] in (4, 5, 6) and self.game.interacted[2] == 4 else False
        
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

    def go_sleep(self, end_day: bool = False):
        if self.game.interacted[1] == 4 and self.game.interacted[2] in (5, 6) and not self.game.vybalenie and not end_day and self.game.nap:
            fade = pygame.Surface((640, 480))
            fade.fill((0,0,0))
            self.__fade_transition(fade)
            
            # Events
            for event in pygame.event.get():

                # Close button/Esc
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return
                
            self.game.nap = False
            # Updates
            self.game.clock.tick(FPS)
            pygame.display.update()
        
        elif self.game.interacted[1] == 4 and self.game.interacted[2] in (5, 6) and end_day and not self.game.vybalenie and not self.game.nap and not self.game.friends:
            fade = pygame.Surface((640, 480))
            fade.fill((0,0,0))
            self.__fade_transition(fade, True)
            return True
        
    def __fade_transition(self, fade: pygame.Surface, end_day: bool = False):
        for alpha in range(0, 510):
            fade.set_alpha(alpha)
            self.game.screen.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(25)
            if alpha >= 100: fade.blit(self.game.settings_font.render("You took a nap..." if not end_day else "Tomorrow is another day", False, WHITE), (200, 190))
    
    def with_friends(self):
        if self.game.lyz_saved_data == 'second': self.game.friends = False; return True
        return False