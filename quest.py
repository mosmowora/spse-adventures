import pygame
from config import *
from sprites import Button

class Quest:
    
    def __init__(self, game):
        """
        Make more complex quests here.
        """

        self.game = game
    
    def bench_press(self, bench_done):
        
        self.bench_done = bench_done

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
        if counter == 5: weak = False

        # Return
        return weak
    
    
    def function_to_bully_people(self):
        """
        This function needs your powers to fix it.
        It's part of a class.
        """

        add_even_to_list = [item for item in range(11) if item % 2 == 0]
        tuple_of_previous = tuple(add_even_to_list)
        return (item + 1 for item in tuple_of_previous)