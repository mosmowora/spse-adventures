# Import
import pygame, sys
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
        self.screen = pygame.display.set_mode((win_width, win_height))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_spritesheet = Spritesheet("img/character.png")
        self.terrain_spritesheet = Spritesheet("img/terrain.png")
    
    def createTilemap(self):
        """
        Creates tile map
        """

        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "W": Wall(self, j, i)
                elif column == "P": Player(self, j, i)

    def new(self):
        """
        A new game starts
        """

        # Player is alive
        self.playing = True

        # Sprites, blocks, npcs
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.LayeredUpdates()

        # Tilemap
        self.createTilemap()


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

        self.screen.fill(black) # Draws screen
        self.all_sprites.draw(self.screen) # Draws sprites onto the scree
        self.clock.tick(fps) # How often does the game update
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
sys.exit()