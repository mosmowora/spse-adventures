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
        self.big_font = pygame.font.Font("Caveat.ttf", 32)
        self.font = pygame.font.Font("Roboto.ttf", 22)

        self.character_spritesheet = Spritesheet("img/character.png")
        self.terrain_spritesheet = Spritesheet("img/terrain.png")
        self.npcs_spritesheet = Spritesheet("img/npc.png")

        # Into and Game Over backgrounds
        self.intro_background = pygame.image.load("img/introbackground.png")
        self.game_over_background = pygame.image.load("img/game_over_background.png")

        self.rooms = [ground_floor, first_floor, "chodba_2", "chodba_2_0", "chodba_3", "chodba_3_0", "chodba_4", "chodba_4_0", basement] # Rooms where player can go
        self.in_room = self.rooms[0] # Room where player is rn (starting point)

        # Inventory
        self.inv: List[str] = ["locker key", "changing_room key", "light"]

        # Objects you can interact with
        self.interacted = ["", "", ""]
        self.interactive = {}

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
                if column == "_": Blockade(self, j, i) # Black
                elif column == "!": Block(self, j, i, "!") # No entry ground
                elif column == "P": self.player = Player(self, j, i) # Player
                elif column == "W": Block(self, j, i, "W") # Basic wall
                elif column == "w": Block(self, j, i, "w") # Window
                elif column == "L": self.interactive[Block(self, j, i, "L")] = "L" + str(i) + str(j) # Locker
                elif column == "S": self.interactive[Block(self, j, i, "S")] = "S" + str(i) + str(j) # Stairs
                elif column == "Z": self.interactive[Block(self, j, i, "Z")] = "Z" + str(i) + str(j) # Stairs
                elif column == "s": self.interactive[Block(self, j, i, "s")] = "s" + str(i) + str(j) # Stairs down
                elif column == "z": self.interactive[Block(self, j, i, "z")] = "z" + str(i) + str(j) # Stairs down
                elif column == "D": self.interactive[Block(self, j, i, "D")] = "D" + str(i) + str(j) # Door
                elif column == "B": self.interactive[Block(self, j, i, "B")] = "B" + str(i) + str(j) # Bench
                elif column == "t": self.interactive[Block(self, j, i, "t")] = "t" + str(i) + str(j) # Trashcan
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
            # self.check_active_scene_change(self.in_room)

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

        # Start button
        play_button = Button(10, 50, 100, 50, WHITE, BLACK, "Play", 32)

        # Main loop for intro
        while intro:

            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: intro = self.game_running = False

            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Button was pressed
            if play_button.is_pressed(mouse_pos, mouse_pressed): intro = False

            # Diplaying background, title, button
            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def talking(self, msg_content: str):
        """
        When character is talking
        """

        for _ in range(100):
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
                self.talking("You found a key in the trashcan. It says AR.")

            # Empty trashcan
            else: self.talking("There is nothing interesting.")

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
                    self.talking("I unlocked the locker.")
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
                self.talking("You found the forbidden Kokosky fragment. [1/4]")
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

        # Changing room -> Hall
        if self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 167:

            # Door is locked
            if self.locked_changing_room:

                # Key in inventory
                if "changing_room key" in self.inv: 
                    self.talking("I unlocked the door.")
                    self.locked_changing_room = False

                # No key
                else: self.talking("I need to find key to unlock the door.")
            
            # Door is unlocked
            else: 
                for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
                self.player.rect.y += 2 * TILE_SIZE

        # Hall -> Changing room
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 167: 
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.player.rect.y -= 2 * TILE_SIZE

        # Hall -> Buffet Amper
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 176:
            self.talking("Buffet Amper. I like to buy food here.")
            self.talking("Sadly it's closed now.")

        # Hall -> 020
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 166:
            self.talking("020 - not a classroom")

        # Hall -> 021
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 159: 
            self.talking("021 - not a classroom")

        # Hall -> 022
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 152: 
            self.talking("022 - not a classroom")

        # Hall -> 023
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 133: 
            self.talking("023 - LIT 3")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.player.rect.y += 2 * TILE_SIZE

        # 023 -> Hall
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 133: 
            self.talking("023 - LIT 3")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.player.rect.y -= 2 * TILE_SIZE
            
        # Hall -> ???
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 123: 
            self.talking("??? - not a classroom")

        # Hall -> 025
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 96: 
            self.talking("025 - LCUJ 4")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.player.rect.y += 2 * TILE_SIZE

        # 025 -> Hall 
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 96: 
            self.talking("025 - LCUJ 4")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.player.rect.y -= 2 * TILE_SIZE

        # Hall -> 026
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 88: 
            self.talking("026 - not a classroom")

        # 026 -> Hall
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 88: 
            self.talking("026 - not a classroom")

        # Hall -> 027
        elif self.player.facing == "right" and self.interacted[1] == 25 and self.interacted[2] == 76: 
            self.talking("027 - not a classroom")

        # Hall -> 010
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 33: 
            self.talking("010 - Toilets")

        # Hall -> 009
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 25: 
            self.talking("009 - not a classroom")

        # Hall -> 008
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 19: 
            self.talking("008 - DPXA 3")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.player.rect.y += 2 * TILE_SIZE

        # 008 -> Hall
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 19: 
            self.talking("008 - DPXA 3")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.player.rect.y -= 2 * TILE_SIZE

        # Hall -> 007
        elif self.player.facing == "left" and self.interacted[1] == 17 and self.interacted[2] == 11: 
            self.talking("007 - LIT 10")
            for sprite in self.all_sprites: sprite.rect.x += 2 * TILE_SIZE
            self.player.rect.x -= 2 * TILE_SIZE

        # 007 -> Hall
        elif self.player.facing == "right" and self.interacted[1] == 17 and self.interacted[2] == 11: 
            self.talking("007 - LIT 10")
            for sprite in self.all_sprites: sprite.rect.x -= 2 * TILE_SIZE
            self.player.rect.x += 2 * TILE_SIZE

        # 007 -> 006
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 9:
            self.talking("006 - LIT 9")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.player.rect.y -= 2 * TILE_SIZE

        # 006 -> 007
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 9:
            self.talking("006 - LIT 9")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.player.rect.y += 2 * TILE_SIZE

        # Hall -> 004
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 20: 
            self.talking("004 - LIT 8")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.player.rect.y -= 2 * TILE_SIZE

        # 004 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 20: 
            self.talking("004 - LIT 8")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.player.rect.y += 2 * TILE_SIZE

        # Hall -> 003
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 24: 
            self.talking("003 - DPXA 2")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.player.rect.y -= 2 * TILE_SIZE

        # 003 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 24: 
            self.talking("003 - DPXA 2")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.player.rect.y += 2 * TILE_SIZE

        # Hall -> 002
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 35: 
            self.talking("002 - DPXA 1")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.player.rect.y -= 2 * TILE_SIZE

        # 002 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 35: 
            self.talking("002 - DPXA 1")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.player.rect.y += 2 * TILE_SIZE

        # Hall -> 012
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 79: 
            self.talking("012 - II.A")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.player.rect.y -= 2 * TILE_SIZE

        # 012 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 79: 
            self.talking("012 - II.A")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.player.rect.y += 2 * TILE_SIZE

        # Hall -> 013
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 88: 
            self.talking("013 - II.B")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.player.rect.y -= 2 * TILE_SIZE

        # 013 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 88: 
            self.talking("013 - II.B")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.player.rect.y += 2 * TILE_SIZE

        # Hall -> 014
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 114: 
            self.talking("014 - LAELE")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.player.rect.y -= 2 * TILE_SIZE
        
        # 014 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 114: 
            self.talking("014 - LAELE")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.player.rect.y += 2 * TILE_SIZE

        # Hall -> 015
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 135: 
            self.talking("015 - II.C")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.player.rect.y -= 2 * TILE_SIZE

        # 015 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 135: 
            self.talking("015 - II.C")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.player.rect.y += 2 * TILE_SIZE

        # Hall -> 016
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 159: 
            self.talking("016 - II.SA")
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
            self.player.rect.y -= 2 * TILE_SIZE
                
        # 016 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 159: 
            self.talking("016 - II.SA")
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE
            self.player.rect.y += 2 * TILE_SIZE
                
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
        Going up/down the stairs
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
                    sprite.rect.x -= 172 * TILE_SIZE
                    sprite.rect.y -= 10 * TILE_SIZE
            
            # Left stairs
            elif self.interacted[1] == 13 and self.interacted[2] in (45, 46, 47, 48, 49, 50, 51):
                for sprite in self.all_sprites:
                    sprite.rect.x -= 47 * TILE_SIZE
                    sprite.rect.y -= 13 * TILE_SIZE
                self.player.rect.x -= 126 * TILE_SIZE
                self.player.rect.y += 2 * TILE_SIZE
                
        # 1st floor -> Ground floor
        elif self.interacted[0] == "Stairs_down" and self.in_room == first_floor:
            self.in_room = self.rooms[0] # Ground floor
            self.create_tile_map()

            # Right stairs
            if self.interacted[1] in (16, 17, 18, 19) and self.interacted[2] == 183:
                for sprite in self.all_sprites:
                    sprite.rect.x -= 173 * TILE_SIZE
                    sprite.rect.y -= 11 * TILE_SIZE
                self.player.rect.x += 14 * TILE_SIZE
                self.player.rect.y += 11 * TILE_SIZE

            # Left stairs
            elif self.interacted[1] == 20 and self.interacted[2] in (52, 53, 54, 55, 56, 57, 58):
                for sprite in self.all_sprites:
                    sprite.rect.x -= 39 * TILE_SIZE
                    sprite.rect.y -= 7 * TILE_SIZE
                self.player.rect.x -= 120 * TILE_SIZE
                self.player.rect.y += 8 * TILE_SIZE
        

g = Game()
g.intro_screen()
g.new()

while g.game_running:
    g.main()
    g.game_over()

pygame.quit()