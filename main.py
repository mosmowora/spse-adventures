# Import
import pygame
from sprites import *; from config import *

class Game:
    """
    Main class for game
    """

    def __init__(self):
        """
        Initialization
        """

        # Pygame initialization
        pygame.init()
        
        # Screen, time, font, running
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_running = True
        self.big_font = pygame.font.Font("Caveat.ttf", 40)
        self.font = pygame.font.Font("Roboto.ttf", 22)
        self.settings_font = pygame.font.Font("Caveat.ttf", 45)

        # Spritesheets
        self.character_spritesheet = Spritesheet("img/character.png")
        self.terrain_spritesheet = Spritesheet("img/terrain.png")
        self.npcs_spritesheet = Spritesheet("img/npc.png")

        # Into and Game Over backgrounds
        self.intro_background = pygame.image.load("img/intro_background.png")
        self.settings_background = pygame.image.load("img/settings_bg.jpg")
        
        # Window icon and title (not final)
        icon = pygame.image.load('img/spselogo.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('SPŠE ADVENTURE - REVENGEANCE')

        self.rooms: List[List[str]] = [ground_floor, first_floor, second_floor, third_floor, fourth_floor, basement] # Rooms where player can go
        self.in_room: List[str] = self.rooms[GROUND_FLOOR] # Room where player is rn (starting point) that's ground floor for those who don't know
        
        # Settings
        self.music_on: bool = True
        self.talking_speed_number: int = 90

        # Player name
        self.player_name: str = ""

        # Npc list
        self.npc = []
    
        self.reseting_game_values()

    def reseting_game_values(self):
        """
        When player wants to restart
        """

        # Objects you can interact with
        self.interacted: List[str, int] = ["", "", "", "", ""]
        self.interactive = {}

        # Inventory
        self.inv: List[str] = []

        # Variables for endings
        self.without_light: int = 0
        self.caught: int = 0

        # Variables for finding items/doing stuff
        self.key_in_trash: bool = True
        self.locked_locker: bool = True
        self.locked_changing_room: bool = True
        self.kokosky_in_locker: bool = True
        self.locker_stuff: dict[str, bool] = {"crocs": True, "boots": False, "key": True}

    def create_tile_map(self):
        """
        Creates tile map
        """

        self.interactive = {}

        for sprite in self.all_sprites: sprite.kill()

        for i, row in enumerate(self.in_room):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "_": Blockade(self, j, i, "_") # Grass
                elif column == "?": Blockade(self, j, i, "?") # Black
                elif column == "!": Block(self, j, i, "!") # No entry ground
                elif column == "P": self.player = Player(self, j, i) # Player
                elif column == "W": Block(self, j, i, "W") # Basic wall
                elif column == "w": Block(self, j, i, "w") # Window
                elif column == "L": self.interactive[Block(self, j, i, "L")] = "L" + str(i) + str(j) # Locker
                elif column == "Ľ": self.interactive[Block(self, j, i, "Ľ")] = "Ľ" + str(i) + str(j) # Locker
                elif column == "ľ": self.interactive[Block(self, j, i, "ľ")] = "ľ" + str(i) + str(j) # Locker
                elif column == "S": self.interactive[Block(self, j, i, "S")] = "S" + str(i) + str(j) # Stairs
                elif column == "Z": self.interactive[Block(self, j, i, "Z")] = "Z" + str(i) + str(j) # Stairs
                elif column == "s": self.interactive[Block(self, j, i, "s")] = "s" + str(i) + str(j) # Stairs down
                elif column == "z": self.interactive[Block(self, j, i, "z")] = "z" + str(i) + str(j) # Stairs down
                elif column == "D": self.interactive[Block(self, j, i, "D")] = "D" + str(i) + str(j) # Door
                elif column == "G": self.interactive[Block(self, j, i, "G")] = "G" + str(i) + str(j) # Glass door
                elif column == "B": self.interactive[Block(self, j, i, "B")] = "B" + str(i) + str(j) # Bench
                elif column == "l": self.interactive[Block(self, j, i, "l")] = "l" + str(i) + str(j) # Desk
                elif column == "U": self.interactive[Block(self, j, i, "U")] = "U" + str(i) + str(j) # LCUJ Desk
                elif column == "J": self.interactive[Block(self, j, i, "J")] = "J" + str(i) + str(j) # LCUJ Desk
                elif column == "j": self.interactive[Block(self, j, i, "j")] = "j" + str(i) + str(j) # Horizontal Desk
                elif column == "t": self.interactive[Block(self, j, i, "t")] = "t" + str(i) + str(j) # Trashcan
                elif column == "T": self.interactive[Block(self, j, i, "T")] = "T" + str(i) + str(j) # Toilet
                elif column == "Ť": self.interactive[Block(self, j, i, "Ť")] = "Ť" + str(i) + str(j) # Toilet
                elif column == "R": self.interactive[Block(self, j, i, "R")] = "R" + str(i) + str(j) # Rails
                elif column == "r": self.interactive[Block(self, j, i, "r")] = "r" + str(i) + str(j) # Rails
                elif column == "Ř": self.interactive[Block(self, j, i, "Ř")] = "Ř" + str(i) + str(j) # Rails ground_floor
                elif column == "Ŕ": self.interactive[Block(self, j, i, "Ŕ")] = "Ŕ" + str(i) + str(j) # Rails second_floor
                elif column == "ŕ": self.interactive[Block(self, j, i, "ŕ")] = "ŕ" + str(i) + str(j) # Rails second_floor
                elif column == "ř": self.interactive[Block(self, j, i, "ř")] = "ř" + str(i) + str(j) # Rails ground_floor
                elif column == "/": self.interactive[Block(self, j, i, "/")] = "/" + str(i) + str(j) # Rails fourth_floor
                elif column == "|": self.interactive[Block(self, j, i, "|")] = "|" + str(i) + str(j) # Rails fourth_floor
                elif column == "b": self.interactive[Block(self, j, i, "b")] = "b" + str(i) + str(j) # Basement
                elif column == "d": self.interactive[Block(self, j, i, "d")] = "d" + str(i) + str(j) # Basement
                elif column == "N": self.npc.append(Npc(self, j, i, "")) # NPC
                elif column == "C": self.npc.append(Npc(self, j, i, "C")) # Cleaner

    def new(self):
        """
        A new game starts
        """

        # Player is alive
        self.playing = True

        # Sprites, blocks, npcs
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.player_sprite = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.LayeredUpdates()
        self.interacts = pygame.sprite.LayeredUpdates()
        self.interactible = pygame.sprite.LayeredUpdates()
        self.cleaner = pygame.sprite.LayeredUpdates()

        # Tilemap
        self.create_tile_map()

        for sprite in self.all_sprites: sprite.rect.x -= 158 * TILE_SIZE

        return self
    
    def main(self):
        """
        Game loop
        """

        # Main game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

        return self
    
    def events(self):
        """
        Events for the game loop
        """

        # Events
        for event in pygame.event.get():

            # Close button
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: self.exiting()

            # Pressed E
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:

                # What was clicked
                match self.player.facing:
                    case "up": Interact(self, self.player.rect.x, self.player.rect.y - TILE_SIZE, self.interactive)
                    case "down": Interact(self, self.player.rect.x, self.player.rect.y + TILE_SIZE, self.interactive)
                    case "left": Interact(self, self.player.rect.x - TILE_SIZE, self.player.rect.y, self.interactive)
                    case "right": Interact(self, self.player.rect.x + TILE_SIZE, self.player.rect.y, self.interactive) 
                
                # What was clicked
                match self.interacted[0].capitalize():
                    case "Trashcan": self.trashcan()
                    case "Door": self.door()
                    case "Locker": self.locker()
                    case "Bench": self.bench()
                    case "Stairs_up": self.stairs()
                    case "Stairs_down": self.stairs()
                    case "Basement": self.basement()
                    case "Toilet": self.toilet()

                # Reset
                self.interacted = ["", "", ""]

    def update(self):
        """
        Updates for the game loop
        """

        # Updates every sprite
        self.all_sprites.update()
    
    def draw(self):
        """
        Draw for the game loop
        """

        self.screen.fill(NEARLY_BLACK) # Draws screen
        self.all_sprites.draw(self.screen) # Draws sprites onto the screen
        self.clock.tick(FPS) # How often does the game update
        pygame.display.update()

    def exiting(self):
        """
        After player presses Close button
        """

        # Buttons
        bg = pygame.image.load("img/exiting.png")
        return_button = Button(WIN_WIDTH // 2 - 155, WIN_HEIGHT // 2 - 45, 150, 40, fg=WHITE, bg=BLACK, content="Return", fontsize=32)
        settings_button = Button(WIN_WIDTH // 2 + 5, WIN_HEIGHT // 2 - 45, 150, 40, fg=WHITE, bg=BLACK, content="Settings", fontsize=32)
        sq_button = Button(WIN_WIDTH // 2 - 155, WIN_HEIGHT // 2 + 5, 310, 40, fg=WHITE, bg=BLACK, content="Save & Quit", fontsize=32)
        exit_pause: bool = False
        while True:

            # Close button
            for event in pygame.event.get():
                if event.type == pygame.QUIT: quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: exit_pause = not exit_pause; break

            if exit_pause: break
            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Settings button was pressed
            if settings_button.is_pressed(mouse_pos, mouse_pressed): self.settings()

            # Return button was pressed
            if return_button.is_pressed(mouse_pos, mouse_pressed): break

            # Save % Quit button was pressed
            if sq_button.is_pressed(mouse_pos, mouse_pressed): self.save_game()

            # BG
            self.screen.blit(bg, (0, 0))

            # Buttons
            self.screen.blit(return_button.image, return_button.rect)
            self.screen.blit(settings_button.image, settings_button.rect)
            self.screen.blit(sq_button.image, sq_button.rect)

            # Updates
            self.clock.tick(FPS)
            pygame.display.update()

    def save_game(self):
        """
        Saves game to file by player name
        """

        print("SAVED")
        quit()

    def game_over(self, img):
        """
        Game over screen
        """

        # Ending
        endings = ["img/lost.png", "img/you_never_learn.png"]

        # True ak ending je jeden z konecny (lost in school e.g.) hra zacina uplne odznova, ak False tak hrac ide na startovacie miesto (caught by cleaning lady e.g.)
        end = True if img in endings else False

        # BG
        self.game_over_background = pygame.image.load(img)

        # Creates text
        text = self.big_font.render("Game Over", True, BLACK)
        text_rect = text.get_rect(center = (75, 50))

        # Creates button
        restart_button = Button(10, WIN_HEIGHT - 60, 200, 50, WHITE, DARK_GRAY, "Main menu", 32) if end else Button(10, WIN_HEIGHT - 60, 200, 50, WHITE, DARK_GRAY, "Try again", 32)
        iamdone_button = Button(10, WIN_HEIGHT - 120, 200, 50, WHITE, DARK_GRAY, "I'm done", 32)

        # Removing every sprite
        for sprite in self.all_sprites: sprite.kill()

        # Loop
        while self.game_running:

            # Close button
            for event in pygame.event.get():
                if event.type == pygame.QUIT: quit()

            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed): 
                if end: 
                    self.reseting_game_values()
                    self.intro_screen().new()
                    self.main()
                else: 
                    self.new()
                    self.main()

            elif iamdone_button.is_pressed(mouse_pos, mouse_pressed): quit()
            
            # Displaying background, text, button
            self.screen.blit(self.game_over_background, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.screen.blit(iamdone_button.image, iamdone_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        """
        Intro screen
        """

        intro = True

        # Title
        title = self.big_font.render("SPSE ADVENTURE", True, BLACK)
        title_rect = title.get_rect(x=10, y=10)

        # Made by
        made = self.font.render("Made by: MTS", True, WHITE)
        made_rect = made.get_rect(x=490, y=450)

        # Start button
        play_button = Button(10, 60, 180, 50, fg=WHITE, bg=BLACK, content="Play", fontsize=32)

        # Settings button
        settings_button = Button(10, 120, 180, 50, fg=WHITE, bg=BLACK, content="Settings", fontsize=32)

        # Leaderboard button
        leaderboard_button = Button(10, 180, 180, 50, fg=WHITE, bg=BLACK, content="Leaderboard", fontsize=32)

        # Main loop for intro
        while intro:

            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: quit()

            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Play button was pressed
            if play_button.is_pressed(mouse_pos, mouse_pressed): intro = self.start(intro)
            if not intro: break

            # Settings button was pressed
            if settings_button.is_pressed(mouse_pos, mouse_pressed): self.settings()
            
            # Leadboard button was pressed
            if leaderboard_button.is_pressed(mouse_pos, mouse_pressed): self.leaderboard()

            # Diplaying background, title, buttons
            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(made, made_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(settings_button.image, settings_button.rect)
            self.screen.blit(leaderboard_button.image, leaderboard_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

        return self
    
    def start(self, intro):
        """
        Starting the game
        """

        picking_name = True
        active = False

        # Button
        back = Button(10, WIN_HEIGHT - 60, 200, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)

        # Title
        title = self.big_font.render("SPSE ADVENTURE", True, BLACK)
        title_rect = title.get_rect(x=10, y=10)

        # Made by
        made = self.font.render("Made by: MTS", True, WHITE)
        made_rect = made.get_rect(x=490, y=450)

        # Your name
        your_name = self.font.render("Your name:", True, WHITE)
        your_name_rect = made.get_rect(x=10, y=62)
        
        # Input rectangle
        input_rect = pygame.Rect(130, 60, 200, 32)

        while picking_name:

            for event in pygame.event.get():
      
                # Quit
                if event.type == pygame.QUIT: quit()
        
                # Click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos): active = True
                    else: active = False

                # Keyboard
                if event.type == pygame.KEYDOWN:
      
                    # Check for backspace
                    if event.key == pygame.K_BACKSPACE: self.player_name = self.player_name[:-1]
                    
                    # Enter
                    elif event.key == pygame.K_RETURN: 
                        if len(self.player_name) > 0: picking_name = intro = False; break

                    # Unicode
                    elif active: self.player_name += event.unicode

            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            if back.is_pressed(mouse_pos, mouse_pressed): picking_name = False

            # Background
            self.screen.blit(self.intro_background, (0, 0))

            # Your name
            self.screen.blit(your_name, your_name_rect)

            if active: color = GRAY
            else: color = BLACK

            # Input rectangle
            pygame.draw.rect(self.screen, color, input_rect)
    
            # Input Text
            text_surface = self.font.render(self.player_name, True, (255, 255, 255))
            self.screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))

            # Width of rectangle
            input_rect.w = max(200, text_surface.get_width()+10)

            # Button
            self.screen.blit(back.image, back.rect)

            # Text
            self.screen.blit(made, made_rect)
            self.screen.blit(title, title_rect)
            self.clock.tick(FPS)
            pygame.display.flip()

        return intro
    
    def settings(self):
        """
        Opens settings window
        """
        
        opened = True

        # Slider
        slider_back = Button(250, 155, 100, 20, fg=BLACK, bg=DIM_GRAY, content="", fontsize=0)
        slider = Button(300, 140, 50, 50, fg=BLACK, bg=GREEN, content="", fontsize=0) if self.music_on else Button(250, 140, 50, 50, fg=BLACK, bg=RED, content="", fontsize=0)
        slider_inside = Button(312.5, 152.5, 25, 25, fg=BLACK, bg=BLACK, content="", fontsize=0) if self.music_on else Button(262.5, 152.5, 25, 25, fg=BLACK, bg=BLACK, content="", fontsize=0)

        # Talking speed
        slow = Button(225, 260, 130, 50, fg=BLACK, bg=DIM_GRAY, content="SLOW", fontsize=32) if self.talking_speed_number == 105 else Button(225, 260, 130, 50, fg=BLACK, bg=WHITE, content="SLOW", fontsize=32)
        medium = Button(365, 260, 130, 50, fg=BLACK, bg=DIM_GRAY, content="MEDIUM", fontsize=32) if self.talking_speed_number == 90 else Button(365, 260, 130, 50, fg=BLACK, bg=WHITE, content="MEDIUM", fontsize=32)
        fast = Button(505, 260, 130, 50, fg=BLACK, bg=DIM_GRAY, content="FAST", fontsize=32) if self.talking_speed_number == 75 else Button(505, 260, 130, 50, fg=BLACK, bg=WHITE, content="FAST", fontsize=32)

        # Button
        back = Button(10, WIN_HEIGHT - 60, 200, 50, fg=WHITE, bg=GRAY, content="Back", fontsize=32)

        # Sound
        sound_effects = self.font.render("Sound", True, WHITE)
        sound_effects_rect = sound_effects.get_rect(x=265, y=100)

        # Sound
        talking_speed = self.font.render("Talking speed", True, WHITE)
        talking_speed_rect = sound_effects.get_rect(x=365, y=220)

        # Title
        title = self.settings_font.render("Settings", True, WHITE)
        title_rect = title.get_rect(x=10, y=10)
        
        while opened:
            
            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: quit()
                
            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            if back.is_pressed(mouse_pos, mouse_pressed): opened = False
            
            # From on (right) to off (left)
            elif slider.is_pressed(mouse_pos, mouse_pressed) and self.music_on or slider_inside.is_pressed(mouse_pos, mouse_pressed) and self.music_on:
                for _ in range(12):
                    slider.rect.x -= 4
                    slider_inside.rect.x -= 4
                    self._settings_animation(title, title_rect, sound_effects, sound_effects_rect, talking_speed, talking_speed_rect, slider_back, slider, slider_inside, back, slow, medium, fast)
                self.music_on = not self.music_on
                slider_inside.rect.x -= 2
                slider = Button(250, 140, 50, 50, fg=BLACK, bg=RED, content="", fontsize=0)
                
            # From off (left) to on (right)
            elif slider.is_pressed(mouse_pos, mouse_pressed) and not self.music_on or slider_inside.is_pressed(mouse_pos, mouse_pressed) and not self.music_on:
                for _ in range(12):
                    slider.rect.x += 4
                    slider_inside.rect.x += 4
                    self._settings_animation(title, title_rect, sound_effects, sound_effects_rect, talking_speed, talking_speed_rect, slider_back, slider, slider_inside, back, slow, medium, fast)
                self.music_on = not self.music_on
                slider_inside.rect.x += 2
                slider = Button(300, 140, 50, 50, fg=BLACK, bg=GREEN, content="", fontsize=0)

            # Talking speed - Slow
            elif slow.is_pressed(mouse_pos, mouse_pressed):
                self.talking_speed_number = 105
                slow = Button(225, 260, 130, 50, fg=BLACK, bg=DIM_GRAY, content="SLOW", fontsize=32)
                medium = Button(365, 260, 130, 50, fg=BLACK, bg=WHITE, content="MEDIUM", fontsize=32)
                fast = Button(505, 260, 130, 50, fg=BLACK, bg=WHITE, content="FAST", fontsize=32)

            # Talking speed - Medium
            elif medium.is_pressed(mouse_pos, mouse_pressed):
                self.talking_speed_number = 90
                slow = Button(225, 260, 130, 50, fg=BLACK, bg=WHITE, content="SLOW", fontsize=32)
                medium = Button(365, 260, 130, 50, fg=BLACK, bg=DIM_GRAY, content="MEDIUM", fontsize=32)
                fast = Button(505, 260, 130, 50, fg=BLACK, bg=WHITE, content="FAST", fontsize=32)

            # Talking speed - Fast
            elif fast.is_pressed(mouse_pos, mouse_pressed):
                self.talking_speed_number = 75
                slow = Button(225, 260, 130, 50, fg=BLACK, bg=WHITE, content="SLOW", fontsize=32)
                medium = Button(365, 260, 130, 50, fg=BLACK, bg=WHITE, content="MEDIUM", fontsize=32)
                fast = Button(505, 260, 130, 50, fg=BLACK, bg=DIM_GRAY, content="FAST", fontsize=32)
                    
            # Diplaying background, title, buttons
            self._settings_animation(title, title_rect, sound_effects, sound_effects_rect, talking_speed, talking_speed_rect, slider_back, slider, slider_inside, back, slow, medium, fast)

    def _settings_animation(self, title, title_rect, sound_effects, sound_effects_rect, talking_speed, talking_speed_rect, slider_back, slider, slider_inside, back, slow, medium, fast):
        """
        Animation for settings sliders
        """

        self.screen.blit(self.settings_background, (0, 0))
        self.screen.blit(title, title_rect)
        self.screen.blit(sound_effects, sound_effects_rect)
        self.screen.blit(talking_speed, talking_speed_rect)
        self.screen.blit(slider_back.image, slider_back.rect)
        self.screen.blit(slider.image, slider.rect)
        self.screen.blit(slider_inside.image, slider_inside.rect)
        self.screen.blit(slow.image, slow.rect)
        self.screen.blit(medium.image, medium.rect)
        self.screen.blit(fast.image, fast.rect)
        self.screen.blit(back.image, back.rect)
        self.clock.tick(FPS)
        pygame.display.update()

    def leaderboard(self):
        """
        Opens leaderboard window
        """
        print("If we had one")

    def door_info(self, msg_content: str):
        """
        Displays info about the room the character is entering/exiting
        """

        for _ in range(45):
            text = self.font.render(msg_content, True, WHITE)
            text_rect = text.get_rect(x=10, y=10)
            self.screen.blit(text, text_rect)
            self.clock.tick(FPS)
            pygame.display.update()
        self.update()
        self.draw()
              
    def talking(self, msg_content: str):
        """
        When character is talking
        """

        for _ in range(self.talking_speed_number):
            text = self.font.render(msg_content, True, WHITE)
            text_rect = text.get_rect(x=10, y=10)
            self.screen.blit(text, text_rect)
            self.clock.tick(FPS)
            pygame.display.update()
        self.update()
        self.draw()

    def trashcan(self):
        """
        Poking around in trashcan
        """

        # In changing room
        if self.interacted[1] == 13 and self.interacted[2] == 165:
            self.talking("There's paper on the side of the trashcan.")
            self.talking("It says 2.SA. You agree with this statement.")

            # Key in trash
            if self.key_in_trash: 
                self.inv.append("locker key")
                self.key_in_trash = False
                self.talking(f"{self.player_name} found a key in the trashcan. It says AR.")

            # Empty trashcan
            else: self.talking("There is nothing interesting.")
            
    def center_player_after_doors(self):
        """
        Makes player stand right behind the door they walk through
        """

        # Facing up
        if self.player.facing == "up":
            self.player.rect.x = self.interacted[3]
            self.player.rect.y = self.interacted[4] - TILE_SIZE
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
        
        # Facing down
        elif self.player.facing == "down":
            self.player.rect.x = self.interacted[3]
            self.player.rect.y = self.interacted[4] + TILE_SIZE
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE

        # Facing left
        elif self.player.facing == "left":
            self.player.rect.x = self.interacted[3] - TILE_SIZE
            self.player.rect.y = self.interacted[4]
            for sprite in self.all_sprites: sprite.rect.x += 2 * TILE_SIZE
            
        # Facing right
        elif self.player.facing == "right":
            self.player.rect.x = self.interacted[3] + TILE_SIZE
            self.player.rect.y = self.interacted[4]
            for sprite in self.all_sprites: sprite.rect.x -= 2 * TILE_SIZE

    def ground_floor_doors(self):
        """
        Doors on the ground floor
        """

        # Changing room -> Hall
        if self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 167:

            # Door is locked
            if self.locked_changing_room:

                # Key in inventory
                if "changing_room key" in self.inv:
                    self.talking(f"{self.player_name} unlocked the door.")
                    self.locked_changing_room = False

                # No key
                else: self.talking(f"{self.player_name} can't find key to unlock the door.")
            
            elif not self.locked_changing_room: self.center_player_after_doors()
                    
        # Hall -> Changing room
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 167: self.door_info("Don't forget to change yo shoes"); self.center_player_after_doors()

        # Hall -> Buffet Amper
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 176:
            self.talking("Buffet Amper. I like to buy food here.")
            self.talking("Sadly it's closed now.")

        # Hall -> 020
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 166:self.door_info("020 - not a classroom")

        # Hall -> 021
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 159: self.door_info("021 - not a classroom")

        # Hall -> 022
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 152: self.door_info("022 - not a classroom")

        # Hall -> 023
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 133: self.door_info("023 - LIT 3"); self.center_player_after_doors()

        # 023 -> Hall
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 133: self.door_info("Hall"); self.center_player_after_doors()
            
        # Hall -> ???
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 123: self.door_info("??? - not a classroom")

                # Hall -> 025
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 96: self.door_info("025 - LCUJ 4"); self.center_player_after_doors()

        # 025 -> Hall 
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 96: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> 026
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 88: self.door_info("026 - not a classroom")

        # 026 -> Hall
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 88: self.door_info("026 - not a classroom")

        # Hall -> 027
        elif self.player.facing == "right" and self.interacted[1] == 25 and self.interacted[2] == 76: self.door_info("027 - not a classroom")

        # Hall -> 010
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 33: self.door_info("010 - Toilets"); self.center_player_after_doors()

        # 010 -> Hall
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 33: self.door_info("Hall"); self.center_player_after_doors()

        # Toilet room -> Stall
        elif self.player.facing == "up" and self.interacted[1] == 24 and self.interacted[2] in (37, 39): self.door_info("PeePeePooPoo time"); self.center_player_after_doors()

        # Stall -> Toilet room
        elif self.player.facing == "down" and self.interacted[1] == 24 and self.interacted[2] in (37, 39): self.door_info("Don't forget to wash yo hands"); self.center_player_after_doors()

        # Hall -> 009
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 25: self.door_info("009 - not a classroom")

        # Hall -> 008
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 19: self.door_info("008 - DPXA 3"); self.center_player_after_doors()

        # 008 -> Hall
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 19: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> 007
        elif self.player.facing == "left" and self.interacted[1] == 17 and self.interacted[2] == 11: self.door_info("007 - LIT 10"); self.center_player_after_doors()

        # 007 -> Hall
        elif self.player.facing == "right" and self.interacted[1] == 17 and self.interacted[2] == 11: self.door_info("Hall"); self.center_player_after_doors()

        # 007 -> 006
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 9: self.door_info("006 - LIT 9"); self.center_player_after_doors()

        # 006 -> 007
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 9: self.door_info("007 - LIT 10"); self.center_player_after_doors()

        # Hall -> 004
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 20: self.door_info("004 - LIT 8"); self.center_player_after_doors()

        # 004 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 20: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> 003
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 24: self.door_info("003 - DPXA 2"); self.center_player_after_doors()

        # 003 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 24: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> 002
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 35: self.door_info("002 - DPXA 1"); self.center_player_after_doors()

        # 002 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 35: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> 012
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 79: self.door_info("012 - II.A"); self.center_player_after_doors()

        # 012 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 79: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> 013
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 88: self.door_info("013 - II.B"); self.center_player_after_doors()

        # 013 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 88: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> 014
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 114: self.door_info("014 - LAELE"); self.center_player_after_doors()
        
        # 014 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 114: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> 015
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 135: self.door_info("015 - II.C"); self.center_player_after_doors()

        # 015 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 135: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> 016
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 159: self.door_info("016 - II.SA"); self.center_player_after_doors()
                
        # 016 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 159: self.door_info("Hall"); self.center_player_after_doors()
            
    def first_floor_doors(self):
        """
        Doors on the first floor
        """

        # Hall -> 122/1
        if self.player.facing == "right" and self.interacted[2] == 173 and self.interacted[1] in (12, 13): self.door_info("122/1 -  LIT 1 (III.SA)"); self.center_player_after_doors()
        
        # 122/1 -> Hall
        elif self.player.facing == "left" and self.interacted[2] == 173 and self.interacted[1] in (12, 13): self.door_info("Hall"); self.center_player_after_doors()
        
        # 122/1 -> 122/2
        elif self.player.facing == "up" and self.interacted[2] == 177 and self.interacted[1] == 8: self.door_info("122/2 -  LIT 2 (IV.SA)"); self.center_player_after_doors()
        
        # 122/2 -> 122/1
        elif self.player.facing == "down" and self.interacted[2] == 177 and self.interacted[1] == 8: self.door_info("122/1 -  LIT 1 (III.SA)"); self.center_player_after_doors()
            
        # Hall -> Kabinet pri 122/1
        elif self.player.facing == "right" and self.interacted[2] == 173 and self.interacted[1] == 18: self.door_info("Cabinet"); self.center_player_after_doors()
            
        # Kabinet pri 122/1 -> Hall
        elif self.player.facing == "left" and self.interacted[2] == 173 and self.interacted[1] == 18: self.door_info("Hall"); self.center_player_after_doors()
            
        # 122/2 -> Kabinet HED, MIT
        elif self.player.facing == "left" and self.interacted[2] == 173 and self.interacted[1] == 6: self.door_info("Cabinet"); self.center_player_after_doors()
            
        # Kabinet HED, MIT -> 122/2 
        elif self.player.facing == "right" and self.interacted[2] == 173 and self.interacted[1] == 6: self.door_info("122/2 -  LIT 2 (IV.SA)"); self.center_player_after_doors()
            
        # Hall -> Kabinet HED, MIT
        elif self.player.facing == "up" and self.interacted[2] == 169 and self.interacted[1] == 7: self.door_info("Cabinet"); self.center_player_after_doors()
            
        # Kabinet HED, MIT -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 169 and self.interacted[1] == 7: self.door_info("Hall"); self.center_player_after_doors()
            
        # Hall -> Toilets
        elif self.player.facing == "left" and self.interacted[2] == 166 and self.interacted[1] == 12: self.door_info("Toilets"); self.center_player_after_doors()
        
        # Toilets -> Stall
        elif self.player.facing == "down" and self.interacted[2] == 161 and self.interacted[1] == 13: self.door_info("PeePeePooPoo Time"); self.center_player_after_doors()

        # Stall -> Toilets
        elif self.player.facing == "up" and self.interacted[2] == 161 and self.interacted[1] == 13: self.door_info("Don't forget to wash your hands"); self.center_player_after_doors()

        # Toilets -> Hall
        elif self.player.facing == "right" and self.interacted[2] == 166 and self.interacted[1] == 12: self.door_info("Hall"); self.center_player_after_doors()
        
        # Hall -> 117
        elif self.player.facing == "up" and self.interacted[2] == 155 and self.interacted[1] == 24: self.door_info("117 - III.B"); self.center_player_after_doors()
        
        # 117 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 155 and self.interacted[1] == 24: self.door_info("Hall"); self.center_player_after_doors()
        
        # Hall -> 115
        elif self.player.facing == "up" and self.interacted[2] == 128 and self.interacted[1] == 24: self.door_info("115 - IV.SB"); self.center_player_after_doors()
        
        # 115 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 128 and self.interacted[1] == 24: self.door_info("Hall"); self.center_player_after_doors()
        
        # Hall -> 113
        elif self.player.facing == "up" and self.interacted[2] == 93 and self.interacted[1] == 24: self.door_info("113 - III.C"); self.center_player_after_doors()
        
        # 113 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 93 and self.interacted[1] == 24: self.door_info("Hall"); self.center_player_after_doors()
        
        # 113 -> Cabinet LIA
        elif self.player.facing == "right" and self.interacted[2] == 97 and self.interacted[1] == 21: self.door_info("Cabinet LIA"); self.center_player_after_doors()
        
        # Cabinet LIA -> 113
        elif self.player.facing == "left" and self.interacted[2] == 97 and self.interacted[1] == 21: self.door_info("113 - III.C"); self.center_player_after_doors()
        
        # Hall -> 112
        elif self.player.facing == "up" and self.interacted[2] == 76 and self.interacted[1] == 24: self.door_info("112 - LELM 1"); self.center_player_after_doors()
        
        # 112 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 76 and self.interacted[1] == 24: self.door_info("Hall"); self.center_player_after_doors()
        
        # Hall -> 124
        elif self.player.facing == "down" and self.interacted[2] == 160 and self.interacted[1] == 30: self.door_info("124 - LELM 2"); self.center_player_after_doors()
        
        # 124 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 160 and self.interacted[1] == 30: self.door_info("Hall"); self.center_player_after_doors()
        
        # Hall -> 126
        elif self.player.facing == "down" and self.interacted[2] == 141 and self.interacted[1] == 30: self.door_info("126 - LSIE 2"); self.center_player_after_doors()
        
        # 126 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 141 and self.interacted[1] == 30: self.door_info("Hall"); self.center_player_after_doors() 
        
        # Hall -> 127
        elif self.player.facing == "down" and self.interacted[2] == 126 and self.interacted[1] == 30: self.door_info("127 - LIOT"); self.center_player_after_doors()
        
        # 127 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 126 and self.interacted[1] == 30: self.door_info("Hall"); self.center_player_after_doors()  
        
        # Hall -> 130
        elif self.player.facing == "down" and self.interacted[2] == 104 and self.interacted[1] == 30: self.door_info("130 - CZV"); self.center_player_after_doors()
        
        # 130 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 104 and self.interacted[1] == 30: self.door_info("Hall"); self.center_player_after_doors()
             
    def second_floor_doors(self): 
        """
        Doors on the second floor
        """

        # Hall -> 203
        if self.player.facing == "left" and self.interacted[2] == 11 and self.interacted[1] == 28: self.door_info("203 - III.A"); self.center_player_after_doors()

        # 203 -> Hall 
        elif self.player.facing == "right" and self.interacted[2] == 11 and self.interacted[1] == 28: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> 202
        elif self.player.facing == "up" and self.interacted[2] == 23 and self.interacted[1] == 25: self.door_info("202 - I.SC"); self.center_player_after_doors()

        # 202 -> Hall 
        elif self.player.facing == "down" and self.interacted[2] == 23 and self.interacted[1] == 25: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> 205
        elif self.player.facing == "down" and self.interacted[2] == 16 and self.interacted[1] == 31: self.door_info("205 - III.A"); self.center_player_after_doors()

        # 205 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 16 and self.interacted[1] == 31: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> 201
        elif self.player.facing == "up" and self.interacted[2] == 42 and self.interacted[1] == 25: self.door_info("201 - Goated place"); self.center_player_after_doors()

        # 201 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 42 and self.interacted[1] == 25: self.door_info("Hall"); self.center_player_after_doors()
    
        # Hall -> Toilets
        elif self.player.facing == "down" and self.interacted[2] == 40 and self.interacted[1] == 31: self.door_info("Toilets"); self.center_player_after_doors()

        # Toilets -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 40 and self.interacted[1] == 31: self.door_info("Hall"); self.center_player_after_doors()
        
        # Toilets -> Stall
        elif self.player.facing == "up" and self.interacted[2] in (42, 44) and self.interacted[1] == 34: self.door_info("Stall"); self.center_player_after_doors()

        # Stall -> Toilets
        elif self.player.facing == "down" and self.interacted[2] in (42, 44) and self.interacted[1] == 34: self.door_info("Don't forget to wash yo hands"); self.center_player_after_doors()
            
        # Hall -> 208
        elif self.player.facing == "up" and self.interacted[2] == 76 and self.interacted[1] == 25: self.door_info("208 - I.A"); self.center_player_after_doors()
            
        # 208 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 76 and self.interacted[1] == 25: self.door_info("Hall"); self.center_player_after_doors()
            
        # Hall -> 209
        elif self.player.facing == "up" and self.interacted[2] == 93 and self.interacted[1] == 25: self.door_info("209 - I.B"); self.center_player_after_doors()

        # 209 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 93 and self.interacted[1] == 25: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> 299
        elif self.player.facing == "up" and self.interacted[2] == 109 and self.interacted[1] == 25: self.door_info("299 - LRIS"); self.center_player_after_doors()

        # 299 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 109 and self.interacted[1] == 25: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> 210
        elif self.player.facing == "up" and self.interacted[2] == 128 and self.interacted[1] == 25: self.door_info("210 - III.SB"); self.center_player_after_doors()
            
        # 210 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 128 and self.interacted[1] == 25: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> 211
        elif self.player.facing == "up" and self.interacted[2] == 138 and self.interacted[1] == 25: self.door_info("211 - Coming soon")

        # 211 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 138 and self.interacted[1] == 25: self.door_info("Hall")

        # Hall -> 212
        elif self.player.facing == "up" and self.interacted[2] == 157 and self.interacted[1] == 25: self.door_info("212 - IV.A"); self.center_player_after_doors()

        # 212 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 157 and self.interacted[1] == 25: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> Toilets
        elif self.player.facing == "left" and self.interacted[2] == 166 and self.interacted[1] == 16: self.door_info("Toilets"); self.center_player_after_doors()

        # Toilets -> Hall
        elif self.player.facing == "right" and self.interacted[2] == 166 and self.interacted[1] == 16: self.door_info("Hall"); self.center_player_after_doors()
        
        # Toilets -> Stall
        elif self.player.facing == "down" and self.interacted[2] == 161 and self.interacted[1] == 16: self.door_info("Stall"); self.center_player_after_doors()

        # Stall -> Toilets
        elif self.player.facing == "up" and self.interacted[2] == 161 and self.interacted[1] == 16: self.door_info("Don't forget to wash yo hands"); self.center_player_after_doors()

        # Hall -> 216
        elif self.player.facing == "up" and self.interacted[2] == 169 and self.interacted[1] == 14: self.door_info("216 - OUF (IV.C)"); self.center_player_after_doors()
            
        # 216 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 169 and self.interacted[1] == 14: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> 217
        elif self.player.facing == "right" and self.interacted[2] == 173 and self.interacted[1] == 19: self.door_info("217 - Cabinet"); self.center_player_after_doors()

        # 217 -> Hall
        elif self.player.facing == "left" and self.interacted[2] == 173 and self.interacted[1] == 19: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> 218
        elif self.player.facing == "down" and self.interacted[2] == 141 and self.interacted[1] == 31: self.door_info("218 - I.SB"); self.center_player_after_doors()

        # 218 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 141 and self.interacted[1] == 31: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> 219
        elif self.player.facing == "down" and self.interacted[2] == 117 and self.interacted[1] == 31: self.door_info("219 = I.SA"); self.center_player_after_doors()

        # 219 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 117 and self.interacted[1] == 31: self.door_info("Hall"); self.center_player_after_doors()

        # Hall -> 220
        elif self.player.facing == "down" and self.interacted[2] == 139 and self.interacted[1] == 31: self.door_info("220 - I.C")

        # 220 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 139 and self.interacted[1] == 31: self.door_info("Hall")
        
    def third_floor_doors(self):
        """
        Doors on the third floor
        """

        # Hall -> Gym changing rooms
        if self.player.facing in ("up", "left") and self.interacted[2] == 63 and self.interacted[1] == 8: self.door_info("Gym - Changing rooms"); self.center_player_after_doors()
        
        # Gym changing rooms -> Hall
        elif self.player.facing in ("down", "right") and self.interacted[2] == 63 and self.interacted[1] == 8: self.door_info("Hall"); self.center_player_after_doors()

        # Gym changing rooms -> Toielet
        elif self.player.facing == "left" and self.interacted[2] == 57 and self.interacted[1] == 7: self.door_info("Toilets"); self.center_player_after_doors()

        # Toilet -> Gym changing rooms
        elif self.player.facing == "right" and self.interacted[2] == 57 and self.interacted[1] == 7: self.door_info("Gym - Changing rooms"); self.center_player_after_doors()
        
        # Gym changing rooms -> Gym
        elif self.player.facing == "left" and self.interacted[2] == 54 and self.interacted[1] == 5: self.door_info("302 - Gym"); self.center_player_after_doors()

        # Gym -> Gym changing rooms
        elif self.player.facing == "right" and self.interacted[2] == 54 and self.interacted[1] == 5: self.door_info("Gym - Changing rooms"); self.center_player_after_doors()

        # Gym -> Gymnasium
        elif self.player.facing == "down" and self.interacted[2] in (16, 17) and self.interacted[1] == 6: self.door_info("304 - Gymnasium"); self.center_player_after_doors()

        # Gymnasium -> Gym
        elif self.player.facing == "up" and self.interacted[2] in (16, 17) and self.interacted[1] == 6: self.door_info("302 - Gym"); self.center_player_after_doors()
        
        # Hall -> 304
        elif self.player.facing == "left" and self.interacted[2] == 54 and self.interacted[1] in (11, 12): self.door_info("304 - Gymnasium"); self.center_player_after_doors()
        
        # 304 -> Hall
        elif self.player.facing == "right" and self.interacted[2] == 54 and self.interacted[1] in (11, 12): self.door_info("Hall"); self.center_player_after_doors()
        
        # Hall -> Gymnasium changing room
        elif self.player.facing == "down" and self.interacted[2] == 67 and self.interacted[1] == 18: self.door_info("Gymnasium - Changing rooms"); self.center_player_after_doors()
        
        # Gymnasium changing room -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 67 and self.interacted[1] == 18: self.door_info("Hall"); self.center_player_after_doors()
        
        # Gymnasium changing room -> Gymnasium
        elif self.player.facing == "left" and self.interacted[2] == 54 and self.interacted[1] == 25: self.door_info("304 - Gymnasium"); self.center_player_after_doors()
        
        # Gymnasium -> Gymnasium changing room
        elif self.player.facing == "right" and self.interacted[2] == 54 and self.interacted[1] == 25: self.door_info("Gymnasium - Changing rooms"); self.center_player_after_doors()

        # Gymnasium changing room -> Showers
        elif self.player.facing == "left" and self.interacted[2] == 72 and self.interacted[1] == 25: self.door_info("Showers"); self.center_player_after_doors()

        # Showers -> Gymnasium changing room
        elif self.player.facing == "right" and self.interacted[2] == 72 and self.interacted[1] == 25: self.door_info("Gymnasium - Changing room"); self.center_player_after_doors()

        # Hall -> Cabinet
        elif self.player.facing == "right" and self.interacted[2] == 70 and self.interacted[1] == 6: self.door_info("Cabinet"); self.center_player_after_doors()
        
        # Cabinet -> Hall
        elif self.player.facing == "left" and self.interacted[2] == 70 and self.interacted[1] == 6: self.door_info("Hall"); self.center_player_after_doors()
        
    def fourth_floor_doors(self):
        """
        Doors on the fourth floor
        """
        
        # Hall -> LSIE
        if self.player.facing == "down" and self.interacted[2] == 62 and self.interacted[1] == 17: self.door_info("403 - LSIE"); self.center_player_after_doors()
        
        # LSIE -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 62 and self.interacted[1] == 17: self.door_info("Hall"); self.center_player_after_doors()
        
        # Hall -> LROB (predsien)
        elif self.player.facing in ("up", "left") and self.interacted[2] == 63 and self.interacted[1] == 8: self.door_info("402 - LROB hallway"); self.center_player_after_doors()

        # LROB (predsien) -> Hall
        elif self.player.facing in ("down", "right") and self.interacted[2] == 63 and self.interacted[1] == 8: self.door_info("Hall"); self.center_player_after_doors()

        # LROB (predsien) -> LROB
        elif self.player.facing == "left" and self.interacted[2] == 54 and self.interacted[1] == 5: self.door_info("402 - LROB"); self.center_player_after_doors()

        # LROB -> LROB (predsien)
        elif self.player.facing == "right" and self.interacted[2] == 54 and self.interacted[1] == 5: self.door_info("402 - LROB hallway"); self.center_player_after_doors()

    def shoes_on(self):
        """
        Checks if player has shoes on
        """

        if self.locker_stuff["crocs"] and self.caught <= 3: 
            self.caught += 2
            self.game_over("img/caught.png")
        elif self.locker_stuff["crocs"] and self.caught > 3: self.game_over("img/you_never_learn.png")
               
    def locker(self):
        """
        Unlocking the locker
        """

        # Locker with key
        if self.interacted[1] == 9 and self.interacted[2] == 171:

            # Locked
            if self.locked_locker:

                # Has key
                if "locker key" in self.inv:
                    self.talking(f"{self.player_name} unlocked the locker.")
                    self.locked_locker = False

                # No key
                else: self.talking("Locked locker.")

            # Unlocked
            else: self.in_locker()

        # Locker with kokosky
        elif self.interacted[1] == 4 and self.interacted[2] == 165:

            # Locker full
            if self.kokosky_in_locker:
                self.talking("Hmm? Why is it unlocked?")
                self.talking("Wow, what is this?")
                self.talking(f"{self.player_name} found the forbidden Kokosky fragment. [1/4]")
                self.kokosky_in_locker = False
                self.inv.append("Kokosky1")

            # Locker empty
            else: self.talking("It's empty, but smells.")

        # Other
        else: 
            
            # Key in inventory
            if "locker key" in self.inv and self.locked_locker: self.talking("Wrong locker.")
            
            # No key
            else: self.talking("Locked locker.")

    def in_locker(self):
        """
        Player is looking in locker
        """

        looking = True

        # Images
        locker = pygame.image.load("img/in_locker.png")
        crocs = pygame.image.load("img/crocs.png")
        crocs_rect = crocs.get_rect(x=195, y=232)
        boots = pygame.image.load("img/boots.png")
        boots_rect = boots.get_rect(x=196, y=229)
        key = pygame.image.load("img/changing_room key.png")
        key_rect = key.get_rect(x=185, y=155)

        # Button
        back_button = Button(500, 400, 120, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)
        
        while looking:
    
            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            # Background
            self.screen.blit(locker, (0, 0))

            # Crocs/Boots
            if self.locker_stuff["crocs"]: self.screen.blit(crocs, crocs_rect)
            else: self.screen.blit(boots, boots_rect)

            # Key
            if self.locker_stuff["key"]: self.screen.blit(key, key_rect)
            
            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: quit()

                # Clicking
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Key
                    if key_rect.collidepoint(event.pos): 
                        self.locker_stuff['key'] = False
                        self.inv.append("changing_room key")
                    
                    # Boots
                    elif boots_rect.collidepoint(event.pos) and self.locker_stuff["boots"]: 
                        self.locker_stuff['boots'] = not self.locker_stuff['boots']
                        self.locker_stuff['crocs'] = not self.locker_stuff['crocs']
                    
                    # Crocs
                    elif crocs_rect.collidepoint(event.pos) and self.locker_stuff['crocs']:
                        self.locker_stuff['crocs'] = not self.locker_stuff['crocs']
                        self.locker_stuff['boots'] = not self.locker_stuff['boots']

            # Button
            self.screen.blit(back_button.image, back_button.rect)
            if back_button.is_pressed(mouse_pos, mouse_pressed): looking = False
            self.clock.tick(FPS)
            pygame.display.update()
            
    def bench(self):
        """
        Sitting on the bench
        """

        self.player.sit(True, self.interacted[1], self.interacted[2])
        self.update()
        self.draw()
        self.talking("You sit on a bench.")
        self.talking("Sitting is really interesting.")
        self.talking("You enjoyed this sitting session.")
        self.talking("But now it's time to continue your journey.")
        self.player.sit(False, self.interacted[1], self.interacted[2])

    def door(self):
        """
        Unlocking/going through door
        """

        # Ground floor
        if self.in_room == ground_floor: self.ground_floor_doors()

        # First floor
        elif self.in_room == first_floor: self.first_floor_doors()

        # Second floor
        elif self.in_room == second_floor: self.second_floor_doors()  
        
        # Third floor
        elif self.in_room == third_floor: self.third_floor_doors()
        
        # Third floor
        elif self.in_room == fourth_floor: self.fourth_floor_doors()
               
    def basement(self):
        """
        Going into the basement
        """
        
        # Light in inventory
        if "light" in self.inv:

            # From right
            if self.interacted[1] == 17 and self.interacted[2] in (192, 193):
                self.talking("I got light with me.")
                self.talking("I'll be able to see now.")
                self.in_room = self.rooms[BASEMENT_FLOOR] # Basement
                self.create_tile_map()
                for sprite in self.all_sprites: sprite.rect.x -= 15 * TILE_SIZE

            # From left
            elif self.interacted[1] in (26, 27) and self.interacted[2] == 116:
                self.talking("I got light with me.")
                self.talking("I'll be able to see now.")
                self.in_room = self.rooms[BASEMENT_FLOOR] # Basement
                self.create_tile_map()
                for sprite in self.all_sprites: sprite.rect.x += 8 * TILE_SIZE
                self.player.rect.x -= 24 * TILE_SIZE

        # No light
        else:

            if self.without_light <= 3:
                self.talking("No way I am going down there without light.")
                self.talking("I don't want to get lost in school.")
                self.talking("I'll go there when I have some light with me.")
                self.without_light += 1
            else:
                self.talking("Welp, you really want me to go down there?")
                self.talking("Let's see.")
                self.game_over("img/lost.png")

    def stairs(self):
        """
        Going up/down the stairs \n
        self.interacted[2] = x coordinates\n
        self.interacted[1] = y coordinates
        """

        # Basement
        if self.interacted[0] == "Stairs_up" and self.in_room == basement:

            # From right
            if self.interacted[1] in (6, 7) and self.interacted[2] == 26:
                self.in_room = self.rooms[GROUND_FLOOR] # Ground floor
                self.create_tile_map()
                for sprite in self.all_sprites: 
                    sprite.rect.x -= 182 * TILE_SIZE
                    sprite.rect.y -= 10 * TILE_SIZE
                self.player.rect.x += 24 * TILE_SIZE
                self.player.rect.y += 10 * TILE_SIZE

            # From left
            if self.interacted[1] in (6, 7) and self.interacted[2] == 0:
                self.in_room = self.rooms[GROUND_FLOOR] # Ground floor
                self.create_tile_map()
                for sprite in self.all_sprites: 
                    sprite.rect.x -= 106 * TILE_SIZE
                    sprite.rect.y -= 20 * TILE_SIZE
                self.player.rect.x -= 53 * TILE_SIZE
                self.player.rect.y += 20 * TILE_SIZE

        # Ground floor -> 1st floor
        elif self.interacted[0] == "Stairs_up" and self.in_room == ground_floor:
            self.in_room = self.rooms[FIRST_FLOOR] # First floor
            self.create_tile_map()

            # Right stairs
            if self.interacted[1] in (16, 17, 18, 19) and self.interacted[2] == 184:
                for sprite in self.all_sprites: 
                    sprite.rect.x -= 171 * TILE_SIZE
                    sprite.rect.y -= 17 * TILE_SIZE
            
            # Left stairs
            elif self.interacted[1] == 13 and self.interacted[2] in (45, 46, 47, 48, 49, 50, 51):
                for sprite in self.all_sprites:
                    sprite.rect.x -= 47 * TILE_SIZE
                    sprite.rect.y -= 17 * TILE_SIZE
                self.player.rect.x -= 124 * TILE_SIZE
                self.player.rect.y += 2 * TILE_SIZE
            
            self.door_info("First floor")
                
        # 1st floor -> Ground floor
        elif self.interacted[0] == "Stairs_down" and self.in_room == first_floor:
            self.in_room = self.rooms[GROUND_FLOOR] # Ground floor
            self.create_tile_map()

            # Right stairs
            if self.interacted[1] in (21, 22, 23, 24) and self.interacted[2] == 181:
                for sprite in self.all_sprites:
                    sprite.rect.x -= 173 * TILE_SIZE
                    sprite.rect.y -= 11 * TILE_SIZE
                self.player.rect.x += 14 * TILE_SIZE
                self.player.rect.y += 11 * TILE_SIZE

            # Left stairs
            elif self.interacted[1] == 24 and self.interacted[2] in (53, 54, 55, 56, 57, 58, 59):
                for sprite in self.all_sprites:
                    sprite.rect.x -= 39 * TILE_SIZE
                    sprite.rect.y -= 7 * TILE_SIZE
                self.player.rect.x -= 120 * TILE_SIZE
                self.player.rect.y += 8 * TILE_SIZE
                
            self.door_info("Ground floor")
        
        # First floor -> Second floor
        elif self.interacted[0] == "Stairs_up" and self.in_room == first_floor:
            self.in_room = self.rooms[SECOND_FLOOR] # Second floor
            self.create_tile_map()
            
            # Right stairs
            if self.interacted[1] in (26, 27, 28, 29) and self.interacted[2] == 181: 
                for sprite in self.all_sprites:
                    sprite.rect.x -= 171 * TILE_SIZE
                    sprite.rect.y -= 18 * TILE_SIZE
            
            # Left stairs
            elif self.interacted[2] in (45, 46, 47, 48, 49, 50, 51) and self.interacted[1] == 24:
                for sprite in self.all_sprites:
                    sprite.rect.x -= 47 * TILE_SIZE
                    sprite.rect.y -= 19 * TILE_SIZE
                self.player.rect.x -= 124 * TILE_SIZE
                self.player.rect.y += 2 * TILE_SIZE
            
            self.door_info("Second floor")
                
        # Second floor -> First floor
        elif self.interacted[0] == "Stairs_down" and self.in_room == second_floor:
            self.in_room = self.rooms[FIRST_FLOOR] # First floor
            self.create_tile_map()

            # Right stairs
            if self.interacted[1] in (22, 23, 24, 25) and self.interacted[2] == 181:
                for sprite in self.all_sprites:
                    sprite.rect.x -= 171 * TILE_SIZE
                    sprite.rect.y -= 19 * TILE_SIZE
                self.player.rect.y += 4 * TILE_SIZE

            # Left stairs
            elif self.interacted[1] == 25 and self.interacted[2] in (53, 54, 55, 56, 57, 58, 59):
                for sprite in self.all_sprites:
                    sprite.rect.x -= 39 * TILE_SIZE
                    sprite.rect.y -= 19 * TILE_SIZE
                self.player.rect.x -= 132 * TILE_SIZE
                self.player.rect.y += 2 * TILE_SIZE
                
            self.door_info("First floor")
        
        # Second floor -> Third floor
        elif self.interacted[0] == "Stairs_up" and self.in_room == second_floor:
            self.in_room = self.rooms[THIRD_FLOOR]
            self.create_tile_map()
            
            if self.interacted[1] in (26, 27, 28, 29) and self.interacted[2] == 181: 
                for sprite in self.all_sprites:
                    sprite.rect.x -= 62 * TILE_SIZE
                    sprite.rect.y -= 4 * TILE_SIZE

            self.door_info("Third floor")
            
        # Third floor -> Second floor
        elif self.interacted[0] == "Stairs_down" and self.in_room == third_floor:
            self.in_room = self.rooms[SECOND_FLOOR]
            self.create_tile_map()
            
            if self.interacted[1] in (8, 9, 10, 11) and self.interacted[2] == 72:
                for sprite in self.all_sprites:
                    sprite.rect.x -= 171 * TILE_SIZE
                    sprite.rect.y -= 20 * TILE_SIZE
                self.player.rect.y += 4 * TILE_SIZE
                    
            self.door_info("Second floor")
            
        # Fourth floor -> Third floor
        elif self.interacted[0] == "Stairs_down" and self.in_room == fourth_floor:
            self.in_room = self.rooms[THIRD_FLOOR]
            self.create_tile_map()
            
            if self.interacted[1] in (8, 9, 10, 11) and self.interacted[2] == 72:
                for sprite in self.all_sprites:
                    sprite.rect.x -= 62 * TILE_SIZE
                    sprite.rect.y -= 7 * TILE_SIZE
                self.player.rect.y += 4 * TILE_SIZE
                    
            self.door_info("Third floor")
            
        # Third floor -> Fourth floor
        elif self.interacted[0] == "Stairs_up" and self.in_room == third_floor:
            self.in_room = self.rooms[FOURTH_FLOOR]
            self.create_tile_map()
            
            if self.interacted[1] in (13, 14, 15, 16) and self.interacted[2] == 72: 
                for sprite in self.all_sprites:
                    sprite.rect.x -= 62 * TILE_SIZE
                    sprite.rect.y -= 4 * TILE_SIZE

            self.door_info("Fourth floor")
                
    def toilet(self):
        """
        PeePeePooPoo time
        """
        self.talking(f"{self.player_name} has PeePeePooPoo time now.")
        

g = Game()
g.intro_screen().new().main()
pygame.quit()