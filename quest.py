import pygame
from config import *
from save_progress import SaveProgress
from sprites import Button

class Quest:
    
    def __init__(self, game):
        """
        Make more complex quests here.
        """
        self.game = game
    
    def bench_press(self):
        
        loaded_data = SaveProgress.load_data(self.game.player_name)
        if not loaded_data['quests']['dumbbell_lifted']: 
            self.game.talking('{} already did this quest.'.format(self.game.player_name))
            self.game.dumbbell_lifted = False
            return
        
        # Bench press quest for stronk bois
        background = pygame.image.load("img/bench_press.png").convert()
        dumbbell = pygame.image.load("img/bench_press_dumbbell.png").convert_alpha()
        dumbbell_rect = dumbbell.get_rect(x=8, y=50)
        back_button = Button(500, 400, 120, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)
        looking: bool = True
        counter: int = 0
        push_strength: int = 20
        
        while looking and counter < 5:
            
    
            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: self.game.exiting()

                # Clicking
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if dumbbell_rect.y >= -100: 
                        if counter == 2: dumbbell_rect.y -= push_strength - 3
                        elif counter == 3: dumbbell_rect.y -= push_strength - 5
                        elif counter == 4: dumbbell_rect.y -= push_strength - 7
                        else: dumbbell_rect.y -= push_strength
                        
                    else: dumbbell_rect.y = 50; counter += 1
           
            
            if dumbbell_rect.y <= 50: 
                if counter == 2: dumbbell_rect.y += 1.1
                elif counter == 3: dumbbell_rect.y += 1.2
                elif counter == 4: dumbbell_rect.y += 1.3
                else: dumbbell_rect.y += 1                    

            # Button
            print(dumbbell_rect.y)
            self.game.screen.blit(back_button.image, back_button.rect)
            self.game.screen.blit(background, (0, 0))
            self.game.screen.blit(self.game.font.render("Times lifted: {} of 5".format(counter), True, WHITE), (10, 10))
            self.game.screen.blit(dumbbell, dumbbell_rect)
            if back_button.is_pressed(mouse_pos, mouse_pressed): looking = False
            self.game.clock.tick(FPS)
            pygame.display.update()