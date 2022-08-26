import pygame
from config import *
from card_game.cards import start

class Cinematic:
    
    def __init__(self, game) -> None:
        self.game = game
        
    def animate(self):
        if not self.game.vybalenie and not self.game.nap and self.game.lyz_in_room == self.game.lyz_rooms[LYZ_FIRST] and self.game.lyz_day_number == 1:
            tmp_room = self.game.samko_placement((5, 8))
            self.game.create_tile_map(tmp_room)
            for sprite in self.game.all_sprites: 
                sprite.rect.x += 6 * TILE_SIZE
                sprite.rect.y -= 12 * TILE_SIZE
            self.game.player.rect.y += 10 * TILE_SIZE
            self.game.player.rect.x -= 5 * TILE_SIZE
            return True
        
        elif self.game.lyz_day_number == 3 and self.game.lyz_bratko_count != 0:
            tmp_room = self.game.samko_placement((4, 1))
            self.game.create_tile_map(tmp_room)
            for sprite in self.game.all_sprites: 
                sprite.rect.x += 6 * TILE_SIZE
                sprite.rect.y -= 12 * TILE_SIZE
            self.game.player.rect.y += 10 * TILE_SIZE
            self.game.player.rect.x -= 5 * TILE_SIZE
            return True

        else:
            self.game.create_tile_map()
            for sprite in self.game.all_sprites:
                sprite.rect.x += 6 * TILE_SIZE
                sprite.rect.y -= 6 * TILE_SIZE
            self.game.player.rect.y += 10 * TILE_SIZE
            self.game.player.rect.x -= 5 * TILE_SIZE
            return False

class Lyziarsky:
    
    def __init__(self, game, day: int) -> None:
        self.game = game
        self.first = firstDay(self.game)
        self.second = secondDay(self.game)
        self.third = thirdDay(self.game)
        self.day: int = day
        
    def new_day(self):
        print("day: {}".format(self.game.lyz_day_number))
        if self.first._has_all() and self.first.go_sleep(end_day=True) and self.day == 1: self.day += 1; self.game.lyz_day_number += 1
        elif self.second._has_all() and self.first.go_sleep(end_day=True) and self.day == 2: self.day += 1; self.game.lyz_day_number += 1
    
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
            self.__fade_transition(fade, True, "Tomorrow is another day")
            return True
    
    def _has_all(self): return True if not self.game.nap and not self.game.friends and not self.game.vybalenie else False
    
    def __fade_transition(self, fade: pygame.Surface, end_day: bool = False, text: str = ""):
        for alpha in range(0, 510):
            fade.set_alpha(alpha)
            self.game.screen.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(25)
            if alpha >= 100: fade.blit(self.game.settings_font.render("You took a nap..." if not end_day else text, False, WHITE), (200, 190))
    
    def with_friends(self):
        if self.game.lyz_saved_data == 'second': self.game.friends = False; return True
        return False
    
class secondDay:
    
    def __init__(self, game) -> None: 
        self.game = game
        self.notes = {1: "Go to the kitchen for your skis.", 2: "Go straight to the ski slope.", 3: "Go meet up with a teacher in the diner.", 4: "Tomorrow is another day"}

    def _has_all(self): return True if not self.game.ski_suit_on and not self.game.skied_two and not self.game.talked_with_teacher else False
    
    def grab_suit(self):
        suiting = True
        pygame.image.save(self.game.screen, "img/screen.png")
        bg = pygame.image.load("img/screen.png")
        ski_coat = pygame.image.load("img/ski_coat.png")
        ski_coat_rect = ski_coat.get_rect(x=0, y=0)
        ski_pants = pygame.image.load("img/ski_pants.png")
        ski_pants_rect = ski_pants.get_rect(x=0, y=112)
        ski_boots = pygame.image.load("img/ski_bots.png")
        ski_boots_rect = ski_boots.get_rect(x=0, y=224)
        person_silhoutte = pygame.image.load("img/silhouette.png")
        person_silhoutte_rect = person_silhoutte.get_rect(x=320 - person_silhoutte.get_width() // 2, y=0)
        can_move_boot = True
        can_move_coat = True
        can_move_pants = True
        
        while suiting:
            
            # Position of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
        
            # Events
            for event in pygame.event.get():

                # Close button/Esc
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return
                
                
            if ski_coat_rect.center[0] in range(315, 325) and ski_coat_rect.center[1] in range(149, 169): can_move_coat = False
            if ski_pants_rect.center[0] in range(319, 329) and ski_pants_rect.center[1] in range(246, 256): can_move_pants = False
            if ski_boots_rect.center[0] in range(315, 325) and ski_boots_rect.center[1] in range(316, 326): can_move_boot = False

            if mouse_pressed[0]:
                if ski_boots_rect.collidepoint(mouse_pos) and can_move_boot: ski_boots_rect.center = mouse_pos
                elif ski_coat_rect.collidepoint(mouse_pos) and can_move_coat: ski_coat_rect.center = mouse_pos
                elif ski_pants_rect.collidepoint(mouse_pos) and can_move_pants: ski_pants_rect.center = mouse_pos
                
            if not can_move_boot and not can_move_coat and not can_move_pants:
                self.game.ski_suit_on = False
                return
            
            self.game.screen.blit(bg, (0,0))
            self.game.screen.blit(person_silhoutte, person_silhoutte_rect)
            self.game.screen.blit(ski_boots, ski_boots_rect)
            self.game.screen.blit(ski_pants, ski_pants_rect)
            self.game.screen.blit(ski_coat, ski_coat_rect)
            # Updates
            self.game.clock.tick(FPS)
            pygame.display.update()


class thirdDay:
    def __init__(self, game) -> None: 
        self.game = game
        self.notes = {1: "Help your friend repair the speaker.", 2: "A bed in your room has broken down.", 3: "You've been invited to the top floor.", 4: "Tomorrow is another day"}
        
    def repair_speaker(self):
        repairing: bool = True
        speaker_arrow = pygame.image.load("img/speaker_arrow.png")
        speaker_room = pygame.image.load("img/speaker_room.jpg")
        speaker_bar = pygame.image.load("img/repair_speaker.png")
        speaker = pygame.image.load("img/speaker_to_repair.png")
        x_coord = 110
        left: bool = False
        speed: int = 5
        repaired: int = 0
        while repairing:
            
            # Events
            for event in pygame.event.get():

                # Close button/Esc
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return
                
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and speaker_arrow.get_rect(x=x_coord, y=20).center[0] in range(110+192, 110+253):
                    repaired += 1
                    speed += 5
            
            if x_coord <= 420 and not left:
                x_coord += speed
            elif x_coord >= 110:
                x_coord -= speed
                left = True
            else: 
                left = False
                
            self.game.screen.blit(speaker_room, (0, 0))
            self.game.screen.blit(self.game.big_font.render(f"repaired: {repaired}/4", True, WHITE), (0, 0))
            self.game.screen.blit(speaker_arrow, (x_coord, 20))
            self.game.screen.blit(speaker_bar, (120, 80))
            self.game.screen.blit(speaker, (100, 185))

            if repaired == 4: self.game.lyz_repair_speaker = False; repairing = False
            
            # Updates
            self.game.clock.tick(FPS)
            pygame.display.update()
            
            
    def _has_all(self): return True if not self.game.repaired_bed and not self.game.lyz_repair_speaker and not self.game.cards else False

    def repair_bed(self):
        bg = pygame.image.load("img/speaker_room.jpg")
        bed_img = pygame.image.load("img/repair_bed.png")
        bed_one = pygame.image.load("img/bed_one.png")
        bed_two = pygame.image.load("img/bed_two.png")
        rects: list[pygame.Rect] = []
        repaired: int = 0
        repairing: bool = True
        for i in range(4):
            if i < 2:
                rects.append(pygame.Rect(90 + i*130, 210, 120, 80))
            else:
                rects.append(pygame.Rect(150 + (i-1)*130, 210, 120, 80))
                
        
        while repairing:
            
            # Position, and state of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]
            
            # Events
            for event in pygame.event.get():

                # Close button/Esc
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return
                
            for i in rects:
                if i.collidepoint(mouse_pos) and mouse_pressed:
                    i.center = (690, 530)
                    repaired += 1
                    
            
            self.game.screen.blit(bg, (0, 0))
            for i in range(2):
                self.game.screen.blit(bed_one, rects[i])
            for i in range(2, 4):
                self.game.screen.blit(bed_two, rects[i])
            self.game.screen.blit(bed_img, (80, 80))
                
            if repaired == 4: self.game.repaired_bed = False; repairing = False
            
            # Updates
            self.game.clock.tick(FPS)
            pygame.display.update()
            
    def play_cards(self):
        
        if self.game.lyz_in_room == self.game.lyz_rooms[LYZ_SECOND] and not self.game.repaired_bed and not self.game.lyz_repair_speaker:
            result = start()
            return result