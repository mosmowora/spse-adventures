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

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height) if not self.game.lyz_created else self.game.character_spritesheet.get_sprite(141, 0, self.width, self.height)

        self.player_sitting = False

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Down animations
        self.facing_down = [
            self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)
        ] if not self.game.lyz_created else [
            self.game.character_spritesheet.get_sprite(141, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(141 + 33, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(141 + 66, 0, self.width, self.height)
        ]

        # Up animations
        self.facing_up = [
            self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)
        ] if not self.game.lyz_created else [
            self.game.character_spritesheet.get_sprite(141, 35, self.width, self.height),
            self.game.character_spritesheet.get_sprite(141 + 33, 35, self.width, self.height),
            self.game.character_spritesheet.get_sprite(141 + 66, 35, self.width, self.height)
        ]

        # Left animations
        self.facing_left = [
            self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)
        ] if not self.game.lyz_created else [
            self.game.character_spritesheet.get_sprite(141, 99, self.width, self.height),
            self.game.character_spritesheet.get_sprite(141 + 32, 99, self.width, self.height),
            self.game.character_spritesheet.get_sprite(141 + 65, 99, self.width, self.height)
        ]

        # Right animations
        self.facing_right = [
            self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)
        ] if not self.game.lyz_created else [
            self.game.character_spritesheet.get_sprite(141, 66, self.width, self.height),
            self.game.character_spritesheet.get_sprite(141 + 32, 66, self.width, self.height),
            self.game.character_spritesheet.get_sprite(141 + 65, 66, self.width, self.height)
        ]

        # Lost guy
        self.go_left = 0
        self.go_down = 0

    def update(self):
        """
        Update for the player
        """

        # Moving
        if self.game.player_follow:
            if self.go_left < 470:
                self.facing = "left"
                self.movement()
            elif self.go_down < 40:
                self.facing = "down"
                self.movement()
            else: 
                self.facing = "left"
                self.game.found_guy()
        elif not self.player_sitting: self.movement()
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
            if self.facing in ("right", "left"): self.image = self.game.character_spritesheet.get_sprite(102, 34, self.width, self.height) if self.facing == "right" else self.game.character_spritesheet.get_sprite(102, 2, self.width, self.height)
            else: self.image = self.game.character_spritesheet.get_sprite(102, 66, self.width, self.height) if self.facing == "up" else self.game.character_spritesheet.get_sprite(102, 98, self.width, self.height)

        # Not sitting
        else: 
            self.x_change = 0
            self.y_change = 0

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
        elif self.game.player_follow: 
            if self.facing == "left":
                for sprite in self.game.all_sprites: sprite.rect.x += int(PLAYER_SPEED / 1.4)
                self.x_change -= int(PLAYER_SPEED / 1.4)
                self.go_left += 1
            else:
                for sprite in self.game.all_sprites: sprite.rect.y -= int(PLAYER_SPEED / 1.4)
                self.y_change += int(PLAYER_SPEED / 1.4)
                self.go_down += 1

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
                self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height) if not self.game.lyz_created else self.game.character_spritesheet.get_sprite(141, 0, self.width, self.height)
            else:
                self.image = self.facing_down[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3: self.animation_loop = 1

        # Up
        elif self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height) if not self.game.lyz_created else self.game.character_spritesheet.get_sprite(141, 35, self.width, self.height)
            else:
                self.image = self.facing_up[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3: self.animation_loop = 1

        # Left
        elif self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height) if not self.game.lyz_created else self.game.character_spritesheet.get_sprite(141, 99, self.width, self.height)
            else:
                self.image = self.facing_left[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3: self.animation_loop = 1

        # Right
        elif self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height) if not self.game.lyz_created else self.game.character_spritesheet.get_sprite(141, 66, self.width, self.height)
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
        if self.type in ("C", "K", "9"): self.groups = self.game.all_sprites, self.game.npcs, self.game.cleaner
        elif self.type == "p": self.groups = self.game.all_sprites, self.game.npcs
        else: self.groups = self.game.all_sprites, self.game.npcs, self.game.interactible
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = r.choice(["left", "right", "up", "down"])
        if self.type == "§": self.facing = "down"
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = r.randint(7, 15)

        colors = [
            0, # Purple 0
            99, # Green 1
            198, # Red 2
            297, # Yellow 3
            396, # Orange 4
            495, # Blue 5 
            594, # Pink 6 
            693, # Black 7
            792, # Brown 8
            891 # White (For cleaners) 9 (-1)
        ]

        # Cleaner - White
        if self.type == "C": self.color = colors[-1]

        # Vujcheek - Blue
        elif self.type == "9": self.color = colors[5]

        # G.G - Purple
        elif self.type == "§": self.color = colors[0]

        # Kvôňtura - Green
        elif x == 21 and y == 3: self.color = colors[1]

        # Koky - Brown
        elif x == 111 and y == 9: self.color = colors[8]

        # Guydosova - Purple
        elif x == 94 and y == 24: self.color = colors[0]
        
        # Martin Shreky - Black
        elif x == 180 and y == 5: self.color = colors[5]

        # Liascinska - Green
        elif x == 100 and y == 19: self.color = colors[1]

        # Mohyla - Pink
        elif x == 190 and y == 19: self.color = colors[6]

        # (Ne)Pusti - Red
        elif x == 188 and y == 13: self.color = colors[2]
        
        # NiguSova - Black
        elif x == 77 and y == 16: self.color = colors[7]
        
        # Bartin Moda - Black
        elif x == 25 and y == 36: self.color = colors[7]

        # HaramBozo - Orange
        elif x == 8 and y == 28: self.color = colors[4]

        # Rolada - Green
        elif x == 42 and y == 18: self.color = colors[1] 

        # Gone-valova - Yellow
        elif x == 155 and y == 37: self.color = colors[3]

        # Gulbaka - Blue
        elif x == 57 and y == 22: self.color = colors[5]
        
        # Metrova - Orange
        elif x == 130 and y == 26: self.color = colors[4]
        
        # Zo Sarisa - Black
        elif x == 139 and y == 7: self.color = colors[7]

        # Random shirt color cause just random side character
        else: self.color = r.choice(colors[:-1]) 

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

        # Lost guy
        self.go_left = 0
        self.go_down = 0

    def update(self):
        """
        Update for the npc
        """

        # Moving
        if self.type in ("C", "9", "p"): self.movement()
        elif self.type == "§" and self.game.g_move: self.y_change += 1.95 * TILE_SIZE; self.movement()
        elif self.type == "§" and self.game.g_leave:
            if self.go_left < 470: 
                self.facing = "left"
                self.movement()
            elif self.go_down < 40:
                self.facing = "down"
                self.movement()
                self.facing = r.choice(["left", "right", "up"])
            else: self.facing = "left"
        self.animate()
        
        # Collision
        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.collide_player()
        self.rect.y += self.y_change
        self.collide_blocks("y")
        self.collide_player()

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        """
        Movement for the npc
        """

        if self.facing == "left":
            if self.game.g_leave: self.go_left += 1
            self.x_change -= NPC_SPEED
            self.movement_loop -= 1
            if self.type == "9": self.move_towards_player()
            elif self.movement_loop <= -self.max_travel: self.max_travel, self.facing = r.randint(7, 15), r.choice(["left", "right", "up", "down"])

        elif self.facing == "right":
            self.x_change += NPC_SPEED
            self.movement_loop += 1
            if self.type == "9": self.move_towards_player()
            elif self.movement_loop >= self.max_travel: self.max_travel, self.facing = r.randint(7, 15), r.choice(["left", "right", "up", "down"])

        elif self.facing == "up":
            self.y_change -= NPC_SPEED
            self.movement_loop -= 1
            if self.type == "9": self.move_towards_player()
            elif self.movement_loop <= -self.max_travel: self.max_travel, self.facing = r.randint(7, 15), r.choice(["left", "right", "up", "down"])

        elif self.facing == "down":
            if self.game.g_leave: self.go_down += 1
            self.y_change += NPC_SPEED
            self.movement_loop += 1
            if self.type == "9": self.move_towards_player()
            elif self.movement_loop >= self.max_travel: self.max_travel, self.facing = r.randint(7, 15), r.choice(["left", "right", "up", "down"])
            
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

    def move_towards_player(self):
        """
        For Vujcheek to move closer to the player
        """
        
        dirvect = pygame.math.Vector2(self.game.player.rect.x - self.rect.x,
                                      self.game.player.rect.y - self.rect.y)
                                      
        # if player is in the hall and has more than 9 quests done then Vujcheek is goona go after him
        if dirvect.length() > 0 and self.game.saved_room_data == "Hall" and len(self.game.grades) > 9:
            dirvect.normalize(); dirvect.scale_to_length(VUJ_SPEED)
            if round(dirvect[1]) < 0: self.facing = "up"
            elif round(dirvect[1]) > 0: self.facing = "down"
            elif round(dirvect[0]) > 0: self.facing = "right"
            elif round(dirvect[0]) < 0: self.facing = "left"
            self.rect.move_ip(dirvect)

        # Or he's just gonna behave like any other npc
        else: 
            if self.facing == "left":
                self.x_change -= VUJ_SPEED / 2
                if self.movement_loop <= -self.max_travel: self.max_travel, self.facing = r.randint(7, 30), r.choice(["left", "right", "up", "down"])

            elif self.facing == "right":
                self.x_change += VUJ_SPEED / 2
                if self.movement_loop >= self.max_travel: self.max_travel, self.facing = r.randint(7, 30), r.choice(["left", "right", "up", "down"])

            elif self.facing == "up":
                self.y_change -= VUJ_SPEED / 2
                if self.movement_loop <= -self.max_travel: self.max_travel, self.facing = r.randint(7, 30), r.choice(["left", "right", "up", "down"])

            elif self.facing == "down":
                self.y_change += VUJ_SPEED / 2
                if self.movement_loop >= self.max_travel: self.max_travel, self.facing = r.randint(7, 30), r.choice(["left", "right", "up", "down"])

    def collide_player(self):
        """
        Colliding with Player
        """

        # Cleaner
        if self.type == "C": 
            hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
            if hits: self.game.shoes_on()

        # Kacka
        elif self.type == "K":
            hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
            if hits and self.game.locker_stuff['crocs']: 
                pygame.mixer.Sound.play(self.game.kacurovanie, 0, 6000, 1000)
                if self.game.player.facing == "up": self.game.player.rect.y += 1 * TILE_SIZE
                elif self.game.player.facing == "down": self.game.player.rect.y -= 1 * TILE_SIZE
                elif self.game.player.facing == "right": self.game.player.rect.x -= 1 * TILE_SIZE
                elif self.game.player.facing == "left": self.game.player.rect.x += 1 * TILE_SIZE
                self.game.talking("WHY you not wearin' yo boots?", True)
                self.game.talking("You'll get in a lot of trouble for this", True)
                self.game.talking("Who's yo' classteacher?", True)

        # Vujcheek
        elif self.type == "9" and "vujcheek fender" not in self.game.inv.keys():
            hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)
            if hits and len(self.game.grades) > 9: self.game.game_over("img/game_over_background.png")
            

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
        inter = ["L", "Ľ", "ľ", "D", "G", "B", "h", "t", "T", "Ť", "S", "Z", "s", "z", "b", "d", "O", "o", "ó", "Ó", "é", "y", "Y", "g", "w", "E", "ý", "ž", "č", "ú", "ň", "@", "#", "*", "A", "3", "4", "5", "6", "7", "8", "ä", "ď", "▬", "∟", "↔"]

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
        elif type == "h": self.image = self.game.terrain_spritesheet.get_sprite(274, 70, self.width, self.height)
        elif type == "t": self.image = self.game.terrain_spritesheet.get_sprite(36, 70, self.width, self.height)
        elif type == "T": self.image = self.game.terrain_spritesheet.get_sprite(2, 104, self.width, self.height)
        elif type == "Ť": self.image = self.game.terrain_spritesheet.get_sprite(36, 104, self.width, self.height)
        elif type == "R": self.image = self.game.terrain_spritesheet.get_sprite(172, 36, self.width, self.height)
        elif type == "Ŕ": self.image = self.game.terrain_spritesheet.get_sprite(206, 36, self.width, self.height)
        elif type == "ŕ": self.image = self.game.terrain_spritesheet.get_sprite(206, 70, self.width, self.height)
        elif type == "r": self.image = self.game.terrain_spritesheet.get_sprite(172, 2, self.width, self.height)
        elif type == "l": self.image = self.game.terrain_spritesheet.get_sprite(241, 104, self.width, self.height)
        elif type == "k": self.image = self.game.terrain_spritesheet.get_sprite(241, 138, self.width, self.height)
        elif type == "é": self.image = self.game.terrain_spritesheet.get_sprite(274, 172, self.width, self.height)
        elif type == "u": self.image = self.game.terrain_spritesheet.get_sprite(241, 172, self.width, self.height)
        elif type == "ä": self.image = self.game.terrain_spritesheet.get_sprite(241, 240, self.width, self.height)
        elif type == "e": self.image = self.game.terrain_spritesheet.get_sprite(274, 172, self.width, self.height)
        elif type == "Ř": self.image = self.game.terrain_spritesheet.get_sprite(138, 36, self.width, self.height)
        elif type == "ř": self.image = self.game.terrain_spritesheet.get_sprite(70, 70, self.width, self.height)
        elif type == "b": self.image = self.game.terrain_spritesheet.get_sprite(138, 70, self.width, self.height)
        elif type == "d": self.image = self.game.terrain_spritesheet.get_sprite(104, 70, self.width, self.height)
        elif type == "!": self.image = self.game.terrain_spritesheet.get_sprite(138, 2, self.width, self.height)
        elif type == "J": self.image = self.game.terrain_spritesheet.get_sprite(2, 138, self.width, self.height)
        elif type == "U": self.image = self.game.terrain_spritesheet.get_sprite(36, 138, self.width, self.height)
        elif type == "j": self.image = self.game.terrain_spritesheet.get_sprite(206, 104, self.width, self.height)
        elif type == "m": self.image = self.game.terrain_spritesheet.get_sprite(274, 104, self.width, self.height)
        elif type == "i": self.image = self.game.terrain_spritesheet.get_sprite(274, 138, self.width, self.height)
        elif type == "n": self.image = self.game.terrain_spritesheet.get_sprite(274, 36, self.width, self.height)
        elif type == "/": self.image = self.game.terrain_spritesheet.get_sprite(241, 70, self.width, self.height)
        elif type == "|": self.image = self.game.terrain_spritesheet.get_sprite(241, 36, self.width, self.height)
        elif type == "O": self.image = self.game.terrain_spritesheet.get_sprite(138, 138, self.width, self.height)
        elif type == "o": self.image = self.game.terrain_spritesheet.get_sprite(172, 138, self.width, self.height)
        elif type == "ó": self.image = self.game.terrain_spritesheet.get_sprite(70, 138, self.width, self.height)
        elif type == "Ó": self.image = self.game.terrain_spritesheet.get_sprite(104, 138, self.width, self.height)
        elif type == "y": self.image = self.game.terrain_spritesheet.get_sprite(241, 2, self.width, self.height)
        elif type == "Y": self.image = self.game.terrain_spritesheet.get_sprite(274, 2, self.width, self.height)
        elif type == "g": self.image = self.game.terrain_spritesheet.get_sprite(206, 138, self.width, self.height)
        elif type == "]": self.image = self.game.terrain_spritesheet.get_sprite(172, 172, self.width, self.height)
        elif type == "[": self.image = self.game.terrain_spritesheet.get_sprite(104, 172, self.width, self.height)
        elif type == "-": self.image = self.game.terrain_spritesheet.get_sprite(138, 172, self.width, self.height)
        elif type == "=": self.image = self.game.terrain_spritesheet.get_sprite(206, 172, self.width, self.height)
        elif type == "}": self.image = self.game.terrain_spritesheet.get_sprite(2, 172, self.width, self.height)
        elif type == "{": self.image = self.game.terrain_spritesheet.get_sprite(70, 172, self.width, self.height)
        elif type == "^": self.image = self.game.terrain_spritesheet.get_sprite(36, 172, self.width, self.height)
        elif type == "V": self.image = self.game.terrain_spritesheet.get_sprite(2, 206, self.width, self.height)
        elif type == "x": self.image = self.game.terrain_spritesheet.get_sprite(36, 206, self.width, self.height)
        elif type == "X": self.image = self.game.terrain_spritesheet.get_sprite(70, 206, self.width, self.height)
        elif type == "E": self.image = self.game.terrain_spritesheet.get_sprite(104, 206, self.width, self.height)
        elif type == "ž": self.image = self.game.terrain_spritesheet.get_sprite(138, 206, self.width, self.height)
        elif type == "ý": self.image = self.game.terrain_spritesheet.get_sprite(172, 206, self.width, self.height)
        elif type == "ň": self.image = self.game.terrain_spritesheet.get_sprite(206, 206, self.width, self.height)
        elif type == "ú": self.image = self.game.terrain_spritesheet.get_sprite(241, 206, self.width, self.height)
        elif type == "č": self.image = self.game.terrain_spritesheet.get_sprite(274, 205, self.width, self.height)
        elif type == "$": self.image = self.game.terrain_spritesheet.get_sprite(307, 172, self.width, self.height)
        elif type == "Q": self.image = self.game.terrain_spritesheet.get_sprite(307, 104, self.width, self.height)
        elif type == "q": self.image = self.game.terrain_spritesheet.get_sprite(307, 138, self.width, self.height)
        elif type == "a": self.image = self.game.terrain_spritesheet.get_sprite(307, 70, self.width, self.height)
        elif type == "@": self.image = self.game.terrain_spritesheet.get_sprite(342, 172, self.width, self.height)
        elif type == "#": self.image = self.game.terrain_spritesheet.get_sprite(342, 206, self.width, self.height)
        elif type == "*": self.image = self.game.terrain_spritesheet.get_sprite(307, 206, self.width, self.height)
        elif type == "~": self.image = self.game.terrain_spritesheet.get_sprite(342, 138, self.width, self.height)
        elif type == "&": self.image = self.game.terrain_spritesheet.get_sprite(310, 2, self.width, self.height)
        elif type == "0": self.image = self.game.terrain_spritesheet.get_sprite(307, 36, self.width, self.height)
        elif type == "ô": self.image = self.game.terrain_spritesheet.get_sprite(342, 36, self.width, self.height)
        elif type == "Ž": self.image = self.game.terrain_spritesheet.get_sprite(342, 70, self.width, self.height)
        elif type == "ˇ": self.image = self.game.terrain_spritesheet.get_sprite(342, 104, self.width, self.height)
        elif type == "A": self.image = self.game.terrain_spritesheet.get_sprite(342, 2, self.width, self.height)
        elif type == "3": self.image = self.game.terrain_spritesheet.get_sprite(376, 2, self.width, self.height)
        elif type == "4": self.image = self.game.terrain_spritesheet.get_sprite(409, 2, self.width, self.height)
        elif type == "5": self.image = self.game.terrain_spritesheet.get_sprite(376, 36, self.width, self.height)
        elif type == "6": self.image = self.game.terrain_spritesheet.get_sprite(409, 36, self.width, self.height)
        elif type == "7": self.image = self.game.terrain_spritesheet.get_sprite(376, 70, self.width, self.height)
        elif type == "8": self.image = self.game.terrain_spritesheet.get_sprite(409, 70, self.width, self.height)
        elif type == "ď": self.image = self.game.terrain_spritesheet.get_sprite(2, 240, self.width, self.height)
        elif type == "Ú": self.image = self.game.terrain_spritesheet.get_sprite(409, 104, self.width, self.height)
        elif type == "Ů": self.image = self.game.terrain_spritesheet.get_sprite(376, 104, self.width, self.height)
        elif type == "▼": self.image = self.game.terrain_spritesheet.get_sprite(409, 138, self.width, self.height)
        elif type == "ś": self.image = self.game.terrain_spritesheet.get_sprite(500, 2, self.width, self.height)
        elif type == "š": self.image = self.game.terrain_spritesheet.get_sprite(500, 36, self.width, self.height)
        elif type == "▬": self.image = self.game.terrain_spritesheet.get_sprite(568, 2, self.width, self.height)
        elif type == "∟": self.image = self.game.terrain_spritesheet.get_sprite(500, 70, self.width, self.height)
        elif type == "↔": self.image = self.game.terrain_spritesheet.get_sprite(534, 70, self.width, self.height)
        

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

    def __init__(self, game, x: int, y: int, /, dirt: bool = False, snow: bool = False, carpet: bool = False):
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

        if not self.game.lyz_created:
            self.image = self.game.terrain_spritesheet.get_sprite(2, 2, self.width, self.height) 
        elif self.game.lyz_created:
            if not dirt:
                if snow: self.image =  self.game.terrain_spritesheet.get_sprite(534, 2, self.width, self.height)
                elif carpet: self.image = self.game.terrain_spritesheet.get_sprite(568, 36, self.width, self.height)
                else: self.image = self.game.terrain_spritesheet.get_sprite(2, 2, self.width, self.height)
            elif dirt: self.image   =  self.game.terrain_spritesheet.get_sprite(534, 36, self.width, self.height)
             
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Banana(pygame.sprite.Sprite):
    """
    Class for Bananky
    """

    def __init__(self, game, x: int, y: int):
        """
        Initialization
        """

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.bananky
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = pygame.image.load("img/bananok_small.png")
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.floors = ["ground floor", "first floor", "second floor", "third floor", "fourth floor", "ending hallway", "basement"]

    def update(self):
        """
        Update for bananok
        """

        self.collect_bananok()

    def collect_bananok(self):
        """
        When player takes bananok
        """

        hits = pygame.sprite.spritecollide(self, self.game.player_sprite, False)

        if hits:
            self.kill() 
            if "bananok" in self.game.inv.keys(): self.game.number_bananok += 1
            else: self.game.inv["bananok"] = "img/bananok.png"; self.game.number_bananok += 1
            self.game.bananky_on_ground[self.floors[self.game.rooms.index(self.game.in_room)]][str(int(self.x / TILE_SIZE)) + str(int(self.y / TILE_SIZE))] = False


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
                    if self.interactive[hits[0]] == "t" + str(i) + str(j): self.game.interacted = ["Trashcan", i ,j]

                    # Toilet
                    if self.interactive[hits[0]] in ("T" + str(i) + str(j), "Ť" + str(i) + str(j)): self.game.interacted = ["Toilet", i ,j]

                    # Door
                    elif self.interactive[hits[0]] in ("D" + str(i) + str(j), "G" + str(i) + str(j)): self.game.interacted = ["Door", i, j, hits[0].rect.left, hits[0].rect.top]

                    # Locker
                    elif self.interactive[hits[0]] in ("L" + str(i) + str(j), "Ľ" + str(i) + str(j), "ľ" + str(i) + str(j)): self.game.interacted = ["Locker", i, j]

                    # Bench
                    elif self.interactive[hits[0]] in ("B" + str(i) + str(j)): self.game.interacted = ["Bench", hits[0].rect.left, hits[0].rect.top, i, j]
                    elif self.interactive[hits[0]] in ("h" + str(i) + str(j)): self.game.interacted = ["BencH", hits[0].rect.left, hits[0].rect.top]

                    # Stairs
                    elif self.interactive[hits[0]] in ("S" + str(i) + str(j), "Z" + str(i) + str(j), "∟" + str(i) + str(j)): self.game.interacted = ["Stairs_up", i, j]
                    elif self.interactive[hits[0]] in ("s" + str(i) + str(j), "z" + str(i) + str(j), "↔" + str(i) + str(j)): self.game.interacted = ["Stairs_down", i, j]

                    # Basement
                    elif self.interactive[hits[0]] in ("b" + str(i) + str(j), "d" + str(i) + str(j)): self.game.interacted = ["Basement", i, j]

                    # Special desk
                    elif self.interactive[hits[0]] == "é" + str(i) + str(j): self.game.interacted = ["Desk", i ,j]
                    
                    # Bench press
                    elif self.interactive[hits[0]] in ("y" + str(i) + str(j), "Y" + str(i) + str(j)): self.game.interacted = ["Bench_press", i ,j]
                    
                    # Teacher
                    elif self.interactive[hits[0]] == "N" + str(i) + str(j): self.game.interacted = ["Teacher", i, j]

                    # Bookshelf
                    elif self.interactive[hits[0]] in ("O" + str(i) + str(j), "o" + str(i) + str(j), "ó" + str(i) + str(j), "Ó" + str(i) + str(j)): self.game.interacted = ["Bookshelf", i, j]

                    # Computer
                    elif self.interactive[hits[0]] == "g" + str(i) + str(j): self.game.interacted = ["Computer", i, j]

                    # Special window
                    elif self.interactive[hits[0]] == "w" + str(i) + str(j): self.game.interacted = ["Window", i, j]

                    # Router
                    elif self.interactive[hits[0]] == "E" + str(i) + str(j): self.game.interacted = ["Router", i, j]
                    
                    # Taburetky
                    elif self.interactive[hits[0]] in ("ý" + str(i) + str(j), "ž" + str(i) + str(j), "ú" + str(i) + str(j), "ň" + str(i) + str(j), "č" + str(i) + str(j)): self.game.interacted = ["Taburetka", hits[0].rect.left, hits[0].rect.top]
                    
                    # Green chairs
                    elif self.interactive[hits[0]] in ("@" + str(i) + str(j), "*" + str(i) + str(j), "#" + str(i) + str(j)): self.game.interacted = ["Green_chair", hits[0].rect.left, hits[0].rect.top]

                    # Pult
                    elif self.interactive[hits[0]] == "A" + str(i) + str(j): self.game.interacted = ["Pult", i, j]

                    # Baterries
                    elif self.interactive[hits[0]] == "ä" + str(i) + str(j): self.game.interacted = ["Battery", i, j]
                    
                    # Flashlight
                    elif self.interactive[hits[0]] == "8" + str(i) + str(j): self.game.interacted = ["Flashlight", i, j]

                    # Ladder
                    elif self.interactive[hits[0]] == "ď" + str(i) + str(j): self.game.interacted = ["Ladder", i, j]


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

