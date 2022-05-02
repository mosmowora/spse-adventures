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
        
        self.bench_done = bench_done
        grade: int = 5
        # Already did bench press
        if not self.bench_done: self.game.talking("I already did this."); return False
        
        # Bench press quest for stronk bois
        background = pygame.image.load("img/bench_press.png").convert()
        dumbbell = pygame.image.load("img/bench_press_dumbbell.png").convert_alpha()
        dumbbell_rect = dumbbell.get_rect(x=0, y=50)
        back_button = Button(500, 400, 120, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)
        looking: bool = True
        counter: int = 0
        push_strength: int = 20
        weak: bool = True
        
        while looking and counter < 5:
            
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
            if back_button.is_pressed(mouse_pos, mouse_pressed): looking = False; weak = True
            self.game.clock.tick(FPS)
            pygame.display.update()

        # Made it
        if counter in (1, 2, 3, 4, 5): 
            weak = False
            if grade - counter == 0: grade = 1
            else: grade -= counter
            
            self.game.grades["TSV - gym"] = grade

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
            color = DIM_GRAY

            # To fill
            fill_def = pygame.Rect(91, 90, 24, 13)
            fill_self = pygame.Rect(291, 91, 29, 13)
            fill_item = pygame.Rect(257, 233, 31, 12)
            fill_even = pygame.Rect(509, 232, 46, 12)
            fill_tuple = pygame.Rect(257, 257, 37, 13)
            
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
    
    
    # def function_to_bully_people(self):
    #     """
    #     This function needs your powers to fix it.
    #     It's part of a class.
    #     """

    #     add_even_to_list = [item for item in range(11) if item % 2 == 0]
    #     tuple_of_previous = tuple(add_even_to_list)
    #     return (item + 1 for item in tuple_of_previous)