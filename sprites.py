# Imports
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
        self.groups = self.game.all_sprites, self.game.player_sprite
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

        self.player_sitting = False

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Down animations
        self.facing_down = [
            self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)
        ]

        # Up animations
        self.facing_up = [
            self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)
        ]

        # Left animations
        self.facing_left = [
            self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)
        ]

        # Right animations
        self.facing_right = [
            self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)
        ]

    def update(self):
        """
        Update for the player
        """

        # Moving
        if not self.player_sitting: self.movement()
        self.animate()

        # Movement
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        # Collision
        if not self.player_sitting: 
            self.collide_blocks("x")
            self.collide_cleaner("x")
            # self.collide_npc("x")
            self.collide_blocks("y")
            self.collide_cleaner("y")
            # self.collide_npc("y")
        
        # Sitting
        if self.player_sitting:
            self.rect.x = self.x_change
            self.rect.y = self.y_change
            self.image = self.game.character_spritesheet.get_sprite(102, 2, self.width, self.height) if self.facing != "right" else self.game.character_spritesheet.get_sprite(102, 34, self.width, self.height)

        # Not sitting
        else: 
            self.x_change = 0
            self.y_change = 0
            
    def get_facing(self):
        """
        Returns the facing of the player
        """

        return self.facing

    def movement(self):
        """
        Movement for the player
        """

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            for sprite in self.game.all_sprites: sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = "left"
        elif keys[pygame.K_d]: 
            for sprite in self.game.all_sprites: sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = "right"
        elif keys[pygame.K_w]: 
            for sprite in self.game.all_sprites: sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = "up"
        elif keys[pygame.K_s]: 
            for sprite in self.game.all_sprites: sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = "down"

    def collide_cleaner(self, direction: str):
        """
        Colliding with cleaner
        """

        # Moving left and right
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.cleaner, False)
            if hits: self.game.shoes_on()
        
        # Moving down and up
        elif direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.cleaner, False)
            if hits: self.game.shoes_on()

    def collide_npc(self, direction: str):
        """
        Colliding with Npcs
        """

        # Moving left and right
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.npcs, False)
            if hits: 

                # Moving right
                if self.x_change > 0: 
                    for sprite in self.game.all_sprites: sprite.rect.x += PLAYER_SPEED
                    self.rect.x = hits[0].rect.left - self.rect.width

                # Moving left
                if self.x_change < 0: 
                    for sprite in self.game.all_sprites: sprite.rect.x -= PLAYER_SPEED
                    self.rect.x = hits[0].rect.right
        
        # Moving down and up
        elif direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.npcs, False)
            if hits:

                # Moving down
                if self.y_change > 0: 
                    for sprite in self.game.all_sprites: sprite.rect.y += PLAYER_SPEED
                    self.rect.y = hits[0].rect.top - self.rect.height

                # Moving up
                if self.y_change < 0: 
                    for sprite in self.game.all_sprites: sprite.rect.y -= PLAYER_SPEED
                    self.rect.y = hits[0].rect.bottom

    def collide_blocks(self, direction: str):
        """
        Colliding with Blocks/objects
        """

        # Moving left and right
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                
                # Moving right
                if self.x_change > 0: 
                    for sprite in self.game.all_sprites: sprite.rect.x += PLAYER_SPEED
                    self.rect.x = hits[0].rect.left - self.rect.width

                # Moving left
                if self.x_change < 0: 
                    for sprite in self.game.all_sprites: sprite.rect.x -= PLAYER_SPEED
                    self.rect.x = hits[0].rect.right
        
        # Moving down and up
        elif direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:

                # Moving down
                if self.y_change > 0:
                    for sprite in self.game.all_sprites: sprite.rect.y += PLAYER_SPEED
                    self.rect.y = hits[0].rect.top - self.rect.height

                # Moving up
                if self.y_change < 0: 
                    for sprite in self.game.all_sprites: sprite.rect.y -= PLAYER_SPEED
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        """
        Animates player movement
        """

        # Down
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = self.facing_down[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3: self.animation_loop = 1

        # Up
        elif self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = self.facing_up[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3: self.animation_loop = 1

        # Left
        elif self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.facing_left[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3: self.animation_loop = 1

        # Right
        elif self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.facing_right[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3: self.animation_loop = 1

    def sit(self, sit: bool, x: int, y: int):
        """
        Player sits on bench
        """

        if sit: 
            self.player_sitting = True
            self.y_change = y
            self.x_change = x
        elif not sit: 
            self.x_change = self.y_change = 0
            if self.facing == "up": self.rect.y = y + TILE_SIZE
            elif self.facing == "down": self.rect.y = y - TILE_SIZE
            elif self.facing == "left": self.rect.x = x + TILE_SIZE
            elif self.facing == "right": self.rect.x = x - TILE_SIZE
            self.player_sitting = False

class Npc(pygame.sprite.Sprite):
    """
    Class for Npcs
    """

    def __init__(self, game, x: int, y: int, type: str):
        """
        Initialization for NPCs
        """

        self.type = type
        self.game = game
        self._layer = NPC_LAYER
        if self.type == "C": self.groups = self.game.all_sprites, self.game.npcs, self.game.interactible, self.game.cleaner
        else: self.groups = self.game.all_sprites, self.game.npcs, self.game.interactible
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = r.choice(["left", "right", "up", "down"])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = r.randint(7, 30)

        colors = [0, 99, 198, 297, 396, 495, 594, 693, 792]
        if self.type == "C": self.color = colors[-1]
        else: self.color = r.choice(colors) 

        self.image = self.game.npcs_spritesheet.get_sprite(self.color, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Down animations
        self.facing_down = [
            self.game.npcs_spritesheet.get_sprite(self.color + 3, 2, self.width, self.height),
            self.game.npcs_spritesheet.get_sprite(self.color + 35, 2, self.width, self.height),
            self.game.npcs_spritesheet.get_sprite(self.color + 67, 2, self.width, self.height)
        ]

        # Up animations
        self.facing_up = [
            self.game.npcs_spritesheet.get_sprite(self.color + 3, 34, self.width, self.height),
            self.game.npcs_spritesheet.get_sprite(self.color + 35, 34, self.width, self.height),
            self.game.npcs_spritesheet.get_sprite(self.color + 67, 34, self.width, self.height)
        ]

        # Left animations
        self.facing_left = [
            self.game.npcs_spritesheet.get_sprite(self.color + 3, 98, self.width, self.height),
            self.game.npcs_spritesheet.get_sprite(self.color + 35, 98, self.width, self.height),
            self.game.npcs_spritesheet.get_sprite(self.color + 67, 98, self.width, self.height)
        ]

        # Right animations
        self.facing_right = [
            self.game.npcs_spritesheet.get_sprite(self.color + 3, 66, self.width, self.height),
            self.game.npcs_spritesheet.get_sprite(self.color + 35, 66, self.width, self.height),
            self.game.npcs_spritesheet.get_sprite(self.color + 67, 66, self.width, self.height)
        ]
        
    def look_at_player(self):
        """
        NPC looks at player\n
        TODO: needs to be placed in correct method, but it works
        """

        if self.game.player.x > self.x: self.facing = "right"
        elif self.game.player.x < self.x: self.facing = "left"
        elif self.game.player.y > self.y: self.facing = "down"
        elif self.game.player.y < self.y: self.facing = "up"

    def update(self):
        """
        Update for the npc
        """

        # Moving
        if self.type == "C": self.movement()
        self.animate()
        
        # Collision
        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.collide_player("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")
        self.collide_player("y")

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        """
        Movement for the npc
        """

        if self.facing == "left":
            self.x_change -= NPC_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel: self.max_travel, self.facing = r.randint(7, 30), r.choice(["left", "right", "up", "down"])

        elif self.facing == "right":
            self.x_change += NPC_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel: self.max_travel, self.facing = r.randint(7, 30), r.choice(["left", "right", "up", "down"])

        elif self.facing == "up":
            self.y_change -= NPC_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel: self.max_travel, self.facing = r.randint(7, 30), r.choice(["left", "right", "up", "down"])

        elif self.facing == "down":
            self.y_change += NPC_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel: self.max_travel, self.facing = r.randint(7, 30), r.choice(["left", "right", "up", "down"])

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

    def collide_player(self, direction: str):
        """
        Colliding with Player
        """

        # Cleaner
        if self.type == "C": 
            hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
            if hits: self.game.shoes_on()

        """else:
    
            # Moving left and right
            if direction == "x":
                hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
                if hits: 
                        
                    # Moving right
                    if self.x_change > 0: self.rect.x = hits[0].rect.left - self.rect.width

                    # Moving left
                    if self.x_change < 0: self.rect.x = hits[0].rect.right
                
            # Moving down and up
            elif direction == "y":
                hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
                if hits:
                    
                    # Moving down
                    if self.y_change > 0: self.rect.y = hits[0].rect.top - self.rect.height

                    # Moving up
                    if self.y_change < 0: self.rect.y = hits[0].rect.bottom"""

    def animate(self):
        """
        Animates npc movement
        """

        # Down
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.npcs_spritesheet.get_sprite(self.color + 3, 2, self.width, self.height)
            else:
                self.image = self.facing_down[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3: self.animation_loop = 1

        # Up
        elif self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.npcs_spritesheet.get_sprite(self.color + 3, 34, self.width, self.height)
            else:
                self.image = self.facing_up[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3: self.animation_loop = 1

        # Left
        elif self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.npcs_spritesheet.get_sprite(self.color + 3, 98, self.width, self.height)
            else:
                self.image = self.facing_left[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3: self.animation_loop = 1

        # Right
        elif self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.npcs_spritesheet.get_sprite(self.color + 3, 66, self.width, self.height)
            else:
                self.image = self.facing_right[math.floor(self.animation_loop)]
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

        # Interactible blocks
        inter = ["L", "Ľ", "ľ", "D", "G", "B", "t", "T", "Ť", "S", "Z", "s", "z", "b", "d", "O", "o", "ó", "Ó", "ĺ", "y", "Y", "g", "w"]

        self.game = game
        self._layer = BLOCK_LAYER
        if type in inter: self.groups = self.game.all_sprites, self.game.blocks, self.game.interactible
        else: self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        if type == "W": self.image = self.game.terrain_spritesheet.get_sprite(2, 36, self.width, self.height)
        elif type == "L": self.image = self.game.terrain_spritesheet.get_sprite(36, 36, self.width, self.height)
        elif type == "Ľ": self.image = self.game.terrain_spritesheet.get_sprite(70, 104, self.width, self.height)
        elif type == "ľ": self.image = self.game.terrain_spritesheet.get_sprite(104, 104, self.width, self.height)
        elif type == "S": self.image = self.game.terrain_spritesheet.get_sprite(70, 2, self.width, self.height)
        elif type == "Z": self.image = self.game.terrain_spritesheet.get_sprite(138, 104, self.width, self.height)
        elif type == "s": self.image = self.game.terrain_spritesheet.get_sprite(104, 2, self.width, self.height)
        elif type == "z": self.image = self.game.terrain_spritesheet.get_sprite(138, 70, self.width, self.height)
        elif type == "w": self.image = self.game.terrain_spritesheet.get_sprite(70, 36, self.width, self.height)
        elif type == "D": self.image = self.game.terrain_spritesheet.get_sprite(104, 36, self.width, self.height)
        elif type == "G": self.image = self.game.terrain_spritesheet.get_sprite(172, 104, self.width, self.height)
        elif type == "B": self.image = self.game.terrain_spritesheet.get_sprite(2, 70, self.width, self.height)
        elif type == "t": self.image = self.game.terrain_spritesheet.get_sprite(36, 70, self.width, self.height)
        elif type == "T": self.image = self.game.terrain_spritesheet.get_sprite(2, 104, self.width, self.height)
        elif type == "Ť": self.image = self.game.terrain_spritesheet.get_sprite(36, 104, self.width, self.height)
        elif type == "R": self.image = self.game.terrain_spritesheet.get_sprite(172, 36, self.width, self.height)
        elif type == "Ŕ": self.image = self.game.terrain_spritesheet.get_sprite(206, 36, self.width, self.height)
        elif type == "ŕ": self.image = self.game.terrain_spritesheet.get_sprite(206, 70, self.width, self.height)
        elif type == "r": self.image = self.game.terrain_spritesheet.get_sprite(172, 2, self.width, self.height)
        elif type == "l": self.image = self.game.terrain_spritesheet.get_sprite(240, 104, self.width, self.height)
        elif type == "ĺ": self.image = self.game.terrain_spritesheet.get_sprite(240, 104, self.width, self.height)
        elif type == "Ř": self.image = self.game.terrain_spritesheet.get_sprite(138, 36, self.width, self.height)
        elif type == "ř": self.image = self.game.terrain_spritesheet.get_sprite(70, 70, self.width, self.height)
        elif type == "b": self.image = self.game.terrain_spritesheet.get_sprite(138, 70, self.width, self.height)
        elif type == "d": self.image = self.game.terrain_spritesheet.get_sprite(104, 70, self.width, self.height)
        elif type == "!": self.image = self.game.terrain_spritesheet.get_sprite(138, 2, self.width, self.height)
        elif type == "J": self.image = self.game.terrain_spritesheet.get_sprite(2, 138, self.width, self.height)
        elif type == "U": self.image = self.game.terrain_spritesheet.get_sprite(36, 138, self.width, self.height)
        elif type == "j": self.image = self.game.terrain_spritesheet.get_sprite(206, 104, self.width, self.height)
        elif type == "/": self.image = self.game.terrain_spritesheet.get_sprite(241, 70, self.width, self.height)
        elif type == "|": self.image = self.game.terrain_spritesheet.get_sprite(241, 36, self.width, self.height)
        elif type == "O": self.image = self.game.terrain_spritesheet.get_sprite(138, 138, self.width, self.height)
        elif type == "o": self.image = self.game.terrain_spritesheet.get_sprite(172, 138, self.width, self.height)
        elif type == "ó": self.image = self.game.terrain_spritesheet.get_sprite(70, 138, self.width, self.height)
        elif type == "Ó": self.image = self.game.terrain_spritesheet.get_sprite(104, 138, self.width, self.height)
        elif type == "y": self.image = self.game.terrain_spritesheet.get_sprite(240, 2, self.width, self.height)
        elif type == "Y": self.image = self.game.terrain_spritesheet.get_sprite(274, 2, self.width, self.height)
        elif type == "g": self.image = self.game.terrain_spritesheet.get_sprite(206, 138, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Blockade(pygame.sprite.Sprite):
    """
    Main class for adding black block to the screen
    """
    
    def __init__(self, game, x: int, y: int, type: str):
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

        if type == "_": self.image = self.game.terrain_spritesheet.get_sprite(206, 2, self.width, self.height)
        elif type == "?": self.image = self.game.terrain_spritesheet.get_sprite(36, 2, self.width, self.height)

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

class Interact(pygame.sprite.Sprite):
    """
    Class for intracting
    """

    def __init__(self, game, x: int, y: int, inter: dict):
        """
        Initialization
        """

        # Dictionary
        self.interactive = inter

        # Game
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.interacts
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Coordinates and size
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = pygame.image.load("img/interact.png")

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.interacting()

        self.kill()

    def interacting(self):
        """
        Interacting with objects
        """

        hits = pygame.sprite.spritecollide(self, self.game.interactible, False)

        if hits:
            for i, row in enumerate(self.game.in_room):
                for j, _ in enumerate(row):

                    # Trashcan
                    if self.interactive[hits[0]] == "t" + str(i) + str(j): self.game.interacted = ["Trashcan", i ,j]; print(j, i)

                    # Toilet
                    if self.interactive[hits[0]] in ("T" + str(i) + str(j), "Ť" + str(i) + str(j)): self.game.interacted = ["Toilet", i ,j]

                    # Door
                    elif self.interactive[hits[0]] in ("D" + str(i) + str(j), "G" + str(i) + str(j)): self.game.interacted = ["Door", i, j, hits[0].rect.left, hits[0].rect.top]

                    # Locker
                    elif self.interactive[hits[0]] in ("L" + str(i) + str(j), "Ľ" + str(i) + str(j), "ľ" + str(i) + str(j)): self.game.interacted = ["Locker", i, j]

                    # Bench
                    elif self.interactive[hits[0]] == "B" + str(i) + str(j): self.game.interacted = ["Bench", hits[0].rect.left, hits[0].rect.top]

                    # Stairs
                    elif self.interactive[hits[0]] in ("S" + str(i) + str(j), "Z" + str(i) + str(j)): self.game.interacted = ["Stairs_up", i, j]; print(j, i)
                    elif self.interactive[hits[0]] in ("s" + str(i) + str(j), "z" + str(i) + str(j)): self.game.interacted = ["Stairs_down", i, j]; print(j, i)

                    # Basement
                    elif self.interactive[hits[0]] in ("b" + str(i) + str(j), "d" + str(i) + str(j)): self.game.interacted = ["Basement", i, j]; print(j, i)

                    # Special desk
                    elif self.interactive[hits[0]] == "ĺ" + str(i) + str(j): self.game.interacted = ["Desk", i ,j]; print(j, i)
                    
                    # Bench press
                    elif self.interactive[hits[0]] in ("y" + str(i) + str(j), "Y" + str(i) + str(j)): self.game.interacted = ["Bench_press", i ,j]
                    
                    # Teacher
                    elif self.interactive[hits[0]] == "N" + str(i) + str(j): self.game.interacted = ["Teacher", i, j]

                    # Bookshelf
                    elif self.interactive[hits[0]] in ("O" + str(i) + str(j), "o" + str(i) + str(j), "ó" + str(i) + str(j), "Ó" + str(i) + str(j)): self.game.interacted = ["Bookshelf", i, j]

                    # Computer
                    elif self.interactive[hits[0]] == "g" + str(i) + str(j): self.game.interacted = ["Computer", i, j]; print(j, i)

                    # Special window
                    elif self.interactive[hits[0]] == "w" + str(i) + str(j): self.game.interacted = ["Window", i, j]; print(j, i)

class Button:
    """
    Class for button
    """

    def __init__(self, x: int, y: int, width: int, height: int, /,  fg: tuple, bg: tuple, content: str, fontsize: int):
        """
        Initialization
        """

        # Font
        self.font = pygame.font.Font("Roboto.ttf", fontsize)
        self.content = content

        # Coordinates and size
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # self.colors
        self.fg = fg
        self.bg = bg

        # Bg txt
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        # Hitbox
        self.rect.x = self.x
        self.rect.y = self.y

        # Text
        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2)) 
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos: tuple[int, int], pressed: tuple[bool, bool, bool]):
        """ 
        Pressing button 
        """ 
        
        return True if self.rect.collidepoint(pos) and pressed[0] else False
