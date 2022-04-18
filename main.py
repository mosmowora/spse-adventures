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
        self.big_font = pygame.font.Font("Roboto.ttf", 32)
        self.font = pygame.font.Font("Roboto.ttf", 22)

        self.character_spritesheet = Spritesheet("img/character.png")
        self.terrain_spritesheet = Spritesheet("img/terrain.png")
        self.npcs_spritesheet = Spritesheet("img/npc.png")

        # Into and Game Over backgrounds
        self.intro_background = pygame.image.load("img/introbackground.png")
        self.game_over_background = pygame.image.load("img/game_over_background.png")

        self.rooms = [satna, satna_1, chodba_0, chodba_0_1, chodba_1, chodba_1_0, chodba_0_2, "chodba_2", "chodba_2_0", "chodba_3", "chodba_3_0", "chodba_4", "chodba_4_0", basement] # Rooms where player can go
        self.in_room = self.rooms[0] # Room where player is rn (starting point)

        # Inventory
        self.inv = ["kluc od skrinky", "light"]

        # Objects you can interact with
        self.interacted = ""
        self.interactive = {}
    
        # Variables for finding items/doing stuff
        self.key_in_trash = True
        self.locked_locker = True
        self.locked_changing_room = True
        self.key_in_locker = True
        self.kokosky_in_locker = True

        self.x_hop = 0
        self.y_hop = 0

    def create_tile_map(self):
        """
        Creates tile map
        """

        self.interactive = {}

        for sprite in self.all_sprites: sprite.kill()

        for i, row in enumerate(self.in_room):
            for j, column in enumerate(row):
                Ground(self, j, i, column)
                if column == "_": Blockade(self, j, i) # Black
                elif column == "P": self.player = Player(self, j, i) # Player
                elif column == "W": Block(self, j, i, "W") # Basic wall
                elif column == "w": Block(self, j, i, "w") # Window
                elif column == "L": self.interactive[Block(self, j, i, "L")] = "L" + str(i) + str(j) # Locker
                elif column == "S": self.interactive[Block(self, j, i, "S")] = "S" + str(i) + str(j) # Stairs
                elif column == "g": self.interactive[Block(self, j, i, "g")] = "g" + str(i) + str(j) # Stairs down
                elif column == "D": self.interactive[Block(self, j, i, "D")] = "D" + str(i) + str(j) # Door
                elif column == "B": self.interactive[Block(self, j, i, "B")] = "B" + str(i) + str(j) # Bench
                elif column == "t": self.interactive[Block(self, j, i, "t")] = "t" + str(i) + str(j) # Trashcan
                elif column == "R": self.interactive[Block(self, j, i, "R")] = "R" + str(i) + str(j) # Rails
                elif column == "b": self.interactive[Block(self, j, i, "b")] = "b" + str(i) + str(j) # Rails
                elif column == "N": Npc(self, j, i) # NPC

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

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e: 
                match self.player.facing:
                    case "up": Interact(self, self.player.rect.x, self.player.rect.y - TILE_SIZE, self.interactive)
                    case "down": Interact(self, self.player.rect.x, self.player.rect.y + TILE_SIZE, self.interactive)
                    case "left": Interact(self, self.player.rect.x - TILE_SIZE, self.player.rect.y, self.interactive)
                    case "right": Interact(self, self.player.rect.x + TILE_SIZE, self.player.rect.y, self.interactive) 
                
                match self.interacted.capitalize():
                    case "Trashcan": self.trashcan()
                    case "Door": self.door()
                    case "Locker": self.locker()
                    case "Bench": self.bench()
                    case "Stairs": self.stairs()
                    case "Sters": self.stairs()
                    case "Basement": self.basement()
                self.interacted = ""


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

    def talking(self, content):
        """
        When character is talking
        """

        for _ in range(100):
            text = self.font.render(content, True, WHITE)
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

        if self.in_room == satna or self.in_room == satna_1:
            self.talking("There's paper on the side of the trashcan.")
            self.talking("It says 2.SA. You agree with this statement.")
            if self.key_in_trash: 
                self.inv.append("kluc od skrinky")
                self.key_in_trash = False 
                self.talking("You found a key in the trashcan. It says AR.")
            else: self.talking("There is nothing interesting.")

    def locker(self):
        """
        Unlocking the locker
        """

        if self.in_room == satna or self.in_room == satna_1:
            if self.interacted == "LOCKER":
                if self.locked_locker:
                    if "kluc od skrinky" in self.inv:
                        self.talking("I unlocked the locker.")
                        self.locked_locker = False
                    else: self.talking("Locked locker.")
                else: 
                    if self.key_in_locker:
                        self.inv.append("kluc od satne")
                        self.talking("There's a key. It seems to be the key from this room.")
                        self.key_in_locker = False
                    else: self.talking("It's empty.")
            elif self.interacted == "locker":
                if self.kokosky_in_locker:
                    self.talking("Wow, what is this?")
                    self.talking("You found the forbidden Kokosky fragment. [1/4]")
                    self.kokosky_in_locker = False
                    self.inv.append("Kokosky1")
                else: self.talking("It's empty, but smells.")
            else: 
                if "kluc od skrinky" in self.inv and self.key_in_locker: self.talking("Wrong locker.")
                else: self.talking("Locked locker.")

    def bench(self):
        """
        Sitting on the bench
        """

        self.player.sit(True, self.x_hop, self.y_hop)
        self.update()
        self.draw()
        self.talking("You sit on a bench.")
        self.talking("Sitting is really interesting.")
        self.talking("You enjoyed this sitting session.")
        self.talking("But now it's time to continue your journey.")
        self.player.sit(False, self.x_hop, self.y_hop)
        
    def basement(self):
        """
        Going into the basement
        """
        
        if "light" in self.inv:
            self.talking("I got light with me.")
            self.talking("I'll be able to see now.")
            self.in_room = self.rooms[-1]
            self.create_tile_map()
            for sprite in self.all_sprites: sprite.rect.x -= 16 * TILE_SIZE
        else:
            self.talking("No way I am going down there without light.")
            self.talking("I don't want to get lost in school.")
            self.talking("I'll go there when I have some light with me.")

    def door(self):
        """
        Unlocking/going through door
        """
        # satne
        if self.in_room == satna or self.in_room == satna_1:
            if self.locked_changing_room:
                if "kluc od satne" in self.inv: 
                    self.talking("I unlocked the door.")
                    self.locked_changing_room = False
                else: self.talking("I need to find key to unlock the door.")
            else: 
                self.in_room = self.rooms[2]
                self.create_tile_map()
                for sprite in self.all_sprites: sprite.rect.x -= 65 * TILE_SIZE

        # Prizemie
        elif self.in_room in (chodba_0, chodba_0_1, chodba_0_2):
            if self.interacted == "DOOR":
                self.in_room = self.rooms[1]
                self.create_tile_map()
                for sprite in self.all_sprites: sprite.rect.y -= 7 * TILE_SIZE
            elif self.interacted == "door":
                self.talking("Buffet Amper. I like to buy food here.")
                self.talking("Sadly it's closed now.")
                

    def stairs(self):
        """
        Going up/down the stairs
        """
        # Basement
        if self.interacted == "Stairs" and self.in_room == basement:
            self.in_room = self.rooms[6]    # chodba_0_2
            self.create_tile_map()
            for sprite in self.all_sprites: 
                sprite.rect.x -= 88 * TILE_SIZE
                sprite.rect.y += 2 * TILE_SIZE

        # Prizemie = hore schodmi
        elif self.interacted == "Stairs" and self.in_room in (chodba_0, chodba_0_1, chodba_0_2) or self.interacted == "Stairs" and self.in_room in (chodba_1, chodba_1_0):
            self.in_room = self.rooms[4]    # chodba_1
            self.create_tile_map()
            for sprite in self.all_sprites: sprite.rect.x -= 80 * TILE_SIZE
        
        # Prizemie = dole schodmi
        elif self.interacted == "Sters" and self.in_room in (chodba_0, chodba_0_1, chodba_0_2):
            self.in_room = self.rooms[3]    # chodba_0_1
            self.create_tile_map()
            for sprite in self.all_sprites: sprite.rect.x -= 50 * TILE_SIZE
            
        # 1. Poschodie = dole schodmi
        elif self.interacted == "Sters" and self.in_room in (chodba_1, chodba_1_0, chodba_0_2):
            self.in_room = self.rooms[3]    # chodba_0_1
            self.create_tile_map()
            for sprite in self.all_sprites: sprite.rect.x -= 80 * TILE_SIZE
        


g = Game()
g.intro_screen()
g.new()

while g.game_running:
    g.main()
    g.game_over()

pygame.quit()