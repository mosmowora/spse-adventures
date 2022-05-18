import pygame
from config import *
from sprites import Button
from typing import List
import math, random as r

class Quest:
    
    def __init__(self, game):
        """
        Make more complex quests here.
        """

        self.game = game
        self.things_to_buy = {"level_teleporter": (pygame.image.load("img/amper_teleporter.png"), 25), "referat": (pygame.image.load("img/amper_referat.png"), 30)}
    
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
            
            self.game.info("You've recieved a grade for TSV", WHITE, 90)
            self.game.grades["TSV"] = grade

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
                    self.game.info("You've recieved a grade for PRO")
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
        second_rect = second_screen.get_rect(x=WIN_WIDTH // 2 - second_screen.get_width() // 2, y=WIN_HEIGHT // 2 - second_screen.get_height() // 2)
        grades_one = pygame.image.load("img/grades_first.png")
        grades_one_rect = grades_one.get_rect(x=WIN_WIDTH // 2 - grades_one.get_width() // 2, y=WIN_HEIGHT // 2 - grades_one.get_height() // 2)
        grades_two = pygame.image.load("img/grades_second.png")
        grades_two_rect = grades_two.get_rect(x=WIN_WIDTH // 2 - grades_two.get_width() // 2, y=WIN_HEIGHT // 2 - grades_two.get_height() // 2)

        # Button
        back_button = Button(500, 400, 120, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)

        # "Button"
        empty_rect = pygame.Rect(193, 320, 127, 21)
        back_rect = pygame.Rect(302, 422, 36, 22)
        grade_rect = pygame.Rect(193, 245, 127, 24)

        main_app = True
        sub = False
        grades_app = False
        up = True

        # Grades
        grades_to_write = {
            "SJL": 0,
            "ANJ": 0,
            "DEJ": 0,
            "OBN": 0,
            "MAT": 0,
            "TSV": 0,
            "PRO": 0,
            "SIE": 0,
            "ICD": 0,
            "OSY": 0,
            "AEN": 0,
            "IOT": 0,
            "DSY": 0
        }

        # From dictionary
        for i in self.game.grades: grades_to_write[i] = self.game.grades[i]

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

                    # Down
                    elif event.key == pygame.K_DOWN and grades_app: up = False

                    # Up
                    elif event.key == pygame.K_UP and grades_app: up = True

                # Mouse
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    # Sub
                    if empty_rect.collidepoint(event.pos): main_app = not main_app; sub = not sub

                    # Back
                    elif back_rect.collidepoint(event.pos): 
                        if main_app: checking = False; self.game.info("What day even is today?", BRITISH_WHITE); return False
                        elif sub: main_app = not main_app; sub = not sub
                        elif grades_app: main_app = not main_app; grades_app = not grades_app

                    # Grades
                    elif grade_rect.collidepoint(event.pos): main_app = not main_app; grades_app = not grades_app

            # Background
            self.game.screen.blit(bg, (0, 0))
                                                            
            self.game.screen.blit(iphone, (WIN_WIDTH // 2 - iphone.get_width() // 2, WIN_HEIGHT // 2 - iphone.get_height() // 2))
            
            pygame.draw.rect(self.game.screen, BLACK, back_rect)

            # Main app
            if main_app: 
                self.game.screen.blit(first_screen, first_rect)
                pygame.draw.rect(self.game.screen, NAVY, empty_rect, 1)
                pygame.draw.rect(self.game.screen, NAVY, grade_rect, 1)

            # Substitution
            elif sub: self.game.screen.blit(second_screen, second_rect)

            # Grades
            elif grades_app: 
                if up: self.game.screen.blit(grades_one, grades_one_rect); self.render_grades(up, grades_to_write)
                elif not up: self.game.screen.blit(grades_two, grades_two_rect); self.render_grades(up, grades_to_write)
                

            # Back button
            if back_button.is_pressed(mouse_pos, mouse_pressed): checking = False
            self.game.screen.blit(back_button.image, back_button.rect)       

            # Updates
            self.game.clock.tick(FPS)
            pygame.display.update()
            
    def render_grades(self, up, grades):
        """
        Renders grades in EduPage
        """

        n = 0

        # SJL, ANJ, DEJ, OBN, MAT, TSV, PRO
        if up:
            for i in grades: 
                self.game.screen.blit(self.game.font.render(str(grades[i]), True, WHITE), (425, 97 + 44 * n)); n += 1
                if n == 7: break

        # PRO, SIE, ICDL, OSY, AEN, IOT, DSY
        elif not up:
            for i in grades:
                if n > 5: self.game.screen.blit(self.game.font.render(str(grades[i]), True, WHITE), (425, 97 + 44 * (n - 6)))
                n += 1

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
        
        # Answers/Questions
        assignment: List[str] = ["mail".upper(), "aardvark".upper(), "genetic".upper(), "desk".upper(), "religion".upper(), "keyboard".upper(), "iteration".upper(), "carbonated".upper(), "switch".upper(), "printer".upper()]
        assignment_answers: List[str] = ["posta", "mravciar", "geneticky", "lavica", "nabozentvo", "klavesnica", "iteracia", "perliva", "prepinac", "tlaciaren"]
        answer: List[str] = []
        answer_rect = pygame.Rect(155, 215, 302, 67)
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
                    elif event.key == pygame.K_BACKSPACE: answer_text = answer_text[:-1]

                    # Escape
                    elif event.key == pygame.K_ESCAPE: testing = False

                    # Unicode
                    else: answer_text += event.unicode

            # Grading
            if word == len(assignment_answers):
                grade: int = 5 - math.floor(len(tuple(i for i in zip(assignment_answers, answer) if i[0] == i[1])) / 2)
                self.game.anj_test = False
                self.game.info("You've recieved a grade for ANJ", DIM_GRAY)
                return grade if grade != 0 else 1, False

            # Background
            self.game.screen.blit(bg, (0, 0))

            # Button
            self.game.screen.blit(back_button.image, back_button.rect)

            # Paper
            self.game.screen.blit(paper, paper_rect)

            # Text
            text_surface_answer = self.game.big_font.render(answer_text, True, BLACK)
            pygame.draw.rect(self.game.screen, PAPER_WHITE, answer_rect)
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
    
    def slovak_bs(self):
        """
        SJL quest
        """

        testing: bool = True
        bg = pygame.image.load("img/sjl_bg.png")
        word: int = 0
        
        # Answers/Questions
        assignment: List[str] = ["Ako __ má babička?".upper(), "Čo __ __ večer?".upper(), "__ máš namierené?".upper(), "V diaľke som videl lietať v_ra".upper(), "Kr_štálový".upper(), "prer_vaný".upper(), "__ Botto".upper(), "materinský".upper(), "ˇ%053!4P3%!".upper(), "1#!@%^d6n".upper()]
        assignment_answers: List[str] = ["sa", "budeš robiť", "kam", "ý", "y", "ý", "Ján", "jazyk", "/(§)\\", "LK:{DA"]
        answer: List[str] = []
        answer_rect = pygame.Rect(155, 215, 302, 67)
        answer_text: str = ""

        # Button
        back_button = Button(500, 400, 120, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)
        paper = pygame.image.load("img/paper.png")
        paper_rect = paper.get_rect(x=20, y=0)
        assign_rect = pygame.Rect(61, 141, 273, 50)

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
                    elif event.key == pygame.K_BACKSPACE: answer_text = answer_text[:-1]

                    # Escape
                    elif event.key == pygame.K_ESCAPE: testing = False

                    # Unicode
                    else: answer_text += event.unicode

            # Grading
            if word == len(assignment_answers):
                grade: int = 5 - math.floor(len(tuple(i for i in zip(assignment_answers, answer) if i[0] == i[1])) / 2)
                self.game.sjl_test = False
                self.game.info("You've recieved a grade for SJL", DIM_GRAY)
                return grade if grade != 0 else 1, False

            # Background
            self.game.screen.blit(bg, (0, 0))

            # Button
            self.game.screen.blit(back_button.image, back_button.rect)

            # Paper
            self.game.screen.blit(paper, paper_rect)

            # Text
            text_surface_answer = self.game.big_font.render(answer_text, True, BLACK)
            pygame.draw.rect(self.game.screen, PAPER_WHITE, answer_rect)
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
            
    def obn_testo(self):
        """
        High effort quest, obn skusanie
        """
        
        obning: bool = True
        
        # Button
        back_button = Button(10, 400, 120, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)
        done_button = Button(500, 400, 120, 50, fg=WHITE, bg=BLACK, content="Done", fontsize=32)

        
        # active
        active_text: bool = True

        # To fill
        fill_ans = pygame.Rect(10, 150, 200, 40)
        
        # text
        text_ans = ""
        
        # Question counter
        guesses = 0
        
        # Points
        p = 0
        
        # Answers
        answer: List[str] = ["ambutsman", "27", "zuzana caputova", "slovenska republika", "prvej"]
        
        # Guess
        guess: List[str] = []
        
        # Questions
        questions: List[str] = ["Advokat po svedsky?", "Kolko je statov v EU?", "Kto je prezident SR?", "Co znamena skratka SR?", "Pravo na zivot parti medzi prava ktorej generacie?"]
        
        # Bools to control text blitted
        # first = True
        # second = False
        # third = False
        # fourth = False
        # fifth = False
        
        

        # Button
        back_button = Button(10, 400, 120, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)
        assign: str = questions[guesses]
         

        while obning:
            

            
            # Question
            
            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: self.game.exiting()

                # Click
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if fill_ans.collidepoint(event.pos): active_text = True
                    else: active_text = False
                    
                # Keyboard
                if event.type == pygame.KEYDOWN:
    
                    # Esc
                    if event.key == pygame.K_ESCAPE: obning = False
                    
                    # Enter
                    if event.key == pygame.K_RETURN and guesses < 4: guesses += 1; self.game.draw(); self.game.update(); guess.append(text_ans); text_ans = ""; assign: str = questions[guesses]
                    elif event.key == pygame.K_RETURN and guesses == 4: guesses += 1; self.game.draw(); self.game.update(); guess.append(text_ans)

                    # Check for backspace
                    elif event.key == pygame.K_BACKSPACE: 
                        if active_text: text_ans = text_ans[:-1]

                    elif active_text: text_ans += event.unicode

            # Back button
            if back_button.is_pressed(mouse_pos, mouse_pressed): obning = False

            # Grading
            if guesses == len(questions): 
                obning = False
                for i in range(len(guess)):
                    if guess[i].lower() == answer[i]: p += 1
                if p == 5: return 1
                elif p == 4: return 2
                elif p == 3: return 3
                elif p == 2: return 4
                else: return 5
                


            # Button
            self.game.screen.blit(back_button.image, back_button.rect)

            # Text stuff
            pygame.draw.rect(self.game.screen, BLACK, fill_ans) if active_text else None
            text_surface = self.game.font.render(text_ans, True, (255, 255, 255))
            self.game.screen.blit(text_surface, (fill_ans.x+5, fill_ans.y+5))
            
            question = self.game.font.render(assign, True, RED)
            
            self.game.screen.blit(question, (10, 10))
            
            # Updates
            self.game.clock.tick(FPS)
            pygame.display.update()
        pygame.delay(600)
        
    
    def maths(self):
        """
        MAT quest
        """

        testing: bool = True
        bg = pygame.image.load("img/maths_bg.png")
        word: int = 0
        
        # Answers/Questions
        assignment: List[str] = ["10x - 1 = 15 - 6x".upper(), "9x - 8 = 11x - 10".upper(), "7 + x/3 = 8 + x/4".upper(), "x/2 + x/3 = 5".upper(), "x - 2/3 = 5x/7 + 1/2".upper(), "2x - x/2 + 4 = x + x/3".upper(), "5x - 9 - 4/15 = (2x - 1)/3".upper(), "-1 - (3x - x)/4 = (2x - 5)/6".upper(), "(-17/19)x + 51 = 0".upper(), "|x - 7| = 0".upper()]
        assignment_answers: List[str] = ["1", "1", "12", "6", "49/12", "-24", "3/5", "-1/5", "57", "7"]
        
        # print(assignment_answers) # for maths quest debugging
        answer: List[str] = []
        answer_rect = pygame.Rect(155, 215, 302, 67)
        answer_text: str = ""

        # Button
        back_button = Button(500, 400, 120, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)
        paper = pygame.image.load("img/paper.png")
        paper_rect = paper.get_rect(x=20, y=0)
        assign_rect = pygame.Rect(81, 141, 273, 50)

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
                    elif event.key == pygame.K_BACKSPACE: answer_text = answer_text[:-1]

                    # Escape
                    elif event.key == pygame.K_ESCAPE: testing = False

                    # Unicode
                    else: answer_text += event.unicode

            # Grading
            if word == len(assignment_answers):
                grade: int = 5 - math.floor(len(tuple(i for i in zip(assignment_answers, answer) if i[0] == i[1])) / 2)
                self.game.mat_test = False
                self.game.info("You've recieved a grade for MAT", DIM_GRAY)
                return grade if grade != 0 else 1, False

            # Background
            self.game.screen.blit(bg, (0, 0))

            # Button
            self.game.screen.blit(back_button.image, back_button.rect)

            # Paper
            self.game.screen.blit(paper, paper_rect)

            # Text
            text_surface_answer = self.game.big_font.render(answer_text, True, BLACK)
            pygame.draw.rect(self.game.screen, PAPER_WHITE, answer_rect)
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

        while connecting:

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
            else: return "There is something wrong."
            
    def resistor(self): 
        """
        Connecting resistor stuff
        """

        resisting = True
        gave_up = False

        # Background
        bg = pygame.image.load("img/resistor.png")

        # Button
        back_button = Button(10, 400, 120, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)
        done_button = Button(500, 400, 120, 50, fg=WHITE, bg=BLACK, content="Done", fontsize=32)

        # Clickable 
        a1 = pygame.Rect(51, 315, 50, 22)
        a2 = pygame.Rect(465, 318, 100, 22)

        ans = 0
        answers = [0, 0]

        # Cables
        start1 = (64, 177)
        start2  = (116, 177)
        end1 = (64, 177)
        end2  = (116, 177)
        ends = [end1, end2]
        first_rect = pygame.Rect(54, 167, 20, 20)
        second_rect = pygame.Rect(106, 167, 20, 20)

        # Text
        first_text = self.game.font.render("+", True, RED)
        second_text = self.game.font.render("-", True, BLACK)

        # Colors
        colors = [RED, BLACK]

        # Correct
        correct = [1, 2]

        while resisting:

            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Buttons pressed
            if back_button.is_pressed(mouse_pos, mouse_pressed): resisting = False; gave_up = True
            if done_button.is_pressed(mouse_pos, mouse_pressed): resisting = False

            # Events
            for event in pygame.event.get():
                
                # Close button
                if event.type == pygame.QUIT: self.game.exiting()

                # Keyboard
                if pygame.KEYDOWN == event.type:

                    # Escape
                    if event.key == pygame.K_ESCAPE: resisting = False; gave_up = True

                    # Enter
                    if event.key == pygame.K_RETURN: resisting = False

                # Mouse
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    
                    # First rect
                    if first_rect.collidepoint(event.pos): ans = 1

                    # Second rect
                    elif second_rect.collidepoint(event.pos): ans = 2

                    # First rect
                    elif a1.collidepoint(event.pos): 
                        if ans != 0: answers[ans-1] = 1; ends[ans-1] = (58, 324)

                    # Second rect
                    elif a2.collidepoint(event.pos):
                        if ans != 0: answers[ans-1] = 2; ends[ans-1] = (550, 318)

            # Background
            self.game.screen.blit(bg, (0, 0))

            # Button
            self.game.screen.blit(back_button.image, back_button.rect)
            self.game.screen.blit(done_button.image, done_button.rect)

            # Clickable poles
            pygame.draw.rect(self.game.screen, (133, 133, 133), a1, 1)
            pygame.draw.rect(self.game.screen, (133, 133, 133), a2, 1)

            # Text
            self.game.screen.blit(first_text, (55, 314))
            self.game.screen.blit(second_text, (550, 318))

            # Cables
            pygame.draw.circle(self.game.screen, colors[correct[0]-1], (64, 177), 10)
            pygame.draw.circle(self.game.screen, colors[correct[1]-1], (116, 177), 10)

            # Cables
            pygame.draw.line(self.game.screen, RED, start1, ends[0], 5)
            pygame.draw.line(self.game.screen, BLACK, start2, ends[1], 5)

            # Updates
            self.game.clock.tick(FPS)
            pygame.display.update()

        # Grading   
        if gave_up: return 5
        else: 
            if answers == correct: return 1
            else: return 3
            
    def bash(self):
        """
        (č) OSYYYYY
        """


        bashing = True

        # Background
        bg = pygame.image.load("img/OSY.png")
        
        # active
        active_bash = True

        # To fill
        fill_bash = pygame.Rect(103, 147, 96, 13)
        
        # text
        text_bash = ""
        
        # Button
        back_button = Button(10, 400, 120, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)
        grade_button = Button(500, 400, 120, 50, fg=WHITE, bg=BLACK, content="Grade", fontsize=32)
        
        # Info 
        info_text = self.game.font.render("Tell linux to use bash", True, BLACK)

        while bashing:
            
            
            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: self.game.exiting()

                # Click
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if fill_bash.collidepoint(event.pos): active_bash = True
                    else: active_bash = False
                    
                # Keyboard
                if event.type == pygame.KEYDOWN:
    
                    # Esc
                    if event.key == pygame.K_ESCAPE: bashing = False

                    # Check for backspace
                    elif event.key == pygame.K_BACKSPACE: 
                        if active_bash: text_bash = text_bash[:-1]

                    elif active_bash: text_bash += event.unicode


            # Back button
            if back_button.is_pressed(mouse_pos, mouse_pressed): bashing = False

            # Grade button
            elif grade_button.is_pressed(mouse_pos, mouse_pressed): 
                bashing = False
                if text_bash == "!#/bin/bash": return 1
                else: return 3


            # Background
            self.game.screen.blit(bg, (0, 0))
            
            # Very useful info text
            self.game.screen.blit(info_text, (10, 10))

            # Button
            self.game.screen.blit(back_button.image, back_button.rect)
            self.game.screen.blit(grade_button.image, grade_button.rect)

            # Bash
            pygame.draw.rect(self.game.screen, BLACK, fill_bash) if active_bash else None
            text_surface_def = self.game.lrob_font.render(text_bash, True, (4.20, 169, 4.20))
            self.game.screen.blit(text_surface_def, (fill_bash.x+1, fill_bash.y-1))
            
            # Updates
            self.game.clock.tick(FPS)
            pygame.display.update()
            
    def iotest(self): 
        """
        Iot edupage test
        """

        ioting = True

        # Background
        bg = pygame.image.load("img/iot.png")

        # Button
        back_button = Button(10, 400, 120, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)
        done_button = Button(500, 400, 120, 50, fg=WHITE, bg=BLACK, content="Done", fontsize=32)

        # Anwer button
        a_button = Button(101, 145, 25, 27, fg=BLACK, bg=WHITE, content="a)", fontsize=20)
        b_button = Button(101, 192, 25, 27, fg=BLACK, bg=WHITE, content="b)", fontsize=20)
        c_button = Button(101, 238, 25, 27, fg=BLACK, bg=WHITE, content="c)", fontsize=20)
        d_button = Button(101, 286, 25, 27, fg=BLACK, bg=WHITE, content="d)", fontsize=20)

        # Counters for pressed buttons
        a = False
        b = False
        c = False
        d = False

        while ioting:

            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Buttons pressed
            if back_button.is_pressed(mouse_pos, mouse_pressed): ioting = False; return 5
            if done_button.is_pressed(mouse_pos, mouse_pressed): ioting = False; return grade

            # CSS for active buttons (extremely scuffed)

            # Anwer A
            if a_button.is_pressed(mouse_pos, mouse_pressed): 
                if a: a_button = Button(101, 145, 25, 27, fg=BLACK, bg=WHITE, content="a)", fontsize=20); a = False; pygame.time.delay(200)
                else:
                    a_button = Button(101, 145, 25, 27, fg=WHITE, bg=GREEN, content="a)", fontsize=20)
                    b_button = Button(101, 192, 25, 27, fg=BLACK, bg=WHITE, content="b)", fontsize=20)
                    c_button = Button(101, 238, 25, 27, fg=BLACK, bg=WHITE, content="c)", fontsize=20)
                    d_button = Button(101, 286, 25, 27, fg=BLACK, bg=WHITE, content="d)", fontsize=20)
                    a = True

                    # Grade
                    grade = 1
                    pygame.time.delay(200)

            # Answer B
            if b_button.is_pressed(mouse_pos, mouse_pressed): 
                if b: b_button = Button(101, 192, 25, 27, fg=BLACK, bg=WHITE, content="b)", fontsize=20); b = False; pygame.time.delay(200)
                else:
                    a_button = Button(101, 145, 25, 27, fg=BLACK, bg=WHITE, content="a)", fontsize=20)
                    b_button = Button(101, 192, 25, 27, fg=WHITE, bg=GREEN, content="b)", fontsize=20)  
                    c_button = Button(101, 238, 25, 27, fg=BLACK, bg=WHITE, content="c)", fontsize=20)
                    d_button = Button(101, 286, 25, 27, fg=BLACK, bg=WHITE, content="d)", fontsize=20)    
                    b = True

                    # Grade             
                    grade = 3
                    pygame.time.delay(200)

            # Answer C
            if c_button.is_pressed(mouse_pos, mouse_pressed): 
                if c: c_button = Button(101, 238, 25, 27, fg=BLACK, bg=WHITE, content="c)", fontsize=20); c = False; pygame.time.delay(200)
                else:
                    a_button = Button(101, 145, 25, 27, fg=BLACK, bg=WHITE, content="a)", fontsize=20)
                    b_button = Button(101, 192, 25, 27, fg=BLACK, bg=WHITE, content="b)", fontsize=20)
                    c_button = Button(101, 238, 25, 27, fg=WHITE, bg=GREEN, content="c)", fontsize=20)
                    d_button = Button(101, 286, 25, 27, fg=BLACK, bg=WHITE, content="d)", fontsize=20)
                    c = True

                    # Grade
                    grade = 3
                    pygame.time.delay(200)

            # Answer D
            if d_button.is_pressed(mouse_pos, mouse_pressed): 
                if d: d_button = Button(101, 286, 25, 27, fg=BLACK, bg=WHITE, content="d)", fontsize=20); d = False; pygame.time.delay(200)
                else:
                    a_button = Button(101, 145, 25, 27, fg=BLACK, bg=WHITE, content="a)", fontsize=20)
                    b_button = Button(101, 192, 25, 27, fg=BLACK, bg=WHITE, content="b)", fontsize=20)
                    c_button = Button(101, 238, 25, 27, fg=BLACK, bg=WHITE, content="c)", fontsize=20)
                    d_button = Button(101, 286, 25, 27, fg=WHITE, bg=GREEN, content="d)", fontsize=20)
                    d = True

                    # Grade
                    grade = 3
                    pygame.time.delay(200)
            

            # Events
            for event in pygame.event.get():
                
                # Close button
                if event.type == pygame.QUIT: self.game.exiting()

                # Keyboard
                if pygame.KEYDOWN == event.type:

                    # Escape
                    if event.key == pygame.K_ESCAPE: ioting = False; return 5

                    # Enter
                    if event.key == pygame.K_RETURN: ioting = False


            # Background
            self.game.screen.blit(bg, (0, 0))

            # Button
            self.game.screen.blit(back_button.image, back_button.rect)
            self.game.screen.blit(done_button.image, done_button.rect)
            self.game.screen.blit(a_button.image, a_button.rect)
            self.game.screen.blit(b_button.image, b_button.rect)
            self.game.screen.blit(c_button.image, c_button.rect)
            self.game.screen.blit(d_button.image, d_button.rect)

            # Updates
            self.game.clock.tick(FPS)
            pygame.display.update()

    def haram(self):
        """
        Haramgozo likes to bully his students\n
        Sometimes the answer is weird (2.7800000000000002 i.e) Idk why. pls fix :pray:
        """

        pygame.mixer.Sound.play(self.game.wrong_house)

        # Talk before
        self.game.talking("You picked the wrong classroom fool!", True, RED)
        pygame.time.delay(400)
        self.game.talking("I am gonna test your knowledge on resistors.", True, RED)
        self.game.talking("Don't forget the unit.", True, RED)

        haraming = True
        test = 0
        points = 0

        colors_values = [(NEARLY_BLACK, 0), (BROWN, 1), (RED, 2), (ORANGE, 3), (YELLOW, 4), (GREEN, 5), (BLUE, 6), (VIOLET, 7), (GRAY, 8), (WHITE, 9)]
        colors_multi = [(PINK, -3), (SILVER, -2), (GOLD, -1), (NEARLY_BLACK, 0), (BROWN, 1), (RED, 2), (ORANGE, 3), (YELLOW, 4), (GREEN, 5), (BLUE, 6), (VIOLET, 7), (GRAY, 8), (WHITE, 9)]

        # Background
        bg = pygame.image.load("img/resistor_test.png")

        # Answer rect
        answer_rect = pygame.Rect(150, 100, 314, 72)

        # Clickable
        ohm = pygame.Rect(350, 100, 115, 72)
        number = pygame.Rect(150, 100, 200, 72)

        while test < 10:

            # Choosing values
            first = (NEARLY_BLACK, 0)
            while first == (NEARLY_BLACK, 0):
                first = r.choice(colors_values)
            second = r.choice(colors_values)
            third = r.choice(colors_values)
            fourth = r.choice(colors_multi)

            # Rectangles
            first_rect = pygame.Rect(175, 293, 32, 72)
            second_rect = pygame.Rect(220, 293, 32, 72)
            third_rect = pygame.Rect(265, 293, 32, 72)
            fourth_rect = pygame.Rect(310, 293, 32, 72)

            correct_answer = str(float(str(first[1]) + str(second[1]) + str(third[1])) * (10 ** fourth[1]))
            player_answer = ""
            units = ["mOHM", "OHM", "kOHM", "MOHM", "GOHM"]
            unit = 1

            while haraming:
            
                # Events
                for event in pygame.event.get():
                    
                    # Close button
                    if event.type == pygame.QUIT: self.game.saved_room_data = "Hall"; self.game.exiting()

                    # Keyboard
                    if event.type == pygame.KEYDOWN:

                        # Arrow up
                        if event.key == pygame.K_UP: 
                            if unit < len(units) - 1: unit += 1

                        elif event.key == pygame.K_DOWN:
                            if unit != 0: unit -= 1

                        # Enter
                        elif event.key == pygame.K_RETURN and player_answer.isnumeric(): 
                            test += 1
                            match unit:
                                case 0: 
                                    if str(float(player_answer) / 1000) == correct_answer: points += 1
                                case 1:
                                    if str(float(player_answer)) == correct_answer: points += 1
                                case 2: 
                                    if str(float(player_answer) * 1000) == correct_answer: points += 1
                                case 3: 
                                    if str(float(player_answer) * 1000000) == correct_answer: points += 1
                                case 4: 
                                    if str(float(player_answer) * 1000000000) == correct_answer: points += 1
                            haraming = False
                        elif event.key == pygame.K_RETURN and player_answer.isalpha(): player_answer = ""; test += 1; haraming = False
                        

                        # Check for backspace
                        elif event.key == pygame.K_BACKSPACE: player_answer = player_answer[:-1]

                        # Unicode
                        else: player_answer += event.unicode


                # Background
                self.game.screen.blit(bg, (0, 0))

                # Rectangles
                pygame.draw.rect(self.game.screen, first[0], first_rect)
                pygame.draw.rect(self.game.screen, second[0], second_rect)
                pygame.draw.rect(self.game.screen, third[0], third_rect)
                pygame.draw.rect(self.game.screen, fourth[0], fourth_rect)

                # Clickable
                pygame.draw.rect(self.game.screen, WHITE, number, 1)
                pygame.draw.rect(self.game.screen, WHITE, ohm, 1)

                # Text
                text_surface_answer = self.game.big_font.render(player_answer, True, BLACK)
                pygame.draw.rect(self.game.screen, WHITE, answer_rect)
                self.game.screen.blit(self.game.big_font.render(units[unit], True, BLACK), (answer_rect.x+210, answer_rect.y+5))
                self.game.screen.blit(text_surface_answer, (answer_rect.x+5, answer_rect.y+5))


                # Updates
                self.game.clock.tick(FPS)
                pygame.display.update()

            haraming = True
            
        # After test talk
        self.game.draw(); self.game.update()

        # Everything correct
        if points == 10: self.game.talking("I-Impossible. You got everything correct.", True, RED)

        # Atleast something correct
        elif 5 <= points < 10: self.game.talking("You knew at least something. Great", True, RED)

        # Nearly nothing
        elif points <= 5: self.game.talking("What did I expect? Students actually knowing something?", True, RED)

        # Bananky
        self.game.talking("Here, take these bananky as reward for taking the test.", True, RED) if points > 0 else self.game.talking("I am not giving you any bananky for this.", True, RED)
        if "bananok" in self.game.inv.keys(): self.game.number_bananok += points * 5
        else: self.game.inv["bananok"] = "img/bananok.png"; self.game.number_bananok += points * 5

        # Return
        return False

    def amper(self):
        """
        Shopping in Amper
        """

        shopping = True
        link: int = 0
        buy = Button(500, 400, 120, 50, fg=WHITE, bg=BLACK, content="BUY", fontsize=32)
        
        # Background
        bg = pygame.image.load("img/amper_background.png")

        if len(self.things_to_buy) != 0:
            while shopping:
    
                # Position and click of the mouse
                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()
                
                # Events
                for event in pygame.event.get():

                    # Close button
                    if event.type == pygame.QUIT: self.game.exiting()
                        
                    # Keyboard
                    if event.type == pygame.KEYDOWN:
        
                        # Esc
                        if event.key == pygame.K_ESCAPE: shopping = False
                        
                        # Arrows
                        elif event.key == pygame.K_RIGHT and link < len(self.things_to_buy) - 1: link += 1
                        elif event.key == pygame.K_LEFT and link > 0: link -= 1 

                # Background
                self.game.screen.blit(bg, (0, 0))
                self.game.screen.blit(self.game.big_font.render(list(self.things_to_buy.keys())[link], True, WHITE), (10, 5))
                self.game.screen.blit(self.game.big_font.render("Cost: " + str(list(self.things_to_buy.values())[link][1]), True, WHITE), (10, 40))
                self.game.screen.blit(list(self.things_to_buy.values())[link][0], (0, 0))
                self.game.screen.blit(buy.image, buy.rect)
                if buy.is_pressed(mouse_pos, mouse_pressed) and self.game.number_bananok >= list(self.things_to_buy.values())[link][1]: 
                    self.game.number_bananok -= list(self.things_to_buy.values())[link][1]
                    # print(list(self.things_to_buy.keys())[link])
                    self.game.inv[list(self.things_to_buy.keys())[link]] = f"img/{list(self.things_to_buy.keys())[link]}.png"
                    self.things_to_buy.pop(list(self.things_to_buy.keys())[link])
                    link = len(self.things_to_buy) - 1
                    break
                elif buy.is_pressed(mouse_pos, mouse_pressed) and self.game.number_bananok < list(self.things_to_buy.values())[link][1]: self.game.screen.blit(self.game.big_font.render("You can't buy this thingy", True, RED), (280, 20)); pygame.time.delay(400)
                
                # Updates
                self.game.clock.tick(FPS)
                pygame.display.update()
                
        
        else: self.game.draw(); self.game.update(); self.game.talking("We're sold out", True, BLUE); return

        self.game.draw(); self.game.update()
        self.game.talking("Pleasure doing business with you", True, BLUE)