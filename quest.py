import pygame
from config import *
from sprites import Button

class Quest:
    
    def __init__(self, game):
        """
        Make more complex quests here.
        """

        self.game = game
    
    def bench_press(self, bench_done: bool):
        """
        Tst quest - Bench press
        """

        self.bench_done = bench_done
        grade: int = 5

        # Already did bench press
        if not self.bench_done: self.game.talking("I already did this."); return False
        
        # Music
        if self.game.music_on: pygame.mixer.Sound.stop(self.game.theme); pygame.mixer.Sound.play(self.game.tsv_theme, -1)

        # Bench press quest for stronk bois
        background = pygame.image.load("img/bench_press.png").convert()
        dumbbell = pygame.image.load("img/bench_press_dumbbell.png").convert_alpha()
        dumbbell_rect = dumbbell.get_rect(x=0, y=50)
        back_button = Button(500, 400, 120, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)
        working_out: bool = True
        counter: int = 0
        push_strength: int = 20
        weak: bool = True
        exited: bool = False
        start: int = pygame.time.get_ticks()
        
        while working_out and counter < 5:
            
            # You have 1 min for this
            if pygame.time.get_ticks() - start > 60 * 1000: working_out = False

            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: self.game.exiting()

                # Clicking
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if dumbbell_rect.y >= -100: 
                        if counter == 2: dumbbell_rect.y -= push_strength - 3
                        elif counter == 3: dumbbell_rect.y -= push_strength - 5
                        elif counter == 4: dumbbell_rect.y -= push_strength - 7
                        else: dumbbell_rect.y -= push_strength
                        
                    else: dumbbell_rect.y = 50; counter += 1

            # Dumbbell down
            if dumbbell_rect.y <= 50: 
                if counter == 2: dumbbell_rect.y += 1.1
                elif counter == 3: dumbbell_rect.y += 1.2
                elif counter == 4: dumbbell_rect.y += 1.3
                else: dumbbell_rect.y += 1                    

            # Background, button, image
            self.game.screen.blit(background, (0, 0))
            self.game.screen.blit(self.game.font.render("Times lifted: {} of 5".format(counter), True, WHITE), (10, 10))
            self.game.screen.blit(dumbbell, dumbbell_rect)
            self.game.screen.blit(back_button.image, back_button.rect)
            if back_button.is_pressed(mouse_pos, mouse_pressed): working_out = False; weak = True; exited = True
            self.game.clock.tick(FPS)
            pygame.display.update()

        # Made it
        if not exited: 
            weak = False
            if grade - counter == 0: grade = 1
            else: grade -= counter
            
            self.game.grades["TSV - gym"] = grade

        # Music
        if self.game.music_on: pygame.mixer.Sound.stop(self.game.tsv_theme); pygame.mixer.Sound.play(self.game.theme, -1)

        # Return
        return weak
    
    def programming(self):
        """
        Potitat 
        """

        # Potitat v LROB
        if self.game.interacted[2] == 0 and self.game.interacted[1] == 25 and self.game.program_test:

            in_potitat = True

            # Background
            bg = pygame.image.load("img/LROB.png")
            
            # active
            active_def = False
            active_self = False
            active_item = False
            active_even = False
            active_tuple = False

            # Color
            color = GRAY

            # To fill
            fill_def = pygame.Rect(84, 91, 26, 16)
            fill_self = pygame.Rect(220, 93, 29, 14)
            fill_item = pygame.Rect(248, 207, 30, 16)
            fill_even = pygame.Rect(496, 206, 42, 19)
            fill_tuple = pygame.Rect(248, 227, 35, 15)
            
            # text
            text_def = ""
            text_self = ""
            text_item = ""
            text_even = ""
            text_tuple = ""
            
            # Button
            back_button = Button(10, 400, 120, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)
            grade_button = Button(500, 400, 120, 50, fg=WHITE, bg=BLACK, content="Grade", fontsize=32)

            while in_potitat:

                # Position and click of the mouse
                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()

                # Events
                for event in pygame.event.get():

                    # Close button
                    if event.type == pygame.QUIT: self.game.exiting()

                    # Click
                    elif event.type == pygame.MOUSEBUTTONDOWN:

                        if fill_def.collidepoint(event.pos): active_def = True; active_self = False; active_item = False; active_even = False; active_tuple = False # Def
                        elif fill_self.collidepoint(event.pos): active_def = False; active_self = True; active_item = False; active_even = False; active_tuple = False # Self
                        elif fill_item.collidepoint(event.pos): active_def = False; active_self = False; active_item = True; active_even = False; active_tuple = False # Item
                        elif fill_even.collidepoint(event.pos): active_def = False; active_self = False; active_item = False; active_even = True; active_tuple = False # Even
                        elif fill_tuple.collidepoint(event.pos): active_def = False; active_self = False; active_item = False; active_even = False; active_tuple = True # Tuple
                        
                    # Keyboard
                    if event.type == pygame.KEYDOWN:
        
                        # Esc
                        if event.key == pygame.K_ESCAPE: in_potitat = False

                        # Check for backspace
                        elif event.key == pygame.K_BACKSPACE: 
                            if active_def: text_def = text_def[:-1]
                            elif active_self: text_self = text_self[:-1]
                            elif active_item: text_item = text_item[:-1]
                            elif active_even: text_even = text_even[:-1]
                            elif active_tuple: text_tuple = text_tuple[:-1]
                        
                        elif active_def: text_def += event.unicode
                        elif active_self: text_self += event.unicode
                        elif active_item: text_item += event.unicode
                        elif active_even: text_even += event.unicode
                        elif active_tuple: text_tuple += event.unicode

                # Back button
                if back_button.is_pressed(mouse_pos, mouse_pressed): in_potitat = False

                # Grade buttoin
                if grade_button.is_pressed(mouse_pos, mouse_pressed): 
                    self.game.program_test = False
                    grade: int = self.game.grade_program(text_def, text_self, text_item, text_even, text_tuple)
                    self.game.grades['PRO'] = grade
                    in_potitat = False
                    if grade: self.game.talking("I did it!!")

                # Background
                self.game.screen.blit(bg, (0, 0))

                # Button
                self.game.screen.blit(back_button.image, back_button.rect)
                self.game.screen.blit(grade_button.image, grade_button.rect)

                # Def
                pygame.draw.rect(self.game.screen, color, fill_def) if active_def else None
                text_surface_def = self.game.lrob_font.render(text_def, True, (255, 255, 255))
                self.game.screen.blit(text_surface_def, (fill_def.x+1, fill_def.y-1))

                # Self
                pygame.draw.rect(self.game.screen, color, fill_self) if active_self else None
                text_surface_self = self.game.lrob_font.render(text_self, True, (255, 255, 255))
                self.game.screen.blit(text_surface_self, (fill_self.x+1, fill_self.y-1))

                # Item
                pygame.draw.rect(self.game.screen, color, fill_item) if active_item else None
                text_surface_item = self.game.lrob_font.render(text_item, True, (255, 255, 255))
                self.game.screen.blit(text_surface_item, (fill_item.x+1, fill_item.y-1))
                
                # Even
                pygame.draw.rect(self.game.screen, color, fill_even) if active_even else None
                text_surface_even = self.game.lrob_font.render(text_even, True, (255, 255, 255))
                self.game.screen.blit(text_surface_even, (fill_even.x+1, fill_even.y-1))
                
                # Tuple
                pygame.draw.rect(self.game.screen, color, fill_tuple) if active_tuple else None
                text_surface_tuple = self.game.lrob_font.render(text_tuple, True, (255, 255, 255))
                self.game.screen.blit(text_surface_tuple, (fill_tuple.x+1, fill_tuple.y-1))
                
                # Updates
                self.game.clock.tick(FPS)
                pygame.display.update()
                
    def check_suplovanie(self):
        """
        Player checks for the substitution, very yes
        """

        checking = True

        # Screen of the game
        bg = pygame.image.load("img/screen.png")

        # Phone
        iphone = pygame.image.load("img/mobile.png")

        # Screens
        first_screen = pygame.image.load("img/screenshot_first.png")
        first_rect = first_screen.get_rect(x=WIN_WIDTH // 2 - first_screen.get_width() // 2, y=WIN_HEIGHT // 2 - first_screen.get_height() // 2)
        second_screen = pygame.image.load("img/screenshot_second.png")
        second_rect = second_screen.get_rect(x=WIN_WIDTH // 2 - first_screen.get_width() // 2, y=WIN_HEIGHT // 2 - second_screen.get_height() // 2)

        # Button
        back_button = Button(500, 400, 120, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)

        # "Button"
        empty_rect = pygame.Rect(192, 319, 129, 23)
        back_rect = pygame.Rect(300, 420, 37, 29)

        main_app = True
        sub = False

        while checking:
            
            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: self.game.exiting()

                # Keyboard
                elif event.type == pygame.KEYDOWN:

                    # Esc
                    if event.key == pygame.K_ESCAPE: checking = False

                # Mouse
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    # Sub
                    if empty_rect.collidepoint(event.pos): main_app = not main_app; sub = not sub

                    # Back
                    elif back_rect.collidepoint(event.pos): checking = False; return False

            # Background
            self.game.screen.blit(bg, (0, 0))
                                                            
            self.game.screen.blit(iphone, (WIN_WIDTH // 2 - iphone.get_width() // 2, WIN_HEIGHT // 2 - iphone.get_height() // 2))
            
            if main_app: 
                self.game.screen.blit(first_screen, first_rect)
                pygame.draw.rect(self.game.screen, NAVY, empty_rect, 1)
            elif sub: 
                pygame.draw.rect(self.game.screen, BLACK, back_rect)
                self.game.screen.blit(second_screen, second_rect)

            # Back button
            if back_button.is_pressed(mouse_pos, mouse_pressed): checking = False
            self.game.screen.blit(back_button.image, back_button.rect)            

            # Updates
            self.game.clock.tick(FPS)
            pygame.display.update()