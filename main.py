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
        self.font = pygame.font.Font("Roboto.ttf", 32)

        self.character_spritesheet = Spritesheet("img/character.png")
        self.terrain_spritesheet = Spritesheet("img/terrain.png")
        self.npcs_spritesheet = Spritesheet("img/npc.png")

        # Into and Game Over backgrounds
        self.intro_background = pygame.image.load("img/introbackground.png")
        self.game_over_background = pygame.image.load("img/game_over_background.png")

        self.rooms = [satna, chodba_0, "chodba_1", "chodba_2", "chodba_3", "chodba_4"] # skolske poschodia a mmozne roomky do ktorych moze hrac vojst
        self.in_room = self.rooms[0] # hrac v danej roomke
    
    def create_tile_map(self):
        """
        Creates tile map
        """

        for i, row in enumerate(self.in_room):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "_": Blockade(self, j, i) # Black
                elif column == "W": Block(self, j, i, "W") # Basic wall
                elif column == "S": Block(self, j, i, "S") # Skrinka
                elif column == "O": Block(self, j, i, "O") # Okno
                elif column == "D": Block(self, j, i, "D") # Dvere
                elif column == "L": Block(self, j, i, "L") # Lavicka
                elif column == "T": Block(self, j, i, "T") # Trashcan
                elif column == "P": self.player = Player(self, j, i) # Player
                elif column == "N": Npc(self, j, i) # NPC
        
        return (self.player.x, self.player.y)
                

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
        self.player_pos = self.create_tile_map()
        
    # def check_active_scene_change(self, scene: str):
        # "satna", "chodba_0", "chodba_1", "chodba_2", "chodba_3", "chodba_4"
        # match scene:
        #     case "satna":
        #         if self.player_pos.x: 
        
        
    def change_rooms(self, previous_scene: str):
        """
        Changes the map for player to play in
        """

        if self.rooms.index(previous_scene) + 1 >= len(self.rooms): print("No other room available")
        else: self.in_room = self.rooms.index(previous_scene) + 1

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
                    case "up": Interact(self, self.player.rect.x, self.player.rect.y - TILE_SIZE) 
                    case "down": Interact(self, self.player.rect.x, self.player.rect.y + TILE_SIZE)
                    case "left": Interact(self, self.player.rect.x - TILE_SIZE, self.player.rect.y)
                    case "right": Interact(self, self.player.rect.x + TILE_SIZE, self.player.rect.y) 
                
            # print(f"x:{self.player_pos[0]}, y:{self.player_pos[1]}")


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
        self.all_sprites.draw(self.screen) # Draws sprites onto the scree
        self.clock.tick(FPS) # How often does the game update
        pygame.display.update()

    def game_over(self):
        """
        Game over screen
        """

        # Creates text
        text = self.font.render("Game Over", True, BLACK)
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
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        """
        Intro screen
        """

        intro = True

        # Title
        title = self.font.render("SPSE ADVENTURE", True, BLACK)
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


g = Game()
g.intro_screen()
g.new()

while g.running:
    g.main()
    g.game_over()

pygame.quit()