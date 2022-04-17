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
        self.npcs_spritesheet = Spritesheet("img/npc.png")

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
                elif column == "P": self.player_coords = Player(self, j, i) # Player
                elif column == "N": Npc(self, j, i) # NPC
        
        return (self.player_coords.x, self.player_coords.y)
                

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
        if self.rooms.index(previous_scene) + 1 >= len(self.rooms):
            print("No other room available")
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

        # After player dies
        self.running = False

    def events(self):
        """
        Events for the game loop
        """

        # Events
        for event in pygame.event.get():

            # Close button
            if event.type == pygame.QUIT: self.playing = self.running = False
                
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
        self.all_sprites.draw(self.screen) # Draws sprites onto the screen
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