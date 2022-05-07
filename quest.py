from turtle import color
import pygame
from config import *
from sprites import Button
from typing import List
import math

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

            t = str(round((pygame.time.get_ticks() - start) // 1000)) if len(str(round((pygame.time.get_ticks() - start) // 1000))) > 1 else "0" + str(round((pygame.time.get_ticks() - start) // 1000))
            time = self.game.font.render("0:" + t + " / 1:00", True, WHITE)
            time_rect = time.get_rect(x=525, y=10)

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
            self.game.screen.blit(time, time_rect)
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
                    elif back_rect.collidepoint(event.pos): checking = False; self.game.info("What day even is today?"); return False

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
            
    def open_window(self):
        """
        DSY quest to open windows but with a twist
        """
        
        if self.game.interacted[1] == 28 and self.game.interacted[2] in (28, 29):
            pass
            
        
        # Updates
        self.game.clock.tick(FPS)
        pygame.display.update()
    
    def anglictina(self):
        """
        ANJ Skusanie quest
        """

        testing: bool = True
        bg = pygame.image.load("img/anj_bg.png")
        word: int = 0
        
        assignment: List[str] = ["mail".upper(), "aardvark".upper(), "genetic".upper(), "desk".upper(), "religion".upper(), "keyboard".upper(), "iteration".upper(), "carbonated".upper(), "switch".upper(), "printer".upper()]
        assignment_answers: List[str] = ["posta", "mravciar", "geneticky", "lavica", "nabozentvo", "klavesnica", "iteracia", "perliva", "prepinac", "tlaciaren"]
        answer: List[str] = []
        answer_rect = pygame.Rect(155, 215, 302, 67)
        active: bool = False
        answer_text: str = ""

        # Button
        back_button = Button(500, 400, 120, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)
        paper = pygame.image.load("img/paper.png")
        paper_rect = paper.get_rect(x=20, y=0)
        assign_rect = pygame.Rect(151, 141, 273, 50)

        while testing:
            
            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Text of assignment
            assign: str = assignment[word]

            # Events
            for event in pygame.event.get():
                
                # Close button
                if event.type == pygame.QUIT: self.game.exiting()
            
                # Logic
                if pygame.KEYDOWN == event.type:

                    # Enter
                    if event.key == pygame.K_RETURN: word += 1; answer.append(answer_text); answer_text = ""

                    # Check for backspace
                    elif event.key == pygame.K_BACKSPACE: 
                        if active: answer_text = answer_text[:-1]

                    # Unicode
                    elif active: answer_text += event.unicode

                    # Escape
                    elif event.key == pygame.K_ESCAPE: testing = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    # Clicked
                    if answer_rect.collidepoint(event.pos): active = not active

            # Grading
            if word == len(assignment_answers):
                grade: int = 5 - math.floor(len(tuple(i for i in zip(assignment_answers, answer) if i[0] == i[1])) / 2)
                self.game.anj_test = False
                return grade if grade != 0 else 1, False

            # Background
            self.game.screen.blit(bg, (0, 0))

            # Button
            self.game.screen.blit(back_button.image, back_button.rect)

            # Paper
            self.game.screen.blit(paper, paper_rect)

            # Text
            text_surface_answer = self.game.big_font.render(answer_text, True, BLACK)
            pygame.draw.rect(self.game.screen, BRITISH_WHITE, answer_rect)
            self.game.screen.blit(text_surface_answer, (answer_rect.x+5, answer_rect.y+5))
            assing_text_surface = self.game.font.render(assign, True, BLACK)
            self.game.screen.blit(assing_text_surface, (assign_rect.x+100, assign_rect.y+5))
            answer_text_surface = self.game.font.render(str(word + 1) + "/10", True, BLACK)
            self.game.screen.blit(answer_text_surface, (assign_rect.x+230, assign_rect.y-50))

            # Button pressed
            if back_button.is_pressed(mouse_pos, mouse_pressed): testing = not testing; return True

            # Updates
            self.game.clock.tick(FPS)
            pygame.display.update()

    def router(self): 
        """
        Connecting router\n
        If someone knows how to make it look like they are connected pls do cause I don't want to think
        """

        connecting = True
        exited = False

        # Background
        bg = pygame.image.load("img/router.png")

        # Button
        back_button = Button(10, 400, 120, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)
        done_button = Button(500, 400, 120, 50, fg=WHITE, bg=BLACK, content="Done", fontsize=32)

        # Clickable router
        a1 = pygame.Rect(313, 330, 35, 33)
        a2 = pygame.Rect(348, 330, 33, 33)
        a3 = pygame.Rect(381, 330, 34, 33)
        a4 = pygame.Rect(415, 330, 34, 33)
        ans = 0
        answers = [0, 0, 0, 0]

        # Cables
        start1 = (232, 112)
        start2  = (312, 112)
        start3 = (392, 112)
        start4 = (472, 112)
        end1 = (232, 112)
        end2  = (312, 112)
        end3 = (392, 112)
        end4 = (472, 112)
        ends = [end1, end2, end3, end4]
        first_rect = pygame.Rect(200, 80, 64, 64)
        second_rect = pygame.Rect(280, 80, 64, 64)
        third_rect = pygame.Rect(360, 80, 64, 64)
        fourth_rect = pygame.Rect(440, 80, 64, 64)

        # 023
        if self.game.saved_room_data == "023":

            # Router
            first_text = self.game.font.render("W", True, WHITE)
            second_text = self.game.font.render("B", True, BLUE)
            third_text = self.game.font.render("R", True, RED)
            fourth_text = self.game.font.render("G", True, GREEN)    

            # Colors
            colors = [WHITE, BLUE, RED, GREEN]

            # Correct
            correct = [1, 3, 4, 2]

        # 130
        elif self.game.saved_room_data == "130":

            # Router
            first_text = self.game.font.render("G", True, GREEN)
            second_text = self.game.font.render("W", True, WHITE)
            third_text = self.game.font.render("B", True, BLUE)
            fourth_text = self.game.font.render("R", True, RED)    

            # Colors
            colors = [GREEN, WHITE, BLUE, RED]

            # Correct
            correct = [2, 4, 1, 3]

        # 217
        elif self.game.saved_room_data == "217":

            # Router
            first_text = self.game.font.render("R", True, RED)
            second_text = self.game.font.render("G", True, GREEN)
            third_text = self.game.font.render("B", True, BLUE)
            fourth_text = self.game.font.render("W", True, WHITE)    

            # Colors
            colors = [RED, GREEN, BLUE, WHITE]

            # Correct
            correct = [3, 1, 2, 4]

        # 402
        elif self.game.saved_room_data == "402":

            # Route
            first_text = self.game.font.render("B", True, BLUE)
            second_text = self.game.font.render("R", True, RED)
            third_text = self.game.font.render("G", True, GREEN)
            fourth_text = self.game.font.render("W", True, WHITE)    

            # Colors
            colors = [BLUE, RED, GREEN, WHITE]

            # Correct
            correct = [4, 2, 3, 1]

        while connecting and self.game.saved_room_data not in self.game.connected_router:

            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Buttons pressed
            if back_button.is_pressed(mouse_pos, mouse_pressed): connecting = False; exited = True
            if done_button.is_pressed(mouse_pos, mouse_pressed): connecting = False

            # Events
            for event in pygame.event.get():
                
                # Close button
                if event.type == pygame.QUIT: self.game.exiting()

                # Keyboard
                if pygame.KEYDOWN == event.type:

                    # Escape
                    if event.key == pygame.K_ESCAPE: connecting = False; exited = True

                    # Enter
                    if event.key == pygame.K_RETURN: connecting = False

                # Mouse
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    
                    # First rect
                    if first_rect.collidepoint(event.pos): ans = 1

                    # Second rect
                    elif second_rect.collidepoint(event.pos): ans = 2

                    # Third rect
                    elif third_rect.collidepoint(event.pos): ans = 3

                    # Fourth rect
                    elif fourth_rect.collidepoint(event.pos): ans = 4

                    # First rect
                    elif a1.collidepoint(event.pos): 
                        if ans != 0: answers[ans-1] = 1; ends[ans-1] = (330, 346)

                    # Second rect
                    elif a2.collidepoint(event.pos):
                        if ans != 0: answers[ans-1] = 2; ends[ans-1] = (364, 346)

                    # Third rect
                    elif a3.collidepoint(event.pos):
                        if ans != 0: answers[ans-1] = 3; ends[ans-1] = (398, 346)

                    # Fourth rect
                    elif a4.collidepoint(event.pos):
                        if ans != 0: answers[ans-1] = 4; ends[ans-1] = (432, 346)

            # Background
            self.game.screen.blit(bg, (0, 0))

            # Button
            self.game.screen.blit(back_button.image, back_button.rect)
            self.game.screen.blit(done_button.image, done_button.rect)

            # Clickable router
            pygame.draw.rect(self.game.screen, (94.9, 82, 40.4), a1, 1)
            pygame.draw.rect(self.game.screen, (94.9, 82, 40.4), a2, 1)
            pygame.draw.rect(self.game.screen, (94.9, 82, 40.4), a3, 1)
            pygame.draw.rect(self.game.screen, (94.9, 82, 40.4), a4, 1)

            # Text
            self.game.screen.blit(first_text, (323, 305))
            self.game.screen.blit(second_text, (356, 305))
            self.game.screen.blit(third_text, (389, 305))
            self.game.screen.blit(fourth_text, (422, 305))

            # Cables
            pygame.draw.rect(self.game.screen, colors[correct[0]-1], first_rect)
            pygame.draw.rect(self.game.screen, colors[correct[1]-1], second_rect)
            pygame.draw.rect(self.game.screen, colors[correct[2]-1], third_rect)
            pygame.draw.rect(self.game.screen, colors[correct[3]-1], fourth_rect)

            # Cables
            pygame.draw.line(self.game.screen, BLACK, start1, ends[0], 5)
            pygame.draw.line(self.game.screen, BLACK, start2, ends[1], 5)
            pygame.draw.line(self.game.screen, BLACK, start3, ends[2], 5)
            pygame.draw.line(self.game.screen, BLACK, start4, ends[3], 5)

            # Updates
            self.game.clock.tick(FPS)
            pygame.display.update()

        if exited: return "I rather leave it be."
        else: 
            if answers == correct: return self.game.saved_room_data 
            elif self.game.saved_room_data in self.game.connected_router: return "I already connected this."
            else: return "There is something wrong."