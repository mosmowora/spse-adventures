import pygame, math, random as r
from config import *

class Spritesheet:
    """
    Class for images
    """

    def __init__(self, file):
        """
        Initialization
        """

        # Loads sheet
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        """
        Returns image from sheet
        """
        
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(black)
        return sprite

class Player(pygame.sprite.Sprite):
    """
    Class for player
    """

    def __init__(self, game, x, y):
        """
        Initialization
        """

        self.game = game
        self._layer = player_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.x_change = 0
        self.y_change = 0

        self.facing = "down"

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        """
        Update for the player
        """

        self.movement()
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        """
        Movement for the player
        """

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: 
            self.x_change -= player_speed
            self.facing = "left"
        elif keys[pygame.K_d]: 
            self.x_change += player_speed
            self.facing = "right"
        elif keys[pygame.K_w]: 
            self.y_change -= player_speed
            self.facing = "up"
        elif keys[pygame.K_s]: 
            self.y_change += player_speed
            self.facing = "down"

class Wall(pygame.sprite.Sprite):
    """
    Class for wall
    """

    def __init__(self, game, x, y):
        """
        Initialization
        """

        self.game = game
        self._layer = wall_layer
        self.groups = self.game.all_sprites, self.game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.x_change = 0
        self.y_change = 0

        self.image = self.game.terrain_spritesheet.get_sprite(2, 36, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    """
    Class for ground
    """

    def __init__(self, game, x, y):
        """
        Initialization
        """

        self.game = game
        self._layer = ground_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.x_change = 0
        self.y_change = 0

        self.image = self.game.terrain_spritesheet.get_sprite(3, 3, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y