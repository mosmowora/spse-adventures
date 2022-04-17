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
        self.running = True
        self.big_font = pygame.font.Font("Roboto.ttf", 32)
        self.font = pygame.font.Font("Roboto.ttf", 22)

        self.character_spritesheet = Spritesheet("img/character.png")
        self.terrain_spritesheet = Spritesheet("img/terrain.png")
        self.npcs_spritesheet = Spritesheet("img/npc.png")

        # Into and Game Over backgrounds
        self.intro_background = pygame.image.load("img/introbackground.png")
        self.game_over_background = pygame.image.load("img/game_over_background.png")

        self.rooms = [satna, satna_1, chodba_0, "chodba_1", "chodba_2", "chodba_3", "chodba_4"] # skolske poschodia a mozne roomky do ktorych moze hrac vojst
        self.in_room = self.rooms[0] # hrac v danej roomke

        # Inventory
        self.inv = ["kluc od satne"]

        # Objects you can interact with
        self.interacted = ""
        self.interactive = {}
    
        # Variables for finding items/doing stuff
        self.kluc_v_kosi = True
        self.zamknuta_skrinka = True
        self.zamknuta_satna = True
        self.kluc_v_skrinke = True
        self.kokosky_v_skrinke = True

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
                Ground(self, j, i)
                if column == "_": Blockade(self, j, i) # Black
                elif column == "W": Block(self, j, i, "W") # Basic wall
                elif column == "S": self.interactive[Block(self, j, i, "S")] = "S" + str(i) + str(j) # Skrinka
                elif column == "O": Block(self, j, i, "O") # Okno
                elif column == "D": self.interactive[Block(self, j, i, "D")] = "D" + str(i) + str(j) # Dvere
                elif column == "L": self.interactive[Block(self, j, i, "L")] = "L" + str(i) + str(j) # Lavicka
                elif column == "T": self.interactive[Block(self, j, i, "T")] = "K" + str(i) + str(j) # Trashcan
                elif column == "P": self.player = Player(self, j, i) # Player
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
            if event.type == pygame.QUIT: self.playing = self.running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e: 
                match self.player.facing:
                    case "up": Interact(self, self.player.rect.x, self.player.rect.y - TILE_SIZE, self.interactive)
                    case "down": Interact(self, self.player.rect.x, self.player.rect.y + TILE_SIZE, self.interactive)
                    case "left": Interact(self, self.player.rect.x - TILE_SIZE, self.player.rect.y, self.interactive)
                    case "right": Interact(self, self.player.rect.x + TILE_SIZE, self.player.rect.y, self.interactive) 
                
            # print(f"x:{self.player_pos[0]}, y:{self.player_pos[1]}")

                match self.interacted.capitalize():
                    case "Kos": self.hrabanie_v_kosi()
                    case "Dvere": self.dvere()
                    case "Skrinka": self.skrinka()
                    case "Lavicka": self.lavicka()


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

        self.animate()

        # Creates text
        text = self.big_font.render("Game Over", True, BLACK)
        text_rect = text.get_rect(center = (75, 50))

        # Creates button
        restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, "Restart", 32)

        # Removing every sprite
        for sprite in self.all_sprites: sprite.kill()

        # Loop
        while self.running:

            # Close button
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False

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
                if event.type == pygame.QUIT: intro = self.running = False

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

    def hrabanie_v_kosi(self):
        """
        Hrabanie v kosi
        """

        if self.in_room == satna or self.in_room == satna_1:
            self.talking("There's paper on the side of the trashcan.")
            self.talking("It says 2.SA. You agree with this statement.")
            if self.kluc_v_kosi: 
                self.inv.append("kluc od skrinky")
                self.kluc_v_kosi = False 
                self.talking("You found a key in the trashcan. It says AR.")
            else: self.talking("There is nothing interesting.")

    def skrinka(self):
        """
        Odomknutie skrinky
        Hladnie v skrinke
        """

        if self.in_room == satna or self.in_room == satna_1:
            if self.interacted == "SKRINKA":
                if self.zamknuta_skrinka:
                    if "kluc od skrinky" in self.inv:
                        self.talking("I unlocked the locker.")
                        self.zamknuta_skrinka = False
                    else: self.talking("Locked locker.")
                else: 
                    if self.kluc_v_skrinke:
                        self.inv.append("kluc od satne")
                        self.talking("There's a key. It seems to be the key from this room.")
                        self.kluc_v_skrinke = False
                    else: self.talking("It's empty.")
            elif self.interacted == "skrinka":
                if self.kokosky_v_skrinke:
                    self.talking("Wow, what is this?")
                    self.talking("You found the forbidden Kokosky fragment. [1/4]")
                    self.kokosky_v_skrinke = False
                    self.inv.append("Kokosky1")
                else: self.talking("It's empty, but smells.")
            else: 
                if "kluc od skrinky" in self.inv and self.kluc_v_skrinke: self.talking("Wrong locker.")
                else: self.talking("Locked locker.")

    def lavicka(self):
        """
        Sadnut si na lavicku
        """

        self.player.sit(True, self.x_hop, self.y_hop)
        self.update()
        self.draw()
        self.talking("You sit on a bench.")
        self.talking("Sitting is really interesting.")
        self.talking("You enjoyed this sitting session.")
        self.talking("But now it's time to continue your journey.")
        self.player.sit(False, self.x_hop, self.y_hop)

    def dvere(self):
        """
        Odomknutie/prejdenie dverami
        """

        if self.in_room == satna or self.in_room == satna_1:
            if self.zamknuta_satna:
                if "kluc od satne" in self.inv: 
                    self.talking("I unlocked the door.")
                    self.zamknuta_satna = False
                else: self.talking("I need to find key to unlock the door.")
            else: 
                self.in_room = self.rooms[2]
                self.create_tile_map()
                for sprite in self.all_sprites: sprite.rect.x -= 35 * TILE_SIZE

        elif self.in_room == chodba_0:
            self.in_room = self.rooms[1]
            self.create_tile_map()
            for sprite in self.all_sprites: sprite.rect.y -= 7 * TILE_SIZE


g = Game()
g.intro_screen()
g.new()

while g.running:
    g.main()
    g.game_over()

pygame.quit()