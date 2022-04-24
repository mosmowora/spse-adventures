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

        # Spritesheets
        self.character_spritesheet = Spritesheet("img/character.png")
        self.terrain_spritesheet = Spritesheet("img/terrain.png")
        self.npcs_spritesheet = Spritesheet("img/npc.png")

        # Into and Game Over backgrounds
        self.intro_background = pygame.image.load("img/intro_background.png")
        self.game_over_background = pygame.image.load("img/game_over_background.png")
        
        # Window icon and title (not final)
        icon = pygame.image.load('img/spselogo.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('SPŠE ADVENTURE')

        self.rooms: List[List[str]] = [ground_floor, first_floor, second_floor, basement] # Rooms where player can go
        self.in_room: List[str] = self.rooms[0] # Room where player is rn (starting point)

        # Inventory
        self.inv: List[str] = ["locker key", "changing_room key", "light"]

        # Objects you can interact with
        self.interacted: List[str] = ["", "", "", "", ""]
        self.interactive= {}

        # Player name
        self.player_name: str = ""

        self.npc = []
    
        # Variables for finding items/doing stuff
        self.key_in_trash = True
        self.locked_locker = True
        self.locked_changing_room = True
        self.key_in_locker = True
        self.kokosky_in_locker = True

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
                elif column == "B": self.interactive[Block(self, j, i, "B")] = "B" + str(i) + str(j) # Bench
                elif column == "t": self.interactive[Block(self, j, i, "t")] = "t" + str(i) + str(j) # Trashcan
                elif column == "T": self.interactive[Block(self, j, i, "T")] = "T" + str(i) + str(j) # Toilet
                elif column == "Ť": self.interactive[Block(self, j, i, "Ť")] = "Ť" + str(i) + str(j) # Toilet
                elif column == "R": self.interactive[Block(self, j, i, "R")] = "R" + str(i) + str(j) # Rails
                elif column == "r": self.interactive[Block(self, j, i, "r")] = "r" + str(i) + str(j) # Rails
                elif column == "Ř": self.interactive[Block(self, j, i, "Ř")] = "Ř" + str(i) + str(j) # Rails ground_floor
                elif column == "ř": self.interactive[Block(self, j, i, "ř")] = "ř" + str(i) + str(j) # Rails ground_floor
                elif column == "b": self.interactive[Block(self, j, i, "b")] = "b" + str(i) + str(j) # Basement
                elif column == "d": self.interactive[Block(self, j, i, "d")] = "d" + str(i) + str(j) # Basement
                elif column == "N": self.npc.append(Npc(self, j, i)) # NPC

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

        # Tilemap
        self.create_tile_map()

        for sprite in self.all_sprites: sprite.rect.x -= 158 * TILE_SIZE
    
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
            if event.type == pygame.QUIT: self.playing = self.game_running = False

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

    def game_over(self):
        """
        Game over screen
        """

        # Creates text
        text = self.big_font.render("Game Over", True, BLACK)
        text_rect = text.get_rect(center = (75, 50))

        # Creates button
        restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, "Restart", 32)

        # Removing every sprite
        for sprite in self.all_sprites: sprite.kill()

        # Loop
        while self.game_running:

            # Close button
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.game_running = False

            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed): 
                self.new()
                self.main()

            # Displaying background, text, button
            self.screen.blit(self.game_over_background, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS // 2)
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
        play_button = Button(10, 60, 180, 50, WHITE, BLACK, "Play", 32)

        # Settings button
        settings_button = Button(10, 120, 180, 50, WHITE, BLACK, "Settings", 32)

        # Leaderboard button
        leaderboard_button = Button(10, 180, 180, 50, WHITE, BLACK, "Leaderboard", 32)

        # Main loop for intro
        while intro:

            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: intro = self.game_running = False

            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Play button was pressed
            if play_button.is_pressed(mouse_pos, mouse_pressed): self.start(); break

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
    
    
    def start(self):
        """
        Starting the game
        """

        picking_name = True
        active = False

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
                if event.type == pygame.QUIT:
                    pygame.quit()
        
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
                        if len(self.player_name) > 0: picking_name = False

                    # Unicode
                    elif active: self.player_name += event.unicode

            # Background
            self.screen.blit(self.intro_background, (0, 0))

            # Your name
            self.screen.blit(your_name, your_name_rect)

            if active: color = GRAY
            else: color = BLACK

            # Input rectangle
            pygame.draw.rect(self.screen, color, input_rect)
    
            # Text
            text_surface = self.font.render(self.player_name, True, (255, 255, 255))
            self.screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))

            # Width of rectangle
            input_rect.w = max(200, text_surface.get_width()+10)

            # Other
            self.screen.blit(made, made_rect)
            self.screen.blit(title, title_rect)
            self.clock.tick(FPS)
            pygame.display.flip()
    

    def settings(self):
        """
        Opens settings window
        """
        print("If we had one")

    def leaderboard(self):
        """
        Opens leaderboard window
        """
        print("If we had one")

    def door_info(self, msg_content: str):
        """
        Displays info about the room the character is entering/exiting
        """

        for _ in range(35):
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

        for _ in range(80):
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
            self.player.rect.y = self.interacted[4] + TILE_SIZE
        
        # Facing down
        elif self.player.facing == "down":
            self.player.rect.x = self.interacted[3]
            self.player.rect.y = self.interacted[4] - TILE_SIZE

        # Facing left
        elif self.player.facing == "left":
            self.player.rect.x = self.interacted[3] + TILE_SIZE
            self.player.rect.y = self.interacted[4]

        # Facing right
        elif self.player.facing == "right":
            self.player.rect.x = self.interacted[3] - TILE_SIZE
            self.player.rect.y = self.interacted[4]

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
                else: 
                    self.talking(f"{self.player_name} can't find key to unlock the door.")
                    
            # Door is unlocked
            else: 
                for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
                self.center_player_after_doors()

        # Hall -> Changing room
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 167: 
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()

        # Hall -> Buffet Amper
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 176:
            self.talking("Buffet Amper. I like to buy food here.")
            self.talking("Sadly it's closed now.")

        # Hall -> 020
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 166:
            self.door_info("020 - not a classroom")

        # Hall -> 021
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 159: 
            self.door_info("021 - not a classroom")

        # Hall -> 022
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 152: 
            self.door_info("022 - not a classroom")

        # Hall -> 023
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 133: 
            self.door_info("023 - LIT 3")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()

        # 023 -> Hall
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 133: 
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()
            
        # Hall -> ???
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 123: 
            self.door_info("??? - not a classroom")

                # Hall -> 025
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 96: 
            self.door_info("025 - LCUJ 4")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()

        # 025 -> Hall 
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 96: 
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()

        # Hall -> 026
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 88: 
            self.door_info("026 - not a classroom")

        # 026 -> Hall
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 88: 
            self.door_info("026 - not a classroom")

        # Hall -> 027
        elif self.player.facing == "right" and self.interacted[1] == 25 and self.interacted[2] == 76: 
            self.door_info("027 - not a classroom")

        # Hall -> 010
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 33: 
            self.door_info("010 - Toilets")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()

        # 010 -> Hall
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 33: 
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()

        # Toilet room -> Stall
        elif self.player.facing == "up" and self.interacted[1] == 24 and self.interacted[2] in (37, 39):
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()

        # Stall -> Toilet room
        elif self.player.facing == "down" and self.interacted[1] == 24 and self.interacted[2] in (37, 39):
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()

        # Hall -> 009
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 25: 
            self.door_info("009 - not a classroom")

        # Hall -> 008
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 19: 
            self.door_info("008 - DPXA 3")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()

        # 008 -> Hall
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 19: 
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()

        # Hall -> 007
        elif self.player.facing == "left" and self.interacted[1] == 17 and self.interacted[2] == 11: 
            self.door_info("007 - LIT 10")
            for sprite in self.all_sprites: sprite.rect.x += 2 * TILE_SIZE
            self.center_player_after_doors()

        # 007 -> Hall
        elif self.player.facing == "right" and self.interacted[1] == 17 and self.interacted[2] == 11: 
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.x -= 2 * TILE_SIZE
            self.center_player_after_doors()

        # 007 -> 006
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 9:
            self.door_info("006 - LIT 9")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()

        # 006 -> 007
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 9: 
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()

        # Hall -> 004
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 20: 
            self.door_info("004 - LIT 8")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()

        # 004 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 20: 
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()

        # Hall -> 003
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 24: 
            self.door_info("003 - DPXA 2")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()

        # 003 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 24: 
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()

        # Hall -> 002
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 35: 
            self.door_info("002 - DPXA 1")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()

        # 002 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 35: 
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()

        # Hall -> 012
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 79: 
            self.door_info("012 - II.A")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()

        # 012 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 79: 
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()

        # Hall -> 013
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 88: 
            self.door_info("013 - II.B")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()

        # 013 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 88: 
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()

        # Hall -> 014
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 114: 
            self.door_info("014 - LAELE")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # 014 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 114: 
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()

        # Hall -> 015
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 135: 
            self.door_info("015 - II.C")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()

        # 015 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 135: 
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()

        # Hall -> 016
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 159: 
            self.door_info("016 - II.SA")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()
                
        # 016 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 159: 
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()
            
    def first_floor_doors(self):
        """
        Doors on the first floor
        """

        # Hall -> 122/1
        if self.player.facing == "right" and self.interacted[2] == 173 and self.interacted[1] in (11, 12):
            self.door_info("122/1 -  LIT 1 (III.SA)")
            for sprite in self.all_sprites: sprite.rect.x -= 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # 122/1 -> Hall
        elif self.player.facing == "left" and self.interacted[2] == 173 and self.interacted[1] in (11, 12):
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.x += 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # 122/1 -> 122/2
        elif self.player.facing == "up" and self.interacted[2] == 177 and self.interacted[1] == 7:
            self.door_info("122/2 -  LIT 2 (IV.SA)")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # 122/2 -> 122/1
        elif self.player.facing == "down" and self.interacted[2] == 177 and self.interacted[1] == 7:
            self.door_info("122/1 -  LIT 1 (III.SA)")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()
            
        # Hall -> Kabinet pri 122/1
        elif self.player.facing == "right" and self.interacted[2] == 173 and self.interacted[1] == 17:
            for sprite in self.all_sprites: sprite.rect.x -= 2 * TILE_SIZE
            self.center_player_after_doors()
            
        # Kabinet pri 122/1 -> Hall
        elif self.player.facing == "left" and self.interacted[2] == 173 and self.interacted[1] == 17:
            for sprite in self.all_sprites: sprite.rect.x += 2 * TILE_SIZE
            self.center_player_after_doors()
            
        # Hall -> Kabinet HED, MIT
        elif self.player.facing == "up" and self.interacted[2] == 169 and self.interacted[1] == 7:
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()
            
        # Kabinet HED, MIT -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 169 and self.interacted[1] == 7:
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()
            
        # Hall -> Toilets
        elif self.player.facing == "left" and self.interacted[2] == 166 and self.interacted[1] == 16:
            self.door_info("Toilets")
            for sprite in self.all_sprites: sprite.rect.x += 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # Toilets -> Stall
        elif self.player.facing == "down" and self.interacted[2] == 161 and self.interacted[1] == 17:
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()

        # Stall -> Toilets
        elif self.player.facing == "up" and self.interacted[2] == 161 and self.interacted[1] == 17:
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()

        # Toilets -> Hall
        elif self.player.facing == "right" and self.interacted[2] == 166 and self.interacted[1] == 16:
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.x -= 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # Hall -> 117
        elif self.player.facing == "up" and self.interacted[2] == 155 and self.interacted[1] == 23:
            self.door_info("117 - III.B")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # 117 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 155 and self.interacted[1] == 23:
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # Hall -> 115
        elif self.player.facing == "up" and self.interacted[2] == 128 and self.interacted[1] == 23:
            self.door_info("115 - IV.SB")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # 115 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 128 and self.interacted[1] == 23:
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # Hall -> 113
        elif self.player.facing == "up" and self.interacted[2] == 93 and self.interacted[1] == 23:
            self.door_info("113 - III.C")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # 113 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 93 and self.interacted[1] == 23:
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # Hall -> 112
        elif self.player.facing == "up" and self.interacted[2] == 76 and self.interacted[1] == 23:
            self.door_info("112 - LELM 1")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # 112 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 76 and self.interacted[1] == 23:
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # Hall -> 124
        elif self.player.facing == "down" and self.interacted[2] == 160 and self.interacted[1] == 29:
            self.door_info("124 - LELM 2")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # 124 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 160 and self.interacted[1] == 29:
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # Hall -> 126
        elif self.player.facing == "down" and self.interacted[2] == 141 and self.interacted[1] == 29:
            self.door_info("126 - LSIE 2")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # 126 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 141 and self.interacted[1] == 29:
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # Hall -> 127
        elif self.player.facing == "down" and self.interacted[2] == 126 and self.interacted[1] == 29:
            self.door_info("127 - LIOT")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # 127 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 126 and self.interacted[1] == 29:
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # Hall -> 130
        elif self.player.facing == "down" and self.interacted[2] == 104 and self.interacted[1] == 29:
            self.door_info("130 - CZV")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.center_player_after_doors()
        
        # 130 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 104 and self.interacted[1] == 29:
            self.door_info("Hall")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.center_player_after_doors()
            
    
    def second_floor_doors(self): pass
        
               
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
            else:

                # Key in locker
                if self.key_in_locker:
                    self.inv.append("changing_room key")
                    self.talking("There's a key. It seems to be the key from this room.")
                    self.key_in_locker = False

                # Locker empty
                else: self.talking("It's empty.")
        
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
            if "locker key" in self.inv and self.key_in_locker: self.talking("Wrong locker.")
            
            # No key
            else: self.talking("Locked locker.")

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
                self.in_room = self.rooms[-1] # Basement
                self.create_tile_map()
                for sprite in self.all_sprites: sprite.rect.x -= 15 * TILE_SIZE

            # From left
            elif self.interacted[1] in (26, 27) and self.interacted[2] == 116:
                self.talking("I got light with me.")
                self.talking("I'll be able to see now.")
                self.in_room = self.rooms[-1] # Basement
                self.create_tile_map()
                for sprite in self.all_sprites: sprite.rect.x += 8 * TILE_SIZE
                self.player.rect.x -= 24 * TILE_SIZE

        # No light
        else:
            self.talking("No way I am going down there without light.")
            self.talking("I don't want to get lost in school.")
            self.talking("I'll go there when I have some light with me.")

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
                self.in_room = self.rooms[0] # Ground floor
                self.create_tile_map()
                for sprite in self.all_sprites: 
                    sprite.rect.x -= 182 * TILE_SIZE
                    sprite.rect.y -= 10 * TILE_SIZE
                self.player.rect.x += 24 * TILE_SIZE
                self.player.rect.y += 10 * TILE_SIZE

            # From left
            if self.interacted[1] in (6, 7) and self.interacted[2] == 0:
                self.in_room = self.rooms[0] # Ground floor
                self.create_tile_map()
                for sprite in self.all_sprites: 
                    sprite.rect.x -= 106 * TILE_SIZE
                    sprite.rect.y -= 20 * TILE_SIZE
                self.player.rect.x -= 53 * TILE_SIZE
                self.player.rect.y += 20 * TILE_SIZE

        # Ground floor -> 1st floor
        elif self.interacted[0] == "Stairs_up" and self.in_room == ground_floor:
            self.in_room = self.rooms[1] # First floor
            self.create_tile_map()

            # Right stairs
            if self.interacted[1] in (16, 17, 18, 19) and self.interacted[2] == 183:
                for sprite in self.all_sprites: 
                    sprite.rect.x -= 171 * TILE_SIZE
                    sprite.rect.y -= 14 * TILE_SIZE
            
            # Left stairs
            elif self.interacted[1] == 13 and self.interacted[2] in (45, 46, 47, 48, 49, 50, 51):
                for sprite in self.all_sprites:
                    sprite.rect.x -= 47 * TILE_SIZE
                    sprite.rect.y -= 17 * TILE_SIZE
                self.player.rect.x -= 124 * TILE_SIZE
                self.player.rect.y += 2 * TILE_SIZE
                
        # 1st floor -> Ground floor
        elif self.interacted[0] == "Stairs_down" and self.in_room == first_floor:
            self.in_room = self.rooms[0] # Ground floor
            self.create_tile_map()

            # Right stairs
            if self.interacted[1] in (20, 21, 22, 23) and self.interacted[2] == 181:
                for sprite in self.all_sprites:
                    sprite.rect.x -= 173 * TILE_SIZE
                    sprite.rect.y -= 11 * TILE_SIZE
                self.player.rect.x += 14 * TILE_SIZE
                self.player.rect.y += 11 * TILE_SIZE

            # Left stairs
            elif self.interacted[1] == 23 and self.interacted[2] in (53, 54, 55, 56, 57, 58, 59):
                for sprite in self.all_sprites:
                    sprite.rect.x -= 39 * TILE_SIZE
                    sprite.rect.y -= 7 * TILE_SIZE
                self.player.rect.x -= 120 * TILE_SIZE
                self.player.rect.y += 8 * TILE_SIZE
        
        # First floor -> Second floor
        elif self.interacted[0] == "Stairs_up" and self.in_room == first_floor:
            self.in_room = self.rooms[2]
            self.create_tile_map()
            
            # Right stairs
            if self.interacted[1] in (25, 26, 27, 28) and self.interacted[2] == 181: 
                for sprite in self.all_sprites:
                    sprite.rect.x -= 171 * TILE_SIZE
                    sprite.rect.y -= 11 * TILE_SIZE
            
            # Left stairs
            elif self.interacted[1] in (45, 46, 47, 48, 49, 50, 51) and self.interacted[2] == 23:
                for sprite in self.all_sprites:
                    sprite.rect.x -= 39 * TILE_SIZE
                    sprite.rect.y -= 7 * TILE_SIZE
                self.player.rect.x -= 120 * TILE_SIZE
                self.player.rect.y += 8 * TILE_SIZE
                
        # Second floor -> First floor (TO BE ADDED)

    def toilet(self):
        """
        PeePeePooPoo time
        """
        self.talking(f"{self.player_name} has PeePeePooPoo time now.")
        

g = Game()
g.intro_screen().new()

while g.game_running: g.main().game_over()

pygame.quit()