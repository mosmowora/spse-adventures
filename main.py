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

        self.character_spritesheet = Spritesheet("img/character.png")
        self.terrain_spritesheet = Spritesheet("img/terrain.png")
    
    def create_tile_map(self):
        """
        Creates tile map
        """

        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "_": Blockade(self, j, i)
                elif column == "W": Block(self, j, i, "W")
                elif column == "S": Block(self, j, i, "S")
                elif column == "O": Block(self, j, i, "O")
                elif column == "D": Block(self, j, i, "D")
                elif column == "L": Block(self, j, i, "L")
                elif column == "T": Block(self, j, i, "T")
                elif column == "P": Player(self, j, i)

    def new(self):
        """
        A new game starts
        """

        # Player is alive
        self.playing = True

        # Sprites, blocks, npcs
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.LayeredUpdates()

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

        # After player dies
        self.running = False

    def events(self):
        """
        Events for the game loop
        """

        # Events
        for event in pygame.event.get():

            # Close button
            if event.type == pygame.QUIT: self.playing, self.running = False, False

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

        self.screen.fill(BLACK) # Draws screen
        self.all_sprites.draw(self.screen) # Draws sprites onto the scree
        self.clock.tick(FPS) # How often does the game update
        pygame.display.update()

    def game_over(self):
        pass

    def intro_screen(self):
        pass


g = Game()
g.intro_screen()
g.new()

while g.running:
    g.main()
    g.game_over()

pygame.quit()