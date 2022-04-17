import pygame, math, random as r
from config import *

class Spritesheet:
    """
    Class for images
    """

    def __init__(self, file: str):
        """
        Initialization
        """

        # Loads sheet
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x: int, y: int, width: int, height: int):
        """
        Returns image from sheet
        """
        
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    """
    Class for player
    """

    def __init__(self, game, x: int, y: int):
        """
        Initialization
        """

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = "down"
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        """
        Update for the player
        """

        # Moving
        self.movement()
        self.animate()

        # Collision
        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")
        
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        """
        Movement for the player
        """

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: 
            self.x_change -= PLAYER_SPEED
            self.facing = "left"
        elif keys[pygame.K_d]: 
            self.x_change += PLAYER_SPEED
            self.facing = "right"
        elif keys[pygame.K_w]: 
            self.y_change -= PLAYER_SPEED
            self.facing = "up"
        elif keys[pygame.K_s]: 
            self.y_change += PLAYER_SPEED
            self.facing = "down"

    def collide_blocks(self, direction: str):
        """
        Colliding with Blocks/objects
        """

        # Moving left and right
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                
                # Moving right
                if self.x_change > 0: self.rect.x = hits[0].rect.left - self.rect.width

                # Moving left
                if self.x_change < 0: self.rect.x = hits[0].rect.right
        
        # Moving down and up
        elif direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                
                # Moving down
                if self.y_change > 0: self.rect.y = hits[0].rect.top - self.rect.height

                # Moving up
                if self.y_change < 0: self.rect.y = hits[0].rect.bottom

    def animate(self):
        """
        Animates player movement
        """

        # Down animations
        facing_down = [
            self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)
        ]

        # Up animations
        facing_up = [
            self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)
        ]

        # Left animations
        facing_left = [
            self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)
        ]

        # Right animations
        facing_right = [
            self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)
        ]

        # Down
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = facing_down[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3: self.animation_loop = 1

        # Up
        elif self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = facing_up[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3: self.animation_loop = 1

        # Left
        elif self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = facing_left[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3: self.animation_loop = 1

        # Right
        elif self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = facing_right[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3: self.animation_loop = 1

class Block(pygame.sprite.Sprite):
    """
    Class for Block
    """

    def __init__(self, game, x: int, y: int, type: str):
        """
        Initialization
        """

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        if type == "W": self.image = self.game.terrain_spritesheet.get_sprite(2, 36, self.width, self.height)
        elif type == "S": self.image = self.game.terrain_spritesheet.get_sprite(36, 36, self.width, self.height)
        elif type == "O": self.image = self.game.terrain_spritesheet.get_sprite(70, 36, self.width, self.height)
        elif type == "D": self.image = self.game.terrain_spritesheet.get_sprite(104, 36, self.width, self.height)
        elif type == "L": self.image = self.game.terrain_spritesheet.get_sprite(2, 70, self.width, self.height)
        elif type == "T": self.image = self.game.terrain_spritesheet.get_sprite(36, 70, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Blockade(pygame.sprite.Sprite):
    """
    Main class for adding black block to the screen
    """
    
    def __init__(self, game, x: int, y: int):
        """
        Initialization
        """
        
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.image = self.game.terrain_spritesheet.get_sprite(36, 2, self.width, self.height) # I can't do the coordinates

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    """
    Class for ground
    """

    def __init__(self, game, x: int, y: int):
        """
        Initialization
        """

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.image = self.game.terrain_spritesheet.get_sprite(2, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y