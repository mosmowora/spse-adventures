# Import
import pygame, random as r
from leaderboard import Leaderboard
from quest import Quest
from save_progress import SaveProgress
from camera import Camera
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
        self.big_font = pygame.font.Font("Caveat.ttf", 40)
        self.font = pygame.font.Font("Roboto.ttf", 22)
        self.settings_font = pygame.font.Font("Caveat.ttf", 45)
        self.lrob_font = pygame.font.Font("Roboto.ttf", 13)

        # Spritesheets
        self.character_spritesheet = Spritesheet("img/character.png")
        self.terrain_spritesheet = Spritesheet("img/terrain.png")
        self.npcs_spritesheet = Spritesheet("img/npc.png")

        # Into and Game Over backgrounds
        self.intro_background = pygame.image.load("img/intro_background.png")
        self.settings_background = pygame.image.load("img/settings_bg.jpg")
        
        # Window icon and title (not final)
        icon = pygame.image.load('img/spselogo2.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('SPŠE ADVENTURE - REVENGEANCE')

        self.rooms: List[List[str]] = [ground_floor, first_floor, second_floor, third_floor, fourth_floor, basement] # Rooms where player can go
        self.in_room: List[str] = self.rooms[GROUND_FLOOR] # Room where player is rn (starting point) that's ground floor for those who don't know
        self.saved_room_data: str = "017"
        self.quest = Quest(self)
        self.grades: dict[str, int] = {}
        self.endings: List[str] = []
        self.camera = Camera(self)
        self.leaderboarding = Leaderboard(self)
        
        # Settings
        self.music_on: bool = True
        self.talking_speed_number: int = 90
        self.reseting_game_values()

        # Player name
        self.player_name: str = ""

        # Npc list
        self.npc = []

        # Sounds
        self.wow_iphone = pygame.mixer.Sound("sounds/wow_iphone.mp3")
        self.wow_iphone.set_volume(0.5)
        self.theme = pygame.mixer.Sound("sounds/theme.mp3")
        self.kacurovanie = pygame.mixer.Sound("sounds/kacurovanie.mp3")
        self.kacurovanie.set_volume(0.05)
        self.theme.set_volume(0.008)
        self.tsv_theme = pygame.mixer.Sound("sounds/bench.mp3")
        self.tsv_theme.set_volume(0.05)
        self.fall = pygame.mixer.Sound("sounds/fall.mp3")
        self.fall.set_volume(0.25)
        self.car = pygame.mixer.Sound("sounds/car.mp3")
        self.car.set_volume(0.1)
        self.lost = pygame.mixer.Sound("sounds/lost.mp3")
        self.lost.set_volume(0.5)
        self.lock = pygame.mixer.Sound("sounds/lock.mp3")
        self.lock.set_volume(0.25)
        self.door_open = pygame.mixer.Sound("sounds/door.mp3")
        self.door_open.set_volume(0.25)
        self.speed = pygame.mixer.Sound("sounds/speed.mp3")
        self.speed.set_volume(0.15)

    def set_level_camera(self, level: List[str]):
        """
        Moves camera and player to stairs
        """
        
        # Ground floor
        if level == ground_floor:
            for sprite in self.all_sprites:
                sprite.rect.x -= 39 * TILE_SIZE
                sprite.rect.y -= 7 * TILE_SIZE
            self.player.rect.x -= 120 * TILE_SIZE
            self.player.rect.y += 8 * TILE_SIZE
        
        # First floor
        elif level == first_floor:
            for sprite in self.all_sprites:
                sprite.rect.x -= 47 * TILE_SIZE
                sprite.rect.y -= 17 * TILE_SIZE
            self.player.rect.x -= 124 * TILE_SIZE
            self.player.rect.y += 2 * TILE_SIZE
        
        # Second floor
        elif level == second_floor:
            for sprite in self.all_sprites:
                sprite.rect.x -= 47 * TILE_SIZE
                sprite.rect.y -= 19 * TILE_SIZE
            self.player.rect.x -= 124 * TILE_SIZE
            self.player.rect.y += 2 * TILE_SIZE
        
        # Third floor
        elif level == third_floor:
            for sprite in self.all_sprites:
                sprite.rect.x -= 62 * TILE_SIZE
                sprite.rect.y -= 4 * TILE_SIZE
                
        # Fourth floor
        elif level == fourth_floor: 
            for sprite in self.all_sprites:
                sprite.rect.x -= 62 * TILE_SIZE
                sprite.rect.y -= 4 * TILE_SIZE

    def reseting_game_values(self):
        """
        When player wants to restart
        """

        # Room and floor
        self.saved_room_data = "017"
        self.in_room = self.rooms[GROUND_FLOOR]

        # Objects you can interact with
        self.interacted: List[str, int] = ["", "", "", "", ""]
        self.interactive = {}

        # Inventory
        self.inv: dict[str, str] = {}

        # Variables for endings
        self.without_light: int = 0
        self.caught: int = 0

        # Quests variables
        self.__gul_counter: int = 0
        self.connected_router = True

        # Variables for finding items/doing stuff
        self.key_in_trash: bool = True
        self.locked_locker: bool = True
        self.locked_changing_room: bool = True
        self.number_kokosky: int = 0
        self.kokosky_in_locker: bool = True
        self.kokosky_in_bookshelf: bool = True
        self.kokosky_under_bench: bool = True
        self.kokosky_in_trash: bool = True
        self.vtipnicek: bool = True
        self.dumbbell_lifted: bool = True
        self.program_test: bool = True
        self.phone_in_trash: bool = True
        self.suplovanie: bool = True
        self.anj_test: bool = True
        self.gul_quest: bool = True
        self.nepusti: bool = True
        self.five_min_sooner: bool = True
        self.locker_stuff: dict[str, bool] = {"crocs": True, "boots": False, "key": True}

        # Grader
        self.grades: dict[str, int] = {}

    def create_tile_map(self):
        """
        Creates tile map
        """

        self.interactive = {}

        for sprite in self.all_sprites: sprite.kill()

        for i, row in enumerate(self.in_room):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "_": Blockade(self, j, i, "_") # Grass
                elif column == "?": Blockade(self, j, i, "?") # Black
                elif column == "!": Block(self, j, i, "!") # No entry ground
                elif column == "P": self.player = Player(self, j, i) # Player
                elif column == "W": Block(self, j, i, "W") # Basic wall
                elif column == "w": self.interactive[Block(self, j, i, "w")] = "w" + str(i) + str(j) # Window
                elif column == "L": self.interactive[Block(self, j, i, "L")] = "L" + str(i) + str(j) # Locker
                elif column == "Ľ": self.interactive[Block(self, j, i, "Ľ")] = "Ľ" + str(i) + str(j) # Locker
                elif column == "ľ": self.interactive[Block(self, j, i, "ľ")] = "ľ" + str(i) + str(j) # Locker
                elif column == "S": self.interactive[Block(self, j, i, "S")] = "S" + str(i) + str(j) # Stairs
                elif column == "Z": self.interactive[Block(self, j, i, "Z")] = "Z" + str(i) + str(j) # Stairs
                elif column == "s": self.interactive[Block(self, j, i, "s")] = "s" + str(i) + str(j) # Stairs down
                elif column == "z": self.interactive[Block(self, j, i, "z")] = "z" + str(i) + str(j) # Stairs down
                elif column == "D": self.interactive[Block(self, j, i, "D")] = "D" + str(i) + str(j) # Door
                elif column == "G": self.interactive[Block(self, j, i, "G")] = "G" + str(i) + str(j) # Glass door
                elif column == "B": self.interactive[Block(self, j, i, "B")] = "B" + str(i) + str(j) # Bench (vertical)
                elif column == "h": self.interactive[Block(self, j, i, "h")] = "h" + str(i) + str(j) # Bench (horizontal)
                elif column == "y": self.interactive[Block(self, j, i, "y")] = "y" + str(i) + str(j) # Benchpress
                elif column == "Y": self.interactive[Block(self, j, i, "Y")] = "Y" + str(i) + str(j) # Benchpress with dumbbells
                elif column == "l": self.interactive[Block(self, j, i, "l")] = "l" + str(i) + str(j) # Desk + chair (vertical) left
                elif column == "k": self.interactive[Block(self, j, i, "k")] = "k" + str(i) + str(j) # Desk no chair (vertical) left
                elif column == "é": self.interactive[Block(self, j, i, "é")] = "é" + str(i) + str(j) # Desk special (vertical)
                elif column == "u": self.interactive[Block(self, j, i, "u")] = "u" + str(i) + str(j) # Desk + chair (vertical) right
                elif column == "e": self.interactive[Block(self, j, i, "e")] = "e" + str(i) + str(j) # Desk no chair (vertical) right
                elif column == "g": self.interactive[Block(self, j, i, "g")] = "g" + str(i) + str(j) # Desk + chair + PC (vertical) right
                elif column == "a": self.interactive[Block(self, j, i, "a")] = "a" + str(i) + str(j) # Desk + chair + PC (vertical) left
                elif column == "U": self.interactive[Block(self, j, i, "U")] = "U" + str(i) + str(j) # LCUJ Desk
                elif column == "J": self.interactive[Block(self, j, i, "J")] = "J" + str(i) + str(j) # LCUJ Desk
                elif column == "j": self.interactive[Block(self, j, i, "j")] = "j" + str(i) + str(j) # Desk + chair (horizontal) up
                elif column == "m": self.interactive[Block(self, j, i, "m")] = "m" + str(i) + str(j) # Desk no chair (horizontal) up
                elif column == "i": self.interactive[Block(self, j, i, "i")] = "i" + str(i) + str(j) # Desk + chair (horizontal) down
                elif column == "n": self.interactive[Block(self, j, i, "n")] = "n" + str(i) + str(j) # Desk no chair (horizontal) down
                elif column == "q": self.interactive[Block(self, j, i, "q")] = "q" + str(i) + str(j) # Desk + chair + PC (horizontal) up
                elif column == "Q": self.interactive[Block(self, j, i, "Q")] = "Q" + str(i) + str(j) # Desk + chair + PC (horizontal) down
                elif column == "t": self.interactive[Block(self, j, i, "t")] = "t" + str(i) + str(j) # Trashcan
                elif column == "T": self.interactive[Block(self, j, i, "T")] = "T" + str(i) + str(j) # Toilet
                elif column == "Ť": self.interactive[Block(self, j, i, "Ť")] = "Ť" + str(i) + str(j) # Toilet
                elif column == "R": self.interactive[Block(self, j, i, "R")] = "R" + str(i) + str(j) # Rails
                elif column == "r": self.interactive[Block(self, j, i, "r")] = "r" + str(i) + str(j) # Rails
                elif column == "Ř": self.interactive[Block(self, j, i, "Ř")] = "Ř" + str(i) + str(j) # Rails ground_floor
                elif column == "Ŕ": self.interactive[Block(self, j, i, "Ŕ")] = "Ŕ" + str(i) + str(j) # Rails second_floor
                elif column == "ŕ": self.interactive[Block(self, j, i, "ŕ")] = "ŕ" + str(i) + str(j) # Rails second_floor
                elif column == "ř": self.interactive[Block(self, j, i, "ř")] = "ř" + str(i) + str(j) # Rails ground_floor
                elif column == "/": self.interactive[Block(self, j, i, "/")] = "/" + str(i) + str(j) # Rails fourth_floor
                elif column == "|": self.interactive[Block(self, j, i, "|")] = "|" + str(i) + str(j) # Rails fourth_floor
                elif column == "b": self.interactive[Block(self, j, i, "b")] = "b" + str(i) + str(j) # Basement
                elif column == "d": self.interactive[Block(self, j, i, "d")] = "d" + str(i) + str(j) # Basement
                elif column == "O": self.interactive[Block(self, j, i, "O")] = "O" + str(i) + str(j) # Bookshelf
                elif column == "o": self.interactive[Block(self, j, i, "o")] = "o" + str(i) + str(j) # Bookshelf
                elif column == "ó": self.interactive[Block(self, j, i, "ó")] = "ó" + str(i) + str(j) # Bookshelf
                elif column == "Ó": self.interactive[Block(self, j, i, "Ó")] = "Ó" + str(i) + str(j) # Bookshelf
                elif column == "]": self.interactive[Block(self, j, i, "]")] = "]" + str(i) + str(j) # Whiteboard -> (that way)
                elif column == "[": self.interactive[Block(self, j, i, "[")] = "[" + str(i) + str(j) # Whiteboard <- (that way)
                elif column == "-": self.interactive[Block(self, j, i, "-")] = "-" + str(i) + str(j) # Whiteboard ^ (that way)
                elif column == "=": self.interactive[Block(self, j, i, "=")] = "=" + str(i) + str(j) # Whiteboard V (that way)
                elif column == "}": self.interactive[Block(self, j, i, "}")] = "}" + str(i) + str(j) # Blackboard -> (that way)
                elif column == "{": self.interactive[Block(self, j, i, "{")] = "{" + str(i) + str(j) # Blackboard <- (that way)
                elif column == "^": self.interactive[Block(self, j, i, "^")] = "^" + str(i) + str(j) # Blackboard ^ (that way)
                elif column == "V": self.interactive[Block(self, j, i, "V")] = "V" + str(i) + str(j) # Blackboard V (that way)
                elif column == "x": self.interactive[Block(self, j, i, "x")] = "x" + str(i) + str(j) # Double Vertical Whiteboard
                elif column == "X": self.interactive[Block(self, j, i, "X")] = "X" + str(i) + str(j) # Double Horizontal Whiteboard
                elif column == "E": self.interactive[Block(self, j, i, "E")] = "E" + str(i) + str(j) # Router
                elif column == "ý": self.interactive[Block(self, j, i, "ý")] = "ý" + str(i) + str(j) # ý as in Yellow Taburetka
                elif column == "ž": self.interactive[Block(self, j, i, "ž")] = "ž" + str(i) + str(j) # ž as in Green (želena) Taburetka
                elif column == "ň": self.interactive[Block(self, j, i, "ň")] = "ň" + str(i) + str(j) # ň as in Brown (hňeda) Taburetka
                elif column == "ú": self.interactive[Block(self, j, i, "ú")] = "ú" + str(i) + str(j) # ú as in Blúe Taburetka
                elif column == "$": self.interactive[Block(self, j, i, "$")] = "$" + str(i) + str(j) # Corner desk
                elif column == "č": self.interactive[Block(self, j, i, "č")] = "č" + str(i) + str(j) # č as in Red (červena) Taburetka
                elif column == "@": self.interactive[Block(self, j, i, "@")] = "@" + str(i) + str(j) # Up facing green chair
                elif column == "#": self.interactive[Block(self, j, i, "#")] = "#" + str(i) + str(j) # Right facing green chair
                elif column == "*": self.interactive[Block(self, j, i, "*")] = "*" + str(i) + str(j) # Left facing green chair
                elif column == "~": self.interactive[Block(self, j, i, "~")] = "~" + str(i) + str(j) # Coffee machine
                elif column == "N": self.interactive[Npc(self, j, i, "")] = "N" + str(i) + str(j)  # NPC
                elif column == "K": self.interactive[Npc(self, j, i, "K")] = "K" + str(i) + str(j)  # NPC
                elif column == "C": self.npc.append(Npc(self, j, i, "C")) # Cleaner

    def set_camera(self, level: List[str]):
            if level == ground_floor: self.camera.set_ground_camera()
            elif level == first_floor: self.camera.set_first_camera()
            elif level == second_floor: self.camera.set_second_camera()
            elif level == third_floor: self.camera.set_third_camera()
            elif level == fourth_floor: self.camera.set_fourth_camera()
    
    def new(self, t: str):
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
        self.cleaner = pygame.sprite.LayeredUpdates()

        # Loads data
        data = SaveProgress.load_data(self.player_name)
        
        # Has profile
        if data is not None and t == "new":

            # Level
            self.in_room = self.rooms[data["level"]]
            self.saved_room_data = data['room_number']

            # Inventory
            self.inv = data["inventory"]

            # Variables for endings
            self.without_light = data["quests"]["without_light"]
            self.caught = data["quests"]["caught"]
            self.endings = data["endings"]

            # Variables for finding items/doing stuff
            self.key_in_trash = data["quests"]["key_in_trash"]
            self.locked_locker = data["quests"]["locked_locker"]
            self.locked_changing_room = data["quests"]["locked_changing_room"]
            self.number_kokosky = data["quests"]["number_kokosky"]
            self.kokosky_in_locker = data["quests"]["kokosky_in_locker"]
            self.kokosky_in_bookshelf = data["quests"]["kokosky_in_bookshelf"]
            self.kokosky_under_bench = data["quests"]["kokosky_under_bench"]
            self.kokosky_in_trash = data["quests"]["kokosky_in_trash"]
            self.locker_stuff = data["quests"]["locker_stuff"]
            self.vtipnicek = data["quests"]["vtipnicek"]
            self.dumbbell_lifted = data["quests"]["dumbbells"]
            self.program_test = data["quests"]["program"]
            self.suplovanie = data["quests"]['suplovanie']
            self.phone_in_trash = data["quests"]["phone"]
            self.anj_test = data["quests"]["anj_test"]
            self.gul_quest = data["quests"]['GUL_quest']
            self.__gul_counter = data["quests"]["gul_counter"]
            self.nepusti = data["quests"]["nepusti"]
            self.connected_router = data["quests"]["router"]
            self.five_min_sooner = data["quests"]["sooner"]

            # Grades
            self.grades = data['grades']

            # Saved settings
            self.music_on = data["settings"]["music"]
            self.talking_speed_number = data["settings"]["talking_speed"]

            # Tile map
            self.create_tile_map()

            # Moving camera/player
            if self.saved_room_data == "Hall": self.set_level_camera(self.in_room)
            else: self.set_camera(self.in_room)
            
        # New player
        else: 
            
            # Tilemap
            self.create_tile_map()

            # Moving camera
            for sprite in self.all_sprites: sprite.rect.x -= 158 * TILE_SIZE

        return self
    
    def main(self):
        """
        Game loop
        """

        if not self.music_on: pygame.mixer.Sound.stop(self.theme)

        # Main game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.craft()

        return self
    
    def events(self):
        """
        Events for the game loop
        """

        # Events
        for event in pygame.event.get():

            # Close button/Esc
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: self.exiting()

            # Pressed I
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_i: 
                pygame.image.save(self.screen, "img/screen.png")
                self.inventory() 

            # Pressed E
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:

                # What was clicked
                match self.player.facing:
                    case "up": Interact(self, self.player.rect.x, self.player.rect.y - TILE_SIZE, self.interactive)
                    case "down": Interact(self, self.player.rect.x, self.player.rect.y + TILE_SIZE, self.interactive)
                    case "left": Interact(self, (self.player.rect.x - TILE_SIZE), self.player.rect.y, self.interactive)
                    case "right": Interact(self, (self.player.rect.x + TILE_SIZE), self.player.rect.y, self.interactive) 
                
                # What was clicked
                match self.interacted[0].capitalize():
                    case "Trashcan": self.trashcan()
                    case "Door": self.door()
                    case "Locker": self.locker()
                    case "Bench": self.bench()
                    case "Stairs_up": self.stairs()
                    case "Stairs_down": self.stairs()
                    case "Basement": self.basement()
                    case "Toilet": self.toilet()
                    case "Teacher": self.talking_with_teachers()
                    case "Bookshelf": self.bookshelf()
                    case "Desk": self.desk()
                    case "Computer": self.quest.programming()
                    case "Bench_press": self.dumbbell_lifted = self.quest.bench_press(self.dumbbell_lifted)
                    case "Window": self.window()
                    case "Taburetka": self.taburetka()
                    case "Green_chair": self.green_chair()
                    case "Router": 
                        if type(self.connected_router) == list: router_outcome = self.quest.router(); self.info("Connected routers {}/4".format(len(self.connected_router) + 1), BLACK); self.connected_router.append(router_outcome) if len(router_outcome) == 3 else self.info(router_outcome, BLACK)
                        else: self.talking("I don't know what to do with this.")
                # Reset
                self.interacted = ["", "", ""]

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

    def exiting(self):
        """
        After player presses Close button
        """

        # Buttons
        bg = pygame.image.load("img/exiting.png")
        return_button = Button(WIN_WIDTH // 2 - 155, WIN_HEIGHT // 2 - 45, 150, 40, fg=WHITE, bg=BLACK, content="Return", fontsize=32)
        settings_button = Button(WIN_WIDTH // 2 + 5, WIN_HEIGHT // 2 - 45, 150, 40, fg=WHITE, bg=BLACK, content="Settings", fontsize=32)
        sq_button = Button(WIN_WIDTH // 2 - 155, WIN_HEIGHT // 2 + 5, 310, 40, fg=WHITE, bg=BLACK, content="Save & Quit", fontsize=32)
        exit_pause: bool = False
        while True:

            # Close button
            for event in pygame.event.get():
                if event.type == pygame.QUIT: quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: exit_pause = not exit_pause; break
                    elif event.key == pygame.K_s: self.settings()

            if exit_pause: break
            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Settings button was pressed
            if settings_button.is_pressed(mouse_pos, mouse_pressed): self.settings()

            # Return button was pressed
            if return_button.is_pressed(mouse_pos, mouse_pressed): break

            # Save & Quit button was pressed
            if sq_button.is_pressed(mouse_pos, mouse_pressed): self.save_game(); quit()

            # BG
            self.screen.blit(bg, (0, 0))

            # Buttons
            self.screen.blit(return_button.image, return_button.rect)
            self.screen.blit(settings_button.image, settings_button.rect)
            self.screen.blit(sq_button.image, sq_button.rect)

            # Updates
            self.clock.tick(FPS)
            pygame.display.update()

    def inventory(self):
        """
        Opens/Closes inventory
        """

        open_inventory = True
        inventory_coords: dict[str, pygame.Rect] = {}
        
        # Screen of the game
        bg = pygame.image.load("img/screen.png")

        # Inventory
        fg = pygame.image.load("img/inv_fg.png")

        # Min/Max items
        min_items = 0
        max_items = 7

        while open_inventory:

            # Background
            self.screen.blit(bg, (0, 0))

            # Inv items
            n = 0
            m = 0
            for i in self.inv:
                if n >= min_items:
                    fg_rect = fg.get_rect(x=10 + 85 * m, y=10)
                    img = pygame.image.load(self.inv[i])
                    rect = img.get_rect(x=10 + 85 * m, y=10)

                    # Display items
                    self.screen.blit(fg, fg_rect)
                    self.screen.blit(img, rect)
                    
                    # Inventory coords for items
                    inventory_coords[self.inv[i]] = rect

                    m += 1
                n += 1
                if n == max_items: break

            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: self.exiting()

                # Esc/I
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.KEYDOWN and event.key == pygame.K_i: open_inventory = False; break

                # Right arrow
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and len(self.inv.keys()) > max_items: max_items += 7; min_items += 7

                # Left arrow
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and min_items != 0: max_items -= 7; min_items -= 7
                
                # Items in inv
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in inventory_coords:
                        if inventory_coords[i].collidepoint(event.pos): self.inventory_item_info(i); break

            # Updates
            self.clock.tick(FPS)
            pygame.display.update()
                  
    def inventory_item_info(self, img: str):
        """
        Player talks about item in inventory
        """
        
        match img:
            
            case "img/locker key.png": self.info("A key from my locker. It's 10th from the door.", BRITISH_WHITE, 90) # Locker key
            case "img/changing_room key.png": self.info("This key is used for OUR changing room.", BRITISH_WHITE, 90) # Changing room key
            case "img/vtipnicek_small.png": self.info("I can read you.", BRITISH_WHITE, 90); self.open_vtipnicek() # Vtipnicek
            case "img/Iphone_small.png": self.info("Let's check my phone", BRITISH_WHITE, 90); self.suplovanie = self.quest.check_suplovanie() # Iphone
            case "img/kokosky1_small.png": self.info("1 of 4 parts of Forbidden Kokosky", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky2_small.png": self.info("1 of 4 parts of Forbidden Kokosky", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky3_small.png": self.info("1 of 4 parts of Forbidden Kokosky", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky4_small.png": self.info("1 of 4 parts of Forbidden Kokosky", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky12_small.png": self.info("2 of 4 parts of Forbidden Kokosky", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky13_small.png": self.info("2 of 4 parts of Forbidden Kokosky", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky14_small.png": self.info("2 of 4 parts of Forbidden Kokosky", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky23_small.png": self.info("2 of 4 parts of Forbidden Kokosky", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky24_small.png": self.info("2 of 4 parts of Forbidden Kokosky", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky34_small.png": self.info("2 of 4 parts of Forbidden Kokosky", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky123_small.png": self.info("3 of 4 parts of Forbidden Kokosky", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky124_small.png": self.info("3 of 4 parts of Forbidden Kokosky", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky234_small.png": self.info("3 of 4 parts of Forbidden Kokosky", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky_small.png": self.info("Forbidden Kokosky", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky

    def show_kokosky(self, img: str):
        """
        Opens big image of kokosky
        """

        kokoskoing = True

        match img:
            case "img/kokosky1_small.png": bg = pygame.image.load("img/kokosky1.png")
            case "img/kokosky2_small.png": bg = pygame.image.load("img/kokosky2.png")
            case "img/kokosky3_small.png": bg = pygame.image.load("img/kokosky3.png")
            case "img/kokosky4_small.png": bg = pygame.image.load("img/kokosky4.png")
            case "img/kokosky12_small.png": bg = pygame.image.load("img/kokosky12.png")
            case "img/kokosky13_small.png": bg = pygame.image.load("img/kokosky13.png")
            case "img/kokosky14_small.png": bg = pygame.image.load("img/kokosky14.png")
            case "img/kokosky23_small.png": bg = pygame.image.load("img/kokosky23.png")
            case "img/kokosky24_small.png": bg = pygame.image.load("img/kokosky24.png")
            case "img/kokosky34_small.png": bg = pygame.image.load("img/kokosky34.png")
            case "img/kokosky123_small.png": bg = pygame.image.load("img/kokosky123.png")
            case "img/kokosky124_small.png": bg = pygame.image.load("img/kokosky124.png")
            case "img/kokosky234_small.png": bg = pygame.image.load("img/kokosky234.png")
            case "img/kokosky_small.png": bg = pygame.image.load("img/kokosky.png")

        while kokoskoing:

            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: self.exiting()

                # Esc
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: kokoskoing = False

            # Bg
            self.screen.blit(bg, (0, 0))

            # Updates
            self.clock.tick(FPS)
            pygame.display.update()

    def craft(self):
        """
        If player has items to craft something it will be crafted
        """

        inv = self.inv.keys()
        
        if "Kokosky1" in inv and "Kokosky2" in inv:
            self.inv.pop("Kokosky1"); self.inv.pop("Kokosky2")
            self.inv["Kokosky12"] = "img/kokosky12_small.png"

        if "Kokosky1" in inv and "Kokosky3" in inv:
            self.inv.pop("Kokosky1"); self.inv.pop("Kokosky3")
            self.inv["Kokosky13"] = "img/kokosky13_small.png"

        if "Kokosky1" in inv and "Kokosky4" in inv:
            self.inv.pop("Kokosky1"); self.inv.pop("Kokosky4")
            self.inv["Kokosky14"] = "img/kokosky14_small.png"

        if "Kokosky2" in inv and "Kokosky3" in inv:
            self.inv.pop("Kokosky2"); self.inv.pop("Kokosky3")
            self.inv["Kokosky23"] = "img/kokosky23_small.png"

        if "Kokosky2" in inv and "Kokosky4" in inv:
            self.inv.pop("Kokosky2"); self.inv.pop("Kokosky4")
            self.inv["Kokosky24"] = "img/kokosky24_small.png"

        if "Kokosky3" in inv and "Kokosky4" in inv:
            self.inv.pop("Kokosky3"); self.inv.pop("Kokosky4")
            self.inv["Kokosky34"] = "img/kokosky34_small.png"

        if "Kokosky12" in inv and "Kokosky3" in inv:
            self.inv.pop("Kokosky12"); self.inv.pop("Kokosky3")
            self.inv["Kokosky123"] = "img/kokosky123_small.png"

        if "Kokosky12" in inv and "Kokosky4" in inv:
            self.inv.pop("Kokosky12"); self.inv.pop("Kokosky4")
            self.inv["Kokosky124"] = "img/kokosky124_small.png"

        if "Kokosky13" in inv and "Kokosky2" in inv:
            self.inv.pop("Kokosky13"); self.inv.pop("Kokosky2")
            self.inv["Kokosky123"] = "img/kokosky123_small.png"

        if "Kokosky13" in inv and "Kokosky4" in inv:
            self.inv.pop("Kokosky13"); self.inv.pop("Kokosky4")
            self.inv["Kokosky134"] = "img/kokosky134_small.png"

        if "Kokosky14" in inv and "Kokosky2" in inv:
            self.inv.pop("Kokosky14"); self.inv.pop("Kokosky2")
            self.inv["Kokosky124"] = "img/kokosky124_small.png"

        if "Kokosky14" in inv and "Kokosky3" in inv:
            self.inv.pop("Kokosky14"); self.inv.pop("Kokosky3")
            self.inv["Kokosky134"] = "img/kokosky134_small.png"

        if "Kokosky23" in inv and "Kokosky1" in inv:
            self.inv.pop("Kokosky23"); self.inv.pop("Kokosky1")
            self.inv["Kokosky123"] = "img/kokosky123_small.png"

        if "Kokosky23" in inv and "Kokosky4" in inv:
            self.inv.pop("Kokosky23"); self.inv.pop("Kokosky4")
            self.inv["Kokosky234"] = "img/kokosky234_small.png"

        if "Kokosky24" in inv and "Kokosky1" in inv:
            self.inv.pop("Kokosky24"); self.inv.pop("Kokosky1")
            self.inv["Kokosky124"] = "img/kokosky124_small.png"

        if "Kokosky24" in inv and "Kokosky3" in inv:
            self.inv.pop("Kokosky24"); self.inv.pop("Kokosky3")
            self.inv["Kokosky234"] = "img/kokosky234_small.png"

        if "Kokosky34" in inv and "Kokosky1" in inv:
            self.inv.pop("Kokosky34"); self.inv.pop("Kokosky1")
            self.inv["Kokosky134"] = "img/kokosky134_small.png"

        if "Kokosky34" in inv and "Kokosky3" in inv:
            self.inv.pop("Kokosky34"); self.inv.pop("Kokosky3")
            self.inv["Kokosky234"] = "img/kokosky234_small.png"

        if "Kokosky123" in inv and "Kokosky4" in inv:
            self.inv.pop("Kokosky123"); self.inv.pop("Kokosky4")
            self.inv["Kokosky"] = "img/kokosky_small.png"

        if "Kokosky124" in inv and "Kokosky3" in inv:
            self.inv.pop("Kokosky124"); self.inv.pop("Kokosky3")
            self.inv["Kokosky"] = "img/kokosky_small.png"

        if "Kokosky134" in inv and "Kokosky2" in inv:
            self.inv.pop("Kokosky134"); self.inv.pop("Kokosky2")
            self.inv["Kokosky"] = "img/kokosky_small.png"

        if "Kokosky234" in inv and "Kokosky1" in inv:
            self.inv.pop("Kokosky234"); self.inv.pop("Kokosky1")
            self.inv["Kokosky"] = "img/kokosky_small.png"

    def open_vtipnicek(self):
        """
        Player can read funny jokes from vtipnicek (not a quest)\n
        relaxation purposes only
        """

        open_vtipnicek = True

        # Screen of the game
        bg = pygame.image.load("img/screen.png")

        # Vtipnicek
        fg = pygame.image.load("img/vtipnicek_one.png")
        fg_rect = fg.get_rect(x=WIN_WIDTH // 2 - 328 // 2, y=WIN_HEIGHT // 2 - 220 // 2)

        # Events
        while open_vtipnicek:

            # Background
            self.screen.blit(bg, (0, 0))

            # Vtipnicek
            self.screen.blit(fg, fg_rect)

            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: self.exiting()

                # Esc/I
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.KEYDOWN and event.key == pygame.K_i: open_vtipnicek = not open_vtipnicek; break # BRUH

            # Updates
            self.clock.tick(FPS)
            pygame.display.update()
    
    def save_game(self):
        """
        Saves game to file by player name
        """

        # Quests
        self.quests = { "key_in_trash": self.key_in_trash,
                        "locked_locker": self.locked_locker, 
                        "locked_changing_room": self.locked_changing_room, 
                        "number_kokosky": self.number_kokosky,
                        "kokosky_in_locker": self.kokosky_in_locker, 
                        "kokosky_in_bookshelf": self.kokosky_in_bookshelf, 
                        "kokosky_under_bench": self.kokosky_under_bench,
                        "kokosky_in_trash": self.kokosky_in_trash,
                        "vtipnicek": self.vtipnicek,
                        "dumbbells": self.dumbbell_lifted,
                        "program": self.program_test,
                        "phone": self.phone_in_trash,
                        "suplovanie": self.suplovanie,
                        "anj_test": self.anj_test,
                        "GUL_quest": self.gul_quest,
                        "gul_counter": self.__gul_counter,
                        "nepusti": self.nepusti,
                        "router": self.connected_router,
                        "sooner": self.five_min_sooner, 
                        "locker_stuff": self.locker_stuff, 
                        "without_light": self.without_light,
                        "caught": self.caught
                        }
        
        # Saving
        self.database = SaveProgress(self.player_name, 
                                    self.inv,
                                    self.endings,
                                    self.quests,
                                    self.rooms.index(self.in_room),
                                    self.saved_room_data,
                                    self.grades,
                                    {
                                        "music": self.music_on,
                                        "talking_speed": self.talking_speed_number
                                    }
                                    )
        self.database.save()
        print("SAVED")

    def game_over(self, img: str):
        """
        Game over screen
        """

        if self.music_on: pygame.mixer.Sound.stop(self.theme)

        # Ending
        endings = ["img/lost.png", "img/you_never_learn.png", "img/window_fail.png", "img/early.png"]
        all_endings = (f"img/{ending}.png" for ending in self.endings)

        # True ak ending je jeden z konecny (lost in school e.g.) hra zacina uplne odznova, ak False tak hrac ide na startovacie miesto (caught by cleaning lady e.g.)
        end = True if img in endings else False

        # BG
        self.game_over_background = pygame.image.load(img)

        # Creates text
        text = self.big_font.render("Game Over", True, BLACK)
        text_rect = text.get_rect(center = (75, 50))

        # Creates button
        restart_button = Button(10, WIN_HEIGHT - 60, 200, 50, WHITE, DARK_GRAY, "Main menu", 32) if end else Button(10, WIN_HEIGHT - 60, 200, 50, WHITE, DARK_GRAY, "Try again", 32)
        iamdone_button = Button(10, WIN_HEIGHT - 120, 200, 50, WHITE, DARK_GRAY, "Save & Quit", 32)

        # Window fail
        if img == "img/window_fail.png": 
            car_oops = pygame.image.load("img/car_oops.png")
            car_dead = pygame.image.load("img/car_dead.png")
            car_oops_move = -270
            car_dead_move = -700
            if self.music_on: pygame.mixer.Sound.play(self.car, -1)

        # Lost 
        elif img == "img/lost.png" and self.music_on: pygame.mixer.Sound.play(self.lost, -1)

        # Early
        elif img == "img/early.png" and self.music_on: pygame.mixer.Sound.play(self.speed, -1)

        # Removing every sprite
        for sprite in self.all_sprites: sprite.kill()

        # Loop
        while self.game_running:

            # Close button
            for event in pygame.event.get():
                if event.type == pygame.QUIT: quit()

            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Restart button
            if restart_button.is_pressed(mouse_pos, mouse_pressed): 
                if end: 
                    if img not in all_endings: self.endings.append(img[4:-4]) # Appends the name of the ending intead of the actual image
                    self.reseting_game_values(); self.save_game(); self.intro_screen().new("new").main()
                else: self.new("old").main()

            # Save & Quit button
            elif iamdone_button.is_pressed(mouse_pos, mouse_pressed): 
                if img not in all_endings: self.endings.append(img[4:-4]) # Appends the name of the ending intead of the actual image
                if end: self.reseting_game_values()
                self.save_game(); quit()
            
            # Displaying background, text, button
            self.screen.blit(self.game_over_background, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.screen.blit(iamdone_button.image, iamdone_button.rect)

            # Window ending
            if img == "img/window_fail.png": 
                self.screen.blit(car_oops, (car_oops_move, 81))
                self.screen.blit(car_dead, (car_dead_move, 81))
                car_oops_move += 5
                car_dead_move += 5
                if car_dead_move >= 1000:
                    car_oops_move = -270
                    car_dead_move = -700

            self.clock.tick(FPS)
            pygame.display.update()

        if img == "img/window_fail.png": pygame.mixer.Sound.stop(self.car)
        elif img == "img/lost.png": pygame.mixer.Sound.stop(self.lost)

    def intro_screen(self):
        """
        Intro screen
        """

        # Start music
        pygame.mixer.Sound.play(self.theme, -1)

        intro = True

        # Title
        title = self.big_font.render("SPSE ADVENTURE", True, BLACK)
        title_rect = title.get_rect(x=10, y=10)

        # Made by
        made = self.font.render("Made by: MTS", True, WHITE)
        made_rect = made.get_rect(x=490, y=450)

        # Start button
        play_button = Button(10, 60, 180, 50, fg=WHITE, bg=BLACK, content="Play", fontsize=32)

        # Settings button
        settings_button = Button(10, 120, 180, 50, fg=WHITE, bg=BLACK, content="Settings", fontsize=32)

        # Leaderboard button
        leaderboard_button = Button(10, 180, 180, 50, fg=WHITE, bg=BLACK, content="Leaderboard", fontsize=32)

        # Main loop for intro
        while intro:

            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: quit()

            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Play button was pressed
            if play_button.is_pressed(mouse_pos, mouse_pressed): intro = self.start(intro)
            if not intro: break

            # Settings button was pressed
            if settings_button.is_pressed(mouse_pos, mouse_pressed): self.settings()
            
            # Leadboard button was pressed
            if leaderboard_button.is_pressed(mouse_pos, mouse_pressed): self.leaderboarding.show_leaderboard()

            # Diplaying background, title, buttons
            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(made, made_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(settings_button.image, settings_button.rect)
            self.screen.blit(leaderboard_button.image, leaderboard_button.rect)
            
            # Updates
            self.clock.tick(FPS)
            pygame.display.update()

        return self
    
    def start(self, intro: bool):
        """
        Starting the game
        """

        picking_name = True
        active = False

        # Button
        back = Button(10, WIN_HEIGHT - 60, 200, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)

        # Title
        title = self.big_font.render("SPSE ADVENTURE", True, BLACK)
        title_rect = title.get_rect(x=10, y=10)

        # Made by
        made = self.font.render("Made by: MTS", True, WHITE)
        made_rect = made.get_rect(x=490, y=450)

        # Your name
        your_name = self.font.render("Your name:", True, WHITE)
        your_name_rect = made.get_rect(x=10, y=62)
        
        # Input rectangle
        input_rect = pygame.Rect(130, 60, 200, 32)

        while picking_name:

            for event in pygame.event.get():
      
                # Quit
                if event.type == pygame.QUIT: quit()
        
                # Click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos): active = True
                    else: active = False

                # Keyboard
                if event.type == pygame.KEYDOWN:
      
                    # Esc
                    if event.key == pygame.K_ESCAPE: picking_name = False

                    # Check for backspace
                    elif event.key == pygame.K_BACKSPACE and active: self.player_name = self.player_name[:-1]
                    
                    # Enter
                    elif event.key == pygame.K_RETURN: 
                        if len(self.player_name) > 0: picking_name = intro = False; break

                    # Unicode
                    elif active: self.player_name += event.unicode

            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            if back.is_pressed(mouse_pos, mouse_pressed): picking_name = False

            # Background
            self.screen.blit(self.intro_background, (0, 0))

            # Your name
            self.screen.blit(your_name, your_name_rect)

            if active: color = GRAY
            else: color = BLACK

            # Input rectangle
            pygame.draw.rect(self.screen, color, input_rect)
    
            # Input Text
            text_surface = self.font.render(self.player_name, True, (255, 255, 255))
            self.screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))

            # Width of rectangle
            input_rect.w = max(200, text_surface.get_width()+10)

            # Button
            self.screen.blit(back.image, back.rect)

            # Text
            self.screen.blit(made, made_rect)
            self.screen.blit(title, title_rect)
            self.clock.tick(FPS)
            pygame.display.flip()

        return intro
    
    def settings(self):
        """
        Opens settings window
        """
        
        music_playing = True
        opened = True

        # Slider
        slider_back = Button(250, 155, 100, 20, fg=BLACK, bg=DIM_GRAY, content="", fontsize=0)
        slider = Button(300, 140, 50, 50, fg=BLACK, bg=GREEN, content="", fontsize=0) if self.music_on else Button(250, 140, 50, 50, fg=BLACK, bg=RED, content="", fontsize=0)
        slider_inside = Button(312.5, 152.5, 25, 25, fg=BLACK, bg=BLACK, content="", fontsize=0) if self.music_on else Button(262.5, 152.5, 25, 25, fg=BLACK, bg=BLACK, content="", fontsize=0)

        # Talking speed
        slow = Button(225, 260, 130, 50, fg=BLACK, bg=DIM_GRAY, content="SLOW", fontsize=32) if self.talking_speed_number == 120 else Button(225, 260, 130, 50, fg=BLACK, bg=WHITE, content="SLOW", fontsize=32)
        medium = Button(365, 260, 130, 50, fg=BLACK, bg=DIM_GRAY, content="MEDIUM", fontsize=32) if self.talking_speed_number == 90 else Button(365, 260, 130, 50, fg=BLACK, bg=WHITE, content="MEDIUM", fontsize=32)
        fast = Button(505, 260, 130, 50, fg=BLACK, bg=DIM_GRAY, content="FAST", fontsize=32) if self.talking_speed_number == 60 else Button(505, 260, 130, 50, fg=BLACK, bg=WHITE, content="FAST", fontsize=32)

        # Button
        back = Button(10, WIN_HEIGHT - 60, 200, 50, fg=WHITE, bg=GRAY, content="Back", fontsize=32)

        # Sound
        sound_effects = self.font.render("Sound", True, WHITE)
        sound_effects_rect = sound_effects.get_rect(x=265, y=100)

        # Sound
        talking_speed = self.font.render("Talking speed", True, WHITE)
        talking_speed_rect = sound_effects.get_rect(x=365, y=220)

        # Title
        title = self.settings_font.render("Settings", True, WHITE)
        title_rect = title.get_rect(x=10, y=10)
        
        while opened:
            
            # Music
            if self.music_on and not music_playing: pygame.mixer.Sound.play(self.theme, -1); music_playing = True
            elif not self.music_on and music_playing: pygame.mixer.Sound.stop(self.theme); music_playing = False

            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: quit()
                
                # Esc
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: opened = not opened
                    elif event.key == pygame.K_m:
                        if self.music_on:
                            for _ in range(12):
                                slider.rect.x -= 4
                                slider_inside.rect.x -= 4
                                self._settings_animation(title, title_rect, sound_effects, sound_effects_rect, talking_speed, talking_speed_rect, slider_back, slider, slider_inside, back, slow, medium, fast)
                            self.music_on = not self.music_on
                            slider_inside.rect.x -= 2
                            slider = Button(250, 140, 50, 50, fg=BLACK, bg=RED, content="", fontsize=0)
                        else:
                            for _ in range(12):
                                slider.rect.x += 4
                                slider_inside.rect.x += 4
                                self._settings_animation(title, title_rect, sound_effects, sound_effects_rect, talking_speed, talking_speed_rect, slider_back, slider, slider_inside, back, slow, medium, fast)
                            self.music_on = not self.music_on
                            slider_inside.rect.x += 2
                            slider = Button(300, 140, 50, 50, fg=BLACK, bg=GREEN, content="", fontsize=0)
            # Back button
            if back.is_pressed(mouse_pos, mouse_pressed): opened = not opened
        
            # From on (right) to off (left)
            elif slider.is_pressed(mouse_pos, mouse_pressed) and self.music_on or slider_inside.is_pressed(mouse_pos, mouse_pressed) and self.music_on:
                for _ in range(12):
                    slider.rect.x -= 4
                    slider_inside.rect.x -= 4
                    self._settings_animation(title, title_rect, sound_effects, sound_effects_rect, talking_speed, talking_speed_rect, slider_back, slider, slider_inside, back, slow, medium, fast)
                self.music_on = not self.music_on
                slider_inside.rect.x -= 2
                slider = Button(250, 140, 50, 50, fg=BLACK, bg=RED, content="", fontsize=0)
                
            # From off (left) to on (right)
            elif slider.is_pressed(mouse_pos, mouse_pressed) and not self.music_on or slider_inside.is_pressed(mouse_pos, mouse_pressed) and not self.music_on:
                for _ in range(12):
                    slider.rect.x += 4
                    slider_inside.rect.x += 4
                    self._settings_animation(title, title_rect, sound_effects, sound_effects_rect, talking_speed, talking_speed_rect, slider_back, slider, slider_inside, back, slow, medium, fast)
                self.music_on = not self.music_on
                slider_inside.rect.x += 2
                slider = Button(300, 140, 50, 50, fg=BLACK, bg=GREEN, content="", fontsize=0)

            # Talking speed - Slow
            elif slow.is_pressed(mouse_pos, mouse_pressed):
                self.talking_speed_number = 120
                slow = Button(225, 260, 130, 50, fg=BLACK, bg=DIM_GRAY, content="SLOW", fontsize=32)
                medium = Button(365, 260, 130, 50, fg=BLACK, bg=WHITE, content="MEDIUM", fontsize=32)
                fast = Button(505, 260, 130, 50, fg=BLACK, bg=WHITE, content="FAST", fontsize=32)

            # Talking speed - Medium
            elif medium.is_pressed(mouse_pos, mouse_pressed):
                self.talking_speed_number = 90
                slow = Button(225, 260, 130, 50, fg=BLACK, bg=WHITE, content="SLOW", fontsize=32)
                medium = Button(365, 260, 130, 50, fg=BLACK, bg=DIM_GRAY, content="MEDIUM", fontsize=32)
                fast = Button(505, 260, 130, 50, fg=BLACK, bg=WHITE, content="FAST", fontsize=32)

            # Talking speed - Fast
            elif fast.is_pressed(mouse_pos, mouse_pressed):
                self.talking_speed_number = 60
                slow = Button(225, 260, 130, 50, fg=BLACK, bg=WHITE, content="SLOW", fontsize=32)
                medium = Button(365, 260, 130, 50, fg=BLACK, bg=WHITE, content="MEDIUM", fontsize=32)
                fast = Button(505, 260, 130, 50, fg=BLACK, bg=DIM_GRAY, content="FAST", fontsize=32)
                    
            # Diplaying background, title, buttons
            self._settings_animation(title, title_rect, sound_effects, sound_effects_rect, talking_speed, talking_speed_rect, slider_back, slider, slider_inside, back, slow, medium, fast)

    def _settings_animation(self, title: pygame.Surface, title_rect: pygame.Rect, sound_effects: pygame.Surface, sound_effects_rect: pygame.Rect, talking_speed: pygame.Surface, talking_speed_rect: pygame.Rect, slider_back: Button, slider: Button, slider_inside: Button, back: Button, slow: Button, medium: Button, fast: Button):
        """
        Animation for settings sliders
        """

        self.screen.blit(self.settings_background, (0, 0))
        self.screen.blit(title, title_rect)
        self.screen.blit(sound_effects, sound_effects_rect)
        self.screen.blit(talking_speed, talking_speed_rect)
        self.screen.blit(slider_back.image, slider_back.rect)
        self.screen.blit(slider.image, slider.rect)
        self.screen.blit(slider_inside.image, slider_inside.rect)
        self.screen.blit(slow.image, slow.rect)
        self.screen.blit(medium.image, medium.rect)
        self.screen.blit(fast.image, fast.rect)
        self.screen.blit(back.image, back.rect)
        self.clock.tick(FPS)
        pygame.display.update()

    def door_info(self, msg_content: str, room_number: str):
        """
        Displays info about the room the character is entering/exiting
        """

        for _ in range(45):
            text = self.font.render(msg_content, True, WHITE)
            text_rect = text.get_rect(x=10, y=10)
            self.screen.blit(text, text_rect)
            self.clock.tick(FPS)
            pygame.display.update()
        self.update()
        self.draw()
        self.saved_room_data = room_number
              
    def talking(self, msg_content: str, teacher: bool = False):
        """
        When character is talking
        """

        for _ in range(self.talking_speed_number):
            text = self.font.render(msg_content, True, WHITE) if not teacher else self.font.render(msg_content, True, BRITISH_WHITE)
            text_rect = text.get_rect(x=10, y=10)
            self.screen.blit(text, text_rect)
            self.clock.tick(FPS)
            pygame.display.update()
        self.update()
        self.draw()

    def info(self, msg_content: str, color: tuple[int, int, int] = WHITE, i: int = 10):
        """
        When character is talking but without the update and draw\n
        Good in some situations
        """

        for _ in range(self.talking_speed_number):
            text = self.font.render(msg_content, True, color)
            text_rect = text.get_rect(x=10, y=i)
            self.screen.blit(text, text_rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def trashcan(self):
        """
        Poking around in trashcan
        """

        # In changing room
        if self.interacted[1] == 13 and self.interacted[2] == 165:
            self.talking("There's paper on the side of the trashcan.")
            self.talking("It says 2.SA. You agree with this statement.")

            # Key in trash
            if self.key_in_trash: 
                self.inv["locker key"] = "img/locker key.png"
                self.key_in_trash = False
                self.talking(f"{self.player_name} found a key in the trashcan. It says AR.")

            # Empty trashcan
            else: self.talking("There is nothing interesting.")

        # 201 Trash can
        elif self.interacted[1] == 24 and self.interacted[2] == 43: 

            # Phone in trash
            if self.phone_in_trash:
                pygame.mixer.Sound.play(self.wow_iphone)
                self.talking("Wow, Iphone")
                self.inv['phone'] = "img/Iphone_small.png"
                self.phone_in_trash = False
                pygame.mixer.Sound.stop(self.wow_iphone)

            # Empty
            else: self.talking("Just some rubbish.")

        # 208 Trash can
        elif self.interacted[1] == 24 and self.interacted[2] == 78:
        
            # Kokosky
            if self.kokosky_in_trash:
                self.talking("Why would someone throw away such yummy food.")
                self.number_kokosky += 1
                self.talking(f"{self.player_name} found the forbidden Kokosky fragment. [{self.number_kokosky}/4]")
                self.inv["Kokosky4"] = "img/kokosky4_small.png"
                self.kokosky_in_trash = False

            # Empty
            else: self.talking("There's nothing interesting.")
            
    def window(self):
        """
        Player looks outside of window or falls
        """

        # Window fail ending
        if self.interacted[1] == 27 and self.interacted[2] in (65, 66): pygame.mixer.Sound.play(self.fall); pygame.time.delay(500); self.game_over("img/window_fail.png")

        # Windows between classrooms
        if self.interacted[1] not in (11, 14, 25) and self.interacted[2] not in (98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 110, 111, 112, 113, 173): self.sans() if r.randint(1, 100) == 100 else self.talking("What a pretty day.")

    def sans(self):
        """
        Special window
        """

        if self.music_on: pygame.mixer.Sound.stop(self.theme)
        sans = pygame.mixer.Sound("sounds/sans.mp3")
        pygame.mixer.Sound.play(sans).set_volume(0.1)
        self.talking("It's a beautiful day outside.")
        self.talking("Birds are singing, flowers are blooming...")
        self.talking("On days like these, kids like you...")
        self.talking("SHOULD BE BURNING IN HELL.")
        pygame.mixer.Sound.stop(sans)
        if self.music_on: pygame.mixer.Sound.play(self.theme)

    def center_player_after_doors(self):
        """
        Makes player stand right behind the door they walk through
        """

        # Music
        pygame.mixer.Sound.play(self.door_open)
        pygame.time.delay(500)

        # Facing up
        if self.player.facing == "up":
            self.player.rect.x = self.interacted[3]
            self.player.rect.y = self.interacted[4] - TILE_SIZE
            for sprite in self.all_sprites: sprite.rect.y += 2 * TILE_SIZE
        
        # Facing down
        elif self.player.facing == "down":
            self.player.rect.x = self.interacted[3]
            self.player.rect.y = self.interacted[4] + TILE_SIZE
            for sprite in self.all_sprites: sprite.rect.y -= 2 * TILE_SIZE

        # Facing left
        elif self.player.facing == "left":
            self.player.rect.x = self.interacted[3] - TILE_SIZE
            self.player.rect.y = self.interacted[4]
            for sprite in self.all_sprites: sprite.rect.x += 2 * TILE_SIZE
            
        # Facing right
        elif self.player.facing == "right":
            self.player.rect.x = self.interacted[3] + TILE_SIZE
            self.player.rect.y = self.interacted[4]
            for sprite in self.all_sprites: sprite.rect.x -= 2 * TILE_SIZE
            
    def end(self):
        """
        Canon ending for the game, crashes the program for now
        """

        # Buttons
        exit_button = Button(10, WIN_HEIGHT - 60, 200, 50, WHITE, DARK_GRAY, "Exit the game", 32)
        main_menu_button = Button(10, WIN_HEIGHT - 120, 200, 50, WHITE, DARK_GRAY, "Main menu", 32)

        # Background
        ending_screen = pygame.image.load("img/unofficial_ending.png")


        while True:

            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: quit()
                

            # Background
            self.screen.blit(ending_screen, (0, 0))

            # Exit button
            self.screen.blit(exit_button.image, exit_button.rect)
            if exit_button.is_pressed(mouse_pos, mouse_pressed): self.endings.append("canon_ending") if "canon_ending" not in self.endings else None; self.save_game(); quit()

            # Main menu button
            self.screen.blit(main_menu_button.image, main_menu_button.rect)
            if main_menu_button.is_pressed(mouse_pos, mouse_pressed): self.endings.append("canon_ending") if "canon_ending" not in self.endings else None; self.reseting_game_values(); self.save_game(); pygame.mixer.Sound.stop(self.theme); self.intro_screen().new("old").main()

            # Updates
            self.clock.tick(FPS)
            pygame.display.update()
        
    def ground_floor_doors(self):
        """
        Doors on the ground floor
        """

        # Changing room -> Hall
        if self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 167:

            # Door is locked
            if self.locked_changing_room:

                # Key in inventory
                if "changing_room key" in self.inv:
                    pygame.mixer.Sound.play(self.lock)
                    self.talking(f"{self.player_name} unlocked the door.")
                    self.locked_changing_room = False

                # No key
                else: self.talking(f"{self.player_name} can't find key to unlock the door.")
            
            elif not self.locked_changing_room: self.door_info("Hall", "Hall"); self.center_player_after_doors()
                    
        # Hall -> Changing room
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 167: self.door_info("Changing room", "017"); self.center_player_after_doors()

        # Escape doors
        elif self.player.facing == "down" and self.interacted[1] == 28 and self.interacted[2] in (54, 55):

            # Has everything
            if len(self.grades) == ALL_GRADES: self.talking("This is the end"); self.end()

            # Permission to go home sooner
            elif self.five_min_sooner == self.nepusti == self.gul_quest == False: self.talking("Now I can go home sooner!"); self.game_over("img/early.png")

            # Not yet
            elif len(self.grades) < ALL_GRADES: self.talking("I can't go home yet"); self.talking("I must fulfil what is left")
        
        # Hall -> Buffet Amper
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 176:
            self.talking("Buffet Amper. I like to buy food here.")
            self.talking("Sadly it's closed now.")

        # Hall -> 020
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 166: self.door_info("020 - not a classroom", "020")

        # Hall -> 021
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 159: self.door_info("021 - not a classroom", "021")

        # Hall -> 022
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 152: self.door_info("022 - not a classroom", "022")

        # Hall -> 023
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 133: self.door_info("023 - LIT 3", "023"); self.center_player_after_doors()

        # 023 -> Hall
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 133: self.door_info("Hall", "Hall"); self.center_player_after_doors()
            
        # Hall -> ???
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 123: self.door_info("??? - not a classroom", "???")

                # Hall -> 025
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 96: self.door_info("025 - LCUJ 4", "025"); self.center_player_after_doors()

        # 025 -> Hall 
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 96: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Hall -> 026
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 88: self.door_info("026 - not a classroom")

        # 026 -> Hall
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 88: self.door_info("026 - not a classroom", "026")

        # Hall -> 027
        elif self.player.facing == "right" and self.interacted[1] == 25 and self.interacted[2] == 76: self.door_info("027 - not a classroom", "027")

        # Hall -> 010
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 33: self.door_info("010 - Toilets", "010"); self.center_player_after_doors()

        # 010 -> Hall
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 33: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Toilet room -> Stall
        elif self.player.facing == "up" and self.interacted[1] == 24 and self.interacted[2] in (37, 39): self.talking("PeePeePooPoo time"); self.center_player_after_doors()

        # Stall -> Toilet room
        elif self.player.facing == "down" and self.interacted[1] == 24 and self.interacted[2] in (37, 39): self.talking("Don't forget to wash yo hands"); self.center_player_after_doors()

        # Hall -> 009
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 25: self.door_info("009 - not a classroom", "009")

        # Hall -> 008
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 19: self.door_info("008 - DPXA 3", "008"); self.center_player_after_doors()

        # 008 -> Hall
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 19: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Hall -> 007
        elif self.player.facing == "left" and self.interacted[1] == 17 and self.interacted[2] == 11: self.door_info("007 - LIT 10", "007"); self.center_player_after_doors()

        # 007 -> Hall
        elif self.player.facing == "right" and self.interacted[1] == 17 and self.interacted[2] == 11: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # 007 -> 006
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 9: self.door_info("006 - LIT 9", "006"); self.center_player_after_doors()

        # 006 -> 007
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 9: self.door_info("007 - LIT 10", "007"); self.center_player_after_doors()

        # Hall -> 004
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 20: self.door_info("004 - LIT 8", "004"); self.center_player_after_doors()

        # 004 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 20: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Hall -> 003
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 24: self.door_info("003 - DPXA 2", "003"); self.center_player_after_doors()

        # 003 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 24: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Hall -> 002
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 35: self.door_info("002 - DPXA 1", "002"); self.center_player_after_doors()

        # 002 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 35: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Hall -> 012
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 79: self.door_info("012 - II.A", "012"); self.center_player_after_doors()

        # 012 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 79: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Hall -> 013
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 88: self.door_info("013 - II.B", "013"); self.center_player_after_doors()

        # 013 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 88: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Hall -> 014
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 114: self.door_info("014 - LAELE", "014"); self.center_player_after_doors()
        
        # 014 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 114: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Hall -> 015
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 135: self.door_info("015 - II.C", "015"); self.center_player_after_doors()

        # 015 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 135: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Hall -> 016
        elif self.player.facing == "up" and self.interacted[1] == 14 and self.interacted[2] == 159: self.door_info("016 - II.SA", "016"); self.center_player_after_doors()
                
        # 016 -> Hall
        elif self.player.facing == "down" and self.interacted[1] == 14 and self.interacted[2] == 159: self.door_info("Hall", "Hall"); self.center_player_after_doors()
            
    def first_floor_doors(self):
        """
        Doors on the first floor
        """

        # Hall -> 122/1
        if self.player.facing == "right" and self.interacted[2] == 173 and self.interacted[1] in (12, 13): self.door_info("122/1 -  LIT 1 (III.SA)", "122/1"); self.center_player_after_doors()
        
        # 122/1 -> Hall
        elif self.player.facing == "left" and self.interacted[2] == 173 and self.interacted[1] in (12, 13): self.door_info("Hall", "Hall"); self.center_player_after_doors()
        
        # 122/1 -> 122/2
        elif self.player.facing == "up" and self.interacted[2] == 177 and self.interacted[1] == 8: self.door_info("122/2 -  LIT 2 (IV.SA)", "122/2"); self.center_player_after_doors()
        
        # 122/2 -> 122/1
        elif self.player.facing == "down" and self.interacted[2] == 177 and self.interacted[1] == 8: self.door_info("122/1 -  LIT 1 (III.SA)", "122/1"); self.center_player_after_doors()
            
        # Hall -> Kabinet pri 122/1
        elif self.player.facing == "right" and self.interacted[2] == 173 and self.interacted[1] == 18: self.talking("Cabinet"); self.center_player_after_doors()
            
        # Kabinet pri 122/1 -> Hall
        elif self.player.facing == "left" and self.interacted[2] == 173 and self.interacted[1] == 18: self.door_info("Hall", "Hall"); self.center_player_after_doors()
            
        # 122/2 -> Kabinet HED, MIT
        elif self.player.facing == "left" and self.interacted[2] == 173 and self.interacted[1] == 6: self.talking("Cabinet"); self.center_player_after_doors()
            
        # Kabinet HED, MIT -> 122/2 
        elif self.player.facing == "right" and self.interacted[2] == 173 and self.interacted[1] == 6: self.door_info("122/2 -  LIT 2 (IV.SA)", "122/2"); self.center_player_after_doors()
            
        # Hall -> Kabinet HED, MIT
        elif self.player.facing == "up" and self.interacted[2] == 169 and self.interacted[1] == 7: self.talking("Cabinet"); self.center_player_after_doors()
            
        # Kabinet HED, MIT -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 169 and self.interacted[1] == 7: self.door_info("Hall", "Hall"); self.center_player_after_doors()
            
        # Hall -> Toilets
        elif self.player.facing == "left" and self.interacted[2] == 166 and self.interacted[1] == 12: self.talking("Toilets"); self.center_player_after_doors()
        
        # Toilets -> Stall
        elif self.player.facing == "down" and self.interacted[2] == 161 and self.interacted[1] == 13: self.talking("PeePeePooPoo Time"); self.center_player_after_doors()

        # Stall -> Toilets
        elif self.player.facing == "up" and self.interacted[2] == 161 and self.interacted[1] == 13: self.talking("Don't forget to wash your hands"); self.center_player_after_doors()

        # Toilets -> Hall
        elif self.player.facing == "right" and self.interacted[2] == 166 and self.interacted[1] == 12: self.door_info("Hall", "Hall"); self.center_player_after_doors()
        
        # Hall -> 117
        elif self.player.facing == "up" and self.interacted[2] == 157 and self.interacted[1] == 24: self.door_info("117 - III.B", "117"); self.center_player_after_doors()
        
        # 117 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 157 and self.interacted[1] == 24: self.door_info("Hall", "Hall"); self.center_player_after_doors()
        
        # Hall -> 115
        elif self.player.facing == "up" and self.interacted[2] == 128 and self.interacted[1] == 24: self.door_info("115 - IV.SB", "115"); self.center_player_after_doors()
        
        # 115 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 128 and self.interacted[1] == 24: self.door_info("Hall", "Hall"); self.center_player_after_doors()
        
        # Hall -> 113
        elif self.player.facing == "up" and self.interacted[2] == 93 and self.interacted[1] == 24: self.door_info("113 - III.C", "113"); self.center_player_after_doors()
        
        # 113 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 93 and self.interacted[1] == 24: self.door_info("Hall", "Hall"); self.center_player_after_doors()
        
        # 113 -> Cabinet LIA
        elif self.player.facing == "right" and self.interacted[2] == 97 and self.interacted[1] == 21: self.talking("Cabinet LIA"); self.center_player_after_doors()
        
        # Cabinet LIA -> 113
        elif self.player.facing == "left" and self.interacted[2] == 97 and self.interacted[1] == 21: self.door_info("113 - III.C", "113"); self.center_player_after_doors()
        
        # Hall -> 112
        elif self.player.facing == "up" and self.interacted[2] == 76 and self.interacted[1] == 24: self.door_info("112 - LELM 1", "112"); self.center_player_after_doors()
        
        # 112 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 76 and self.interacted[1] == 24: self.door_info("Hall", "Hall"); self.center_player_after_doors()
        
        # Hall -> 124
        elif self.player.facing == "down" and self.interacted[2] == 160 and self.interacted[1] == 30: self.door_info("124 - LELM 2", "124"); self.center_player_after_doors()
        
        # 124 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 160 and self.interacted[1] == 30: self.door_info("Hall", "Hall"); self.center_player_after_doors()
        
        # Hall -> 126
        elif self.player.facing == "down" and self.interacted[2] == 141 and self.interacted[1] == 30: self.door_info("126 - LSIE 2", "126"); self.center_player_after_doors()
        
        # 126 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 141 and self.interacted[1] == 30: self.door_info("Hall", "Hall"); self.center_player_after_doors() 
        
        # Hall -> 127
        elif self.player.facing == "down" and self.interacted[2] == 126 and self.interacted[1] == 30: self.door_info("127 - LIOT", "127"); self.center_player_after_doors()
        
        # 127 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 126 and self.interacted[1] == 30: self.door_info("Hall", "Hall"); self.center_player_after_doors()  
        
        # Hall -> 130
        elif self.player.facing == "down" and self.interacted[2] == 104 and self.interacted[1] == 30: self.door_info("130 - CZV", "130"); self.center_player_after_doors()
        
        # 130 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 104 and self.interacted[1] == 30: self.door_info("Hall", "Hall"); self.center_player_after_doors()
             
    def second_floor_doors(self): 
        """
        Doors on the second floor
        """

        # Hall -> 203
        if self.player.facing == "left" and self.interacted[2] == 11 and self.interacted[1] == 28: self.door_info("203 - III.A", "203"); self.center_player_after_doors()

        # 203 -> Hall 
        elif self.player.facing == "right" and self.interacted[2] == 11 and self.interacted[1] == 28: self.door_info("Hall", "Hall"); self.center_player_after_doors()
        
        # 203 -> Cabinet
        elif self.player.facing == "up" and self.interacted[1] == 22 and self.interacted[2] == 9: self.door_info("Cabinet", "Cabinet HAR"); self.center_player_after_doors()
        
        # Cabinet -> 203
        elif self.player.facing == "down" and self.interacted[1] == 22 and self.interacted[2] == 9: self.door_info("203 - III.A", "203"); self.center_player_after_doors()
        
        # Hall -> 202
        elif self.player.facing == "up" and self.interacted[2] == 23 and self.interacted[1] == 25: self.door_info("202 - I.SC", "202"); self.center_player_after_doors()

        # 202 -> Hall 
        elif self.player.facing == "down" and self.interacted[2] == 23 and self.interacted[1] == 25: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Hall -> 205
        elif self.player.facing == "down" and self.interacted[2] == 16 and self.interacted[1] == 31: self.door_info("205 - III.A", "205"); self.center_player_after_doors()

        # 205 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 16 and self.interacted[1] == 31: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Hall -> 201
        elif self.player.facing == "up" and self.interacted[2] == 41 and self.interacted[1] == 25: self.door_info("201 - Goated place", "201"); self.center_player_after_doors()

        # 201 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 41 and self.interacted[1] == 25: self.door_info("Hall", "Hall"); self.center_player_after_doors()
    
        # Hall -> Toilets
        elif self.player.facing == "down" and self.interacted[2] == 40 and self.interacted[1] == 31: self.door_info("Toilets", "Toilets_1"); self.center_player_after_doors()

        # Toilets -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 40 and self.interacted[1] == 31: self.door_info("Hall", "Hall"); self.center_player_after_doors()
        
        # Toilets -> Stall
        elif self.player.facing == "up" and self.interacted[2] in (42, 44) and self.interacted[1] == 34: self.talking("Stall"); self.center_player_after_doors()

        # Stall -> Toilets
        elif self.player.facing == "down" and self.interacted[2] in (42, 44) and self.interacted[1] == 34: self.talking("Don't forget to wash yo hands"); self.center_player_after_doors()
            
        # Hall -> 208
        elif self.player.facing == "up" and self.interacted[2] == 76 and self.interacted[1] == 25: self.door_info("208 - I.A", "208"); self.center_player_after_doors()
            
        # 208 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 76 and self.interacted[1] == 25: self.door_info("Hall", "Hall"); self.center_player_after_doors()
            
        # Hall -> 209
        elif self.player.facing == "up" and self.interacted[2] == 93 and self.interacted[1] == 25: self.door_info("209 - I.B", "209"); self.center_player_after_doors()

        # Hall -> 218
        elif self.player.facing == "down" and self.interacted[2] == 158 and self.interacted[1] == 31: self.door_info("218 - I.SB", "218"); self.center_player_after_doors()
        
        # 218 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 158 and self.interacted[1] == 31: self.door_info("Hall", "Hall"); self.center_player_after_doors()
        
        # 209 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 93 and self.interacted[1] == 25: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Hall -> 299
        elif self.player.facing == "up" and self.interacted[2] in (108, 109) and self.interacted[1] == 25: self.door_info("299 - LRIS", "299"); self.center_player_after_doors()

        # 299 -> Hall
        elif self.player.facing == "down" and self.interacted[2] in (108, 109) and self.interacted[1] == 25: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Hall -> 210
        elif self.player.facing == "up" and self.interacted[2] == 128 and self.interacted[1] == 25: self.door_info("210 - III.SB", "210"); self.center_player_after_doors()
            
        # 210 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 128 and self.interacted[1] == 25: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Hall -> 211
        elif self.player.facing == "up" and self.interacted[2] == 138 and self.interacted[1] == 25: self.door_info("211 - Coming soon", "211")

        # 211 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 138 and self.interacted[1] == 25: self.door_info("Hall", "Hall")

        # Hall -> 212
        elif self.player.facing == "up" and self.interacted[2] == 157 and self.interacted[1] == 25: self.door_info("212 - IV.A", "212"); self.center_player_after_doors()

        # 212 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 157 and self.interacted[1] == 25: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Hall -> Toilets
        elif self.player.facing == "left" and self.interacted[2] == 166 and self.interacted[1] == 16: self.talking("Toilets"); self.center_player_after_doors()

        # Toilets -> Hall
        elif self.player.facing == "right" and self.interacted[2] == 166 and self.interacted[1] == 16: self.door_info("Hall", "Hall"); self.center_player_after_doors()
        
        # Toilets -> Stall
        elif self.player.facing == "down" and self.interacted[2] == 161 and self.interacted[1] == 16: self.talking("Stall"); self.center_player_after_doors()

        # Stall -> Toilets
        elif self.player.facing == "up" and self.interacted[2] == 161 and self.interacted[1] == 16: self.talking("Don't forget to wash yo hands"); self.center_player_after_doors()

        # Hall -> 216
        elif self.player.facing == "up" and self.interacted[2] == 169 and self.interacted[1] == 14: self.door_info("216 - OUF (IV.C)", "216"); self.center_player_after_doors()
            
        # 216 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 169 and self.interacted[1] == 14: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Hall -> 217
        elif self.player.facing == "right" and self.interacted[2] == 173 and self.interacted[1] == 19: self.door_info("217 - Cabinet", "217"); self.center_player_after_doors()

        # 217 -> Hall
        elif self.player.facing == "left" and self.interacted[2] == 173 and self.interacted[1] == 19: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # 218 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 141 and self.interacted[1] == 31: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Hall -> 219
        elif self.player.facing == "down" and self.interacted[2] == 117 and self.interacted[1] == 31: self.door_info("219 - I.SA", "219"); self.center_player_after_doors()

        # 219 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 117 and self.interacted[1] == 31: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Hall -> 220
        elif self.player.facing == "down" and self.interacted[2] == 139 and self.interacted[1] == 31: self.door_info("220 - I.C", "220"); self.center_player_after_doors()

        # 220 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 139 and self.interacted[1] == 31: self.door_info("Hall", "Hall"); self.center_player_after_doors()
        
    def third_floor_doors(self):
        """
        Doors on the third floor
        """

        # Hall -> Gym changing rooms
        if self.player.facing in ("up", "left") and self.interacted[2] == 63 and self.interacted[1] == 8: self.door_info("Gym - Changing rooms", "Gym - chr"); self.center_player_after_doors()

        # Gym changing rooms -> Hall
        elif self.player.facing in ("down", "right") and self.interacted[2] == 63 and self.interacted[1] == 8: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Gym changing rooms -> Toielet
        elif self.player.facing == "left" and self.interacted[2] == 57 and self.interacted[1] == 7: self.door_info("Toilets", "Toilets"); self.center_player_after_doors()

        # Toilet -> Gym changing rooms
        elif self.player.facing == "right" and self.interacted[2] == 57 and self.interacted[1] == 7: self.door_info("Gym - Changing rooms", "Gym - chr"); self.center_player_after_doors()
        
        # Gym changing rooms -> Gym
        elif self.player.facing == "left" and self.interacted[2] == 54 and self.interacted[1] == 5: self.door_info("302 - Gym", "302"); self.center_player_after_doors()

        # Gym -> Gym changing rooms
        elif self.player.facing == "right" and self.interacted[2] == 54 and self.interacted[1] == 5: self.door_info("Gym - Changing rooms", "Gym - chr"); self.center_player_after_doors()

        # Gym -> Gymnasium
        elif self.player.facing == "down" and self.interacted[2] in (16, 17) and self.interacted[1] == 6: self.door_info("304 - Gymnasium", "304"); self.center_player_after_doors()

        # Gymnasium -> Gym
        elif self.player.facing == "up" and self.interacted[2] in (16, 17) and self.interacted[1] == 6: self.door_info("302 - Gym", "302"); self.center_player_after_doors()
        
        # Hall -> 304
        elif self.player.facing == "left" and self.interacted[2] == 54 and self.interacted[1] in (11, 12): self.door_info("304 - Gymnasium", "304"); self.center_player_after_doors()
        
        # 304 -> Hall
        elif self.player.facing == "right" and self.interacted[2] == 54 and self.interacted[1] in (11, 12): self.door_info("Hall", "Hall"); self.center_player_after_doors()
        
        # Hall -> Gymnasium changing room
        elif self.player.facing == "down" and self.interacted[2] == 67 and self.interacted[1] == 18: self.door_info("Gymnasium - Changing rooms", "Gymnasium - chr"); self.center_player_after_doors()
        
        # Gymnasium changing room -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 67 and self.interacted[1] == 18: self.door_info("Hall", "Hall"); self.center_player_after_doors()
        
        # Gymnasium changing room -> Gymnasium
        elif self.player.facing == "left" and self.interacted[2] == 54 and self.interacted[1] == 25: self.door_info("304 - Gymnasium", "304"); self.center_player_after_doors()
        
        # Gymnasium -> Gymnasium changing room
        elif self.player.facing == "right" and self.interacted[2] == 54 and self.interacted[1] == 25: self.door_info("Gymnasium - Changing rooms", "Gymnasium - chr"); self.center_player_after_doors()

        # Gymnasium changing room -> Showers
        elif self.player.facing == "right" and self.interacted[2] == 72 and self.interacted[1] == 25: self.door_info("Showers", "Showers"); self.center_player_after_doors()

        # Showers -> Gymnasium changing room
        elif self.player.facing == "left" and self.interacted[2] == 72 and self.interacted[1] == 25: self.door_info("Gymnasium - Changing room", "Gymnasium - chr"); self.center_player_after_doors()

        # Hall -> Cabinet
        elif self.player.facing == "right" and self.interacted[2] == 70 and self.interacted[1] == 6: self.door_info("Cabinet", "Tsv - Cabinet"); self.center_player_after_doors()
        
        # Cabinet -> Hall
        elif self.player.facing == "left" and self.interacted[2] == 70 and self.interacted[1] == 6: self.door_info("Hall", "Hall"); self.center_player_after_doors()
        
    def fourth_floor_doors(self):
        """
        Doors on the fourth floor
        """
        
        # Hall -> LSIE
        if self.player.facing == "down" and self.interacted[2] == 62 and self.interacted[1] == 17: self.door_info("403 - LSIE", "403"); self.center_player_after_doors()
        
        # LSIE -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 62 and self.interacted[1] == 17: self.door_info("Hall", "Hall"); self.center_player_after_doors()
        
        # Hall -> LROB (predsien)
        elif self.player.facing in ("up", "left") and self.interacted[2] == 63 and self.interacted[1] == 8: self.door_info("402 - LROB hallway", "402 - hallway"); self.center_player_after_doors()

        # LROB (predsien) -> Hall
        elif self.player.facing in ("down", "right") and self.interacted[2] == 63 and self.interacted[1] == 8: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # LROB (predsien) -> LROB
        elif self.player.facing == "left" and self.interacted[2] == 54 and self.interacted[1] == 5: self.door_info("402 - LROB", "402"); self.center_player_after_doors()

        # LROB -> LROB (predsien)
        elif self.player.facing == "right" and self.interacted[2] == 54 and self.interacted[1] == 5: self.door_info("402 - LROB hallway", "402 - hallway"); self.center_player_after_doors()

    def talking_with_teachers(self):
        """
        Player chatting with a teacher
        """
        
        if self.interacted[0] == "Teacher":

            # Liascinska
            if self.interacted[2] == 100 and self.interacted[1] == 19: 
                self.talking("LIA is just standing here")
                self.talking("MENACINGLY")
                
            # Gulbaga
            elif self.interacted[2] == 57 and self.interacted[1] == 22:
                
                # Sooner
                if self.gul_quest:

                    # Not annoyed enough
                    if self.__gul_counter != 3:
                        self.talking("Mr. GUL, can I go home early?")
                        self.talking("You think I can manage that?", True)
                        self.talking("I was just thinking...")
                        self.talking("Maybe another time.", True)
                        self.__gul_counter += 1
                    
                    # Annoyed
                    else:
                        self.talking("Mr. GUL, can I go home early?")
                        self.talking("You think I can manage that?", True)
                        self.talking("I was just thinking...")
                        self.talking("You've annoyed me this much...", True)
                        self.talking("I guess you can", True)
                        self.gul_quest = False

                # WoT
                else: self.talking("You wanna play some WoT with me?", True)
            
            # Gonevalova
            if "DEJ" not in list(self.inv.keys()):
                if self.interacted[2] == 155 and self.interacted[1] == 37:
                    if "chalks" not in list(self.inv.keys()): 
                        self.talking("Can you bring me chalks for the next lesson?", True)
                        self.talking("Thanks in advance", True)
                        self.talking("They should be in the first floor cabinet", True)
                        self.talking("On the right that is...", True)
                    else:
                        self.talking("Thank you {}".format(self.player_name), True)
                        self.talking("I can give you any grade", True)
                        self.talking("Since I teach history...", True)
                        self.info("You've recieved a grade for history")
                        self.grades["DEJ"] = 1
                        self.inv.pop("chalks")
                        
            # Guydosova
            if self.interacted[2] == 94 and self.interacted[1] == 24 and "ANJ" not in list(self.grades.keys()):
                self.talking(f"{self.player_name} I've got the test you didn't attend", True)
                anj_values = self.quest.anglictina()
                if isinstance(anj_values, tuple): self.grades["ANJ"], self.anj_test = anj_values[0], anj_values[1]

            # Koky
            if self.interacted[2] == 111 and self.interacted[1] == 9:

                if self.five_min_sooner:
                    self.talking("Can you let us go 5 minutes sooner?")
                    self.talking("No, I can't do that.", True)
                    self.talking("But I will let you go 10 minutes sooner.", True)
                    self.five_min_sooner = False
                
                elif not self.five_min_sooner: self.talking("What are you still doing here?", True)

            # Michal (Ne)pusti
            if self.interacted[2] == 188 and self.interacted[1] == 13:

                # Already talked
                if not self.nepusti: self.talking("Would you like to learn more about Sie?", True)

                # Not yet done
                elif self.nepusti: 
                    
                    # Not completed misson
                    if self.connected_router != list and SaveProgress.get_amount_of_quests(self.player_name) >= 6:
                        self.talking("Hello, could you please let me go home earlier?")
                        self.talking("I'm sorry but I don't think I can do that.", True)
                        self.talking("Are you sure? Maybe I can help you somehow.")
                        self.talking("Well there is something you can do.", True)
                        self.talking("Connect all the routers please.", True)
                        self.talking("If you do that I will let you go home earlier.", True)
                        self.connected_router = []

                    elif type(self.connected_router) == list:

                        if len(self.connected_router) != 4: self.talking("Thank you for helping me.", True)

                        # 023 missing
                        if "023" not in self.connected_router: self.talking("One of them is in 023.", True)

                        # 130 missing
                        elif "130" not in self.connected_router: self.talking("You are doing great. Next one is in 130.", True)

                        # Cabinet missing
                        elif "217" not in self.connected_router: self.talking("Next one should be in the cabinet near this room.", True)
                        
                        # 402 missing
                        elif "402" not in self.connected_router: self.talking("One of them should be somewhere on the fourth floor.", True)

                        # Completed mission
                        elif len(self.connected_router) == 4:
                            self.talking("I'm back. I connected all of them.")
                            self.talking("You really did it. Thank you for helping me.", True)
                            self.talking("I guess you can go home earlier today", True)
                            self.talking("Thank you very much.")
                            self.connected_router = False
                            self.nepusti = False
                            self.grades["SIE"] = 1
                            self.info("You've recieved a grade for SIE")
                
                    else: 
                        self.talking("Sorry, I don't see the results", True)
                        self.talking("From other lessons", True)
                        self.talking("Come back when you're a bit...", True)
                        self.talking("Richer", True)
                                    
    def shoes_on(self):
        """
        Checks if player has shoes on
        """

        if self.locker_stuff["crocs"] and self.caught >= 3: self.game_over("img/you_never_learn.png")
        elif self.locker_stuff["crocs"] and self.caught < 3: 
            self.caught += 1
            self.game_over("img/caught.png")
               
    def locker(self):
        """
        Unlocking the locker
        """

        # Locker with key
        if self.interacted[1] == 9 and self.interacted[2] == 171:

            # Locked
            if self.locked_locker:

                # Has key
                if "locker key" in self.inv:
                    pygame.mixer.Sound.play(self.lock)
                    self.talking(f"{self.player_name} unlocked the locker.")
                    self.locked_locker = False

                # No key
                else: self.talking("Locked locker.")

            # Unlocked
            else: self.in_locker()
            
        elif self.interacted[2] == 191 and self.interacted[1] == 17: 
            self.inv["chalks"] = "img/chalks_small.png"
            self.info("You should have chalks in your pocket")

        # Locker with kokosky
        elif self.interacted[1] == 4 and self.interacted[2] == 165:

            # Locker full
            if self.kokosky_in_locker:
                self.talking("Hmm? Why is it unlocked?")
                self.talking("Wow, what is this?")
                self.number_kokosky += 1
                self.talking(f"{self.player_name} found the forbidden Kokosky fragment. [{self.number_kokosky}/4]")
                self.kokosky_in_locker = False
                self.inv["Kokosky1"] = "img/kokosky1_small.png"

            # Locker empty
            else: self.talking("It's empty, but smells.")

        # Other
        else: 
            
            # Key in inventory
            if "locker key" in self.inv and self.locked_locker: self.talking("Wrong locker.")
            
            # No key
            else: self.talking("Locked locker.")

    def in_locker(self):
        """
        Player is looking in locker
        """

        looking = True

        # Images
        locker = pygame.image.load("img/in_locker.png")
        crocs = pygame.image.load("img/crocs.png")
        crocs_rect = crocs.get_rect(x=195, y=232)
        boots = pygame.image.load("img/boots.png")
        boots_rect = boots.get_rect(x=196, y=229)
        key = pygame.image.load("img/changing_room key.png")
        key_rect = key.get_rect(x=185, y=155)

        # Button
        back_button = Button(500, 400, 120, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)
        
        while looking:
    
            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            # Background
            self.screen.blit(locker, (0, 0))

            # Crocs/Boots
            if self.locker_stuff["crocs"]: self.screen.blit(crocs, crocs_rect)
            else: self.screen.blit(boots, boots_rect)

            # Key
            if self.locker_stuff["key"]: self.screen.blit(key, key_rect)
            
            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: quit()

                # Clicking
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Key
                    if key_rect.collidepoint(event.pos): 
                        self.locker_stuff['key'] = False
                        self.inv["changing_room key"] = "img/changing_room key.png"
                    
                    # Boots
                    elif boots_rect.collidepoint(event.pos) and self.locker_stuff["boots"]: 
                        self.locker_stuff['boots'] = not self.locker_stuff['boots']
                        self.locker_stuff['crocs'] = not self.locker_stuff['crocs']
                    
                    # Crocs
                    elif crocs_rect.collidepoint(event.pos) and self.locker_stuff['crocs']:
                        self.locker_stuff['crocs'] = not self.locker_stuff['crocs']
                        self.locker_stuff['boots'] = not self.locker_stuff['boots']

                # Esc
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: looking = False

            # Button
            self.screen.blit(back_button.image, back_button.rect)
            if back_button.is_pressed(mouse_pos, mouse_pressed): looking = False
            self.clock.tick(FPS)
            pygame.display.update()
            
    def bench(self):
        """
        Sitting on the bench
        """

        if self.interacted[0] == "Bench" and self.player.facing in ("right", "left") or self.interacted[0] == "BencH" and self.player.facing in ("up", "down"):

            # Kokosky
            if self.interacted[3] == 4 and self.interacted[4] == 63 and self.kokosky_under_bench: 
                self.talking("It seems someone forgot this here.")
                self.number_kokosky += 1
                self.talking(f"{self.player_name} found the forbidden Kokosky fragment. [{self.number_kokosky}/4]")
                self.inv["Kokosky3"] = "img/kokosky3_small.png"
                self.kokosky_under_bench = False

            # Sitting is fun
            else:
                self.player.sit(True, self.interacted[1], self.interacted[2])
                self.update()
                self.draw()
                self.talking("You sit on a bench.")
                self.talking("Sitting is really interesting.")
                self.talking("You enjoyed this sitting session.")
                self.talking("But now it's time to continue your journey.")
                self.player.sit(False, self.interacted[1], self.interacted[2])
            
    def taburetka(self):
        """
        Sitting on a taburetka
        """

        if self.interacted[0] == "Taburetka" and self.player.facing in ("right", "left", "up", "down"):
            self.player.sit(True, self.interacted[1], self.interacted[2])
            self.update()
            self.draw()
            self.talking("You're sitting on a soft taburetka.")
            self.talking("Sitting is really interesting.")
            self.talking("You enjoyed this sitting session.")
            self.talking("But now it's time to continue your journey.")
            self.player.sit(False, self.interacted[1], self.interacted[2])
            
    def green_chair(self):
        """
        Sitting on a green chair
        """

        if self.interacted[0] == "Green_chair" and self.player.facing in ("right", "left", "up", "down"):
            self.player.sit(True, self.interacted[1], self.interacted[2])
            self.update()
            self.draw()
            self.talking("You're sitting on a green chair.")
            self.talking("Sitting is really interesting.")
            self.talking("You enjoyed this sitting session.")
            self.talking("But now it's time to continue your journey.")
            self.player.sit(False, self.interacted[1], self.interacted[2])

    def door(self):
        """
        Unlocking/going through door
        """

        # Ground floor
        if self.in_room == ground_floor: self.ground_floor_doors()

        # First floor
        elif self.in_room == first_floor: self.first_floor_doors()

        # Second floor
        elif self.in_room == second_floor: self.second_floor_doors()  
        
        # Third floor
        elif self.in_room == third_floor: self.third_floor_doors()
        
        # Third floor
        elif self.in_room == fourth_floor: self.fourth_floor_doors()
               
    def basement(self):
        """
        Going into the basement
        """
        
        # Light in inventory
        if "light" in self.inv:

            # From right
            if self.interacted[1] == 17 and self.interacted[2] in (193, 194):
                self.talking("I got light with me.")
                self.talking("I'll be able to see now.")
                self.in_room = self.rooms[BASEMENT_FLOOR] # Basement
                self.create_tile_map()
                for sprite in self.all_sprites: sprite.rect.x -= 79 * TILE_SIZE

            # From left
            elif self.interacted[1] in (26, 27) and self.interacted[2] == 117:
                self.talking("I got light with me.")
                self.talking("I'll be able to see now.")
                self.in_room = self.rooms[BASEMENT_FLOOR] # Basement
                self.create_tile_map()
                for sprite in self.all_sprites: sprite.rect.x += 9 * TILE_SIZE; sprite.rect.y -= 3 * TILE_SIZE
                self.player.rect.x -= 87 * TILE_SIZE
                self.player.rect.y += 3 * TILE_SIZE

        # No light
        else:

            if self.without_light <= 3:
                self.talking("No way I am going down there without light.")
                self.talking("I don't want to get lost in school.")
                self.talking("I'll go there when I have some light with me.")
                self.without_light += 1
            else:
                self.talking("Welp, you really want me to go down there?")
                self.talking("Let's see.")
                self.game_over("img/lost.png")

    def bookshelf(self):
        """
        Searching bookshelfs
        """

        self.talking("There is a lot of books.")
        if self.interacted[1] in (34, 35, 36) and self.interacted[2] == 85: self.otec_iot()
        if self.interacted[1] == 32 and self.interacted[2] == 100 and self.kokosky_in_bookshelf: self.talking("Why is this between the books?"); self.number_kokosky += 1; self.talking(f"{self.player_name} found the forbidden Kokosky fragment. [{self.number_kokosky}/4]"); self.inv["Kokosky2"] = "img/kokosky2_small.png"; self.kokosky_in_bookshelf = False

    def otec_iot(self):
        """
        Looking at boot: Otec_IoT
        """

        self.talking("Huh what is this?")

        looking = True

        # Background
        bg = pygame.image.load("img/otec_iot.png")

        # Button
        back_button = Button(500, 400, 120, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)

        self.talking("It's a book from Honoré de Balzac.")
        self.talking("Otec Goriot but the Gor is badly crossed out.")

        while looking:
            
            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: quit()

                # Esc
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: looking = False

            # Background
            self.screen.blit(bg, (0, 0))

            # Button
            self.screen.blit(back_button.image, back_button.rect)
            if back_button.is_pressed(mouse_pos, mouse_pressed): looking = False

            # Updates
            self.clock.tick(FPS)
            pygame.display.update()
            
    def grade_program(self, text_def: str, text_self: str, text_item: str, text_even: str, text_tuple: str):
        """
        Grading player responses in PRO quiz
        """

        grade: int = 5 - len(tuple(i for i in zip(("def", "self", "item", "2 == 0", "tuple"), (text_def, text_self, text_item, text_even, text_tuple)) if i[0] == i[1]))
        return grade if grade != 0 else 1

    def desk(self):
        """
        Searching desk (some desks are special)
        """
        
        if self.interacted[1] == 11 and self.interacted[2] == 3: self.iot_safe()

    def iot_safe(self):
        """
        IoT safe
        """

        looking = True

        # Background
        bg = pygame.image.load("img/iot_safe_closed.png")
        self.talking("A safe?")

        # Button
        back_button = Button(500, 400, 120, 50, fg=WHITE, bg=BLACK, content="Back", fontsize=32)

        # Note
        note = pygame.image.load("img/safe_note.png")
        note_rect = note.get_rect(x=400, y=3)

        # Number buttons
        one = pygame.image.load("img/b_one.png")
        one_rect = one.get_rect(x=200, y=130)
        two = pygame.image.load("img/b_two.png")
        two_rect = two.get_rect(x=280, y=130)
        three = pygame.image.load("img/b_three.png")
        three_rect = three.get_rect(x=360, y=130)

        four = pygame.image.load("img/b_four.png")
        four_rect = four.get_rect(x=200, y=210)
        five = pygame.image.load("img/b_five.png")
        five_rect = five.get_rect(x=280, y=210)
        six = pygame.image.load("img/b_six.png")
        six_rect = six.get_rect(x=360, y=210)

        seven = pygame.image.load("img/b_seven.png")
        seven_rect = seven.get_rect(x=200, y=290)
        eight = pygame.image.load("img/b_eight.png")
        eight_rect = eight.get_rect(x=280, y=290)
        nine = pygame.image.load("img/b_nine.png")
        nine_rect = nine.get_rect(x=360, y=290)

        enter = pygame.image.load("img/b_enter.png")
        enter_rect = enter.get_rect(x=200, y=370)
        zero = pygame.image.load("img/b_zero.png")
        zero_rect = zero.get_rect(x=280, y=370)
        back = pygame.image.load("img/b_back.png")
        back_rect = back.get_rect(x=360, y=370)

        # Input rectangle
        code_input = pygame.Rect(245, 60, 150, 32)

        # Code
        code = ""

        while looking:

            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: self.exiting()

                # Clicking
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Button
                    if note_rect.collidepoint(event.pos): self.info("Note. Maybe a hint to the code.") # to the code OR for the code OR something different? IDK
                    elif one_rect.collidepoint(event.pos) and len(code) <= 10: code += "1"
                    elif two_rect.collidepoint(event.pos) and len(code) <= 10: code += "2"
                    elif three_rect.collidepoint(event.pos) and len(code) <= 10: code += "3"
                    elif four_rect.collidepoint(event.pos) and len(code) <= 10: code += "4"
                    elif five_rect.collidepoint(event.pos) and len(code) <= 10: code += "5"
                    elif six_rect.collidepoint(event.pos) and len(code) <= 10: code += "6"
                    elif seven_rect.collidepoint(event.pos) and len(code) <= 10: code += "7"
                    elif eight_rect.collidepoint(event.pos) and len(code) <= 10: code += "8"
                    elif nine_rect.collidepoint(event.pos) and len(code) <= 10: code += "9"
                    elif enter_rect.collidepoint(event.pos):
                        if self.vtipnicek:
                            if code == "3906241": self.open_iot_safe()
                            else: code = ""
                        else: self.info("I already have vtipnicek.")
                    elif zero_rect.collidepoint(event.pos) and len(code) <= 10: code += "0"
                    elif back_rect.collidepoint(event.pos): code = code[:-1]

                # Esc
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: looking = False

            if back_button.is_pressed(mouse_pos, mouse_pressed): looking = False

            # Background
            self.screen.blit(bg, (0, 0))

            # Input rectangle
            pygame.draw.rect(self.screen, BLACK, code_input)

            # Input Text
            text_surface = self.font.render(code, True, GREEN)
            self.screen.blit(text_surface, (code_input.x+5, code_input.y+5))

            # Buttons
            self.screen.blit(back_button.image, back_button.rect)
            self.screen.blit(one, one_rect)
            self.screen.blit(two, two_rect)
            self.screen.blit(three, three_rect)
            self.screen.blit(four, four_rect)
            self.screen.blit(five, five_rect)
            self.screen.blit(six, six_rect)
            self.screen.blit(seven, seven_rect)
            self.screen.blit(eight, eight_rect)
            self.screen.blit(nine, nine_rect)
            self.screen.blit(enter, enter_rect)
            self.screen.blit(zero, zero_rect)
            self.screen.blit(back, back_rect)
            self.screen.blit(note, note_rect)

            # Updates
            self.clock.tick(FPS)
            pygame.display.update()

    def open_iot_safe(self):
        """
        Inside IoT safe
        """

        searching = True

        # Background
        bg = pygame.image.load("img/iot_safe_opened.png")
        # vtipnicek
        vtipnicek = pygame.image.load("img/vtipnicek.png")
        vtipnicek_rect = vtipnicek.get_rect(x=193, y=75)

        # Button
        back_button = Button(10, 400, 120, 50, fg=WHITE, bg=BLACK, content="Close", fontsize=32)

        while searching:

            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: self.exiting()

                # Click on vtipnicek
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if vtipnicek_rect.collidepoint(event.pos): self.inv["vtipnicek"] = "img/vtipnicek_small.png"; self.vtipnicek = False

                # Esc
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: searching = False

            # Back button
            if back_button.is_pressed(mouse_pos, mouse_pressed): searching = False

            # Background
            self.screen.blit(bg, (0, 0))

            self.screen.blit(back_button.image, back_button.rect)
            if self.vtipnicek: self.screen.blit(vtipnicek, vtipnicek_rect)

            # Updates
            self.clock.tick(FPS)
            pygame.display.update()

    def stairs(self):
        """
        Going up/down the stairs \n
        self.interacted[2] = x coordinates\n
        self.interacted[1] = y coordinates
        """

        # Basement
        if self.interacted[0] == "Stairs_up" and self.in_room == basement:

            # From right
            if self.interacted[1] in (5, 6) and self.interacted[2] == 89:
                self.in_room = self.rooms[GROUND_FLOOR] # Ground floor
                self.create_tile_map()
                for sprite in self.all_sprites: 
                    sprite.rect.x -= 185 * TILE_SIZE
                    sprite.rect.y -= 10 * TILE_SIZE
                self.player.rect.x += 25 * TILE_SIZE
                self.player.rect.y += 10 * TILE_SIZE

            # From left
            if self.interacted[1] in (9, 10) and self.interacted[2] == 0:
                self.in_room = self.rooms[GROUND_FLOOR] # Ground floor
                self.create_tile_map()
                for sprite in self.all_sprites: 
                    sprite.rect.x -= 107 * TILE_SIZE
                    sprite.rect.y -= 20 * TILE_SIZE
                self.player.rect.x -= 52 * TILE_SIZE
                self.player.rect.y += 20 * TILE_SIZE

        # Ground floor -> 1st floor
        elif self.interacted[0] == "Stairs_up" and self.in_room == ground_floor:
            self.in_room = self.rooms[FIRST_FLOOR] # First floor
            self.create_tile_map()

            # Right stairs
            if self.interacted[1] in (16, 17, 18, 19) and self.interacted[2] == 184:
                for sprite in self.all_sprites: 
                    sprite.rect.x -= 171 * TILE_SIZE
                    sprite.rect.y -= 17 * TILE_SIZE
            
            # Left stairs
            elif self.interacted[1] == 13 and self.interacted[2] in (45, 46, 47, 48, 49, 50, 51):
                for sprite in self.all_sprites:
                    sprite.rect.x -= 47 * TILE_SIZE
                    sprite.rect.y -= 17 * TILE_SIZE
                self.player.rect.x -= 124 * TILE_SIZE
                self.player.rect.y += 2 * TILE_SIZE
            
            self.door_info("First floor", "Hall")
                
        # 1st floor -> Ground floor
        elif self.interacted[0] == "Stairs_down" and self.in_room == first_floor:
            self.in_room = self.rooms[GROUND_FLOOR] # Ground floor
            self.create_tile_map()

            # Right stairs
            if self.interacted[1] in (21, 22, 23, 24) and self.interacted[2] == 181:
                for sprite in self.all_sprites:
                    sprite.rect.x -= 173 * TILE_SIZE
                    sprite.rect.y -= 11 * TILE_SIZE
                self.player.rect.x += 14 * TILE_SIZE
                self.player.rect.y += 11 * TILE_SIZE

            # Left stairs
            elif self.interacted[1] == 24 and self.interacted[2] in (53, 54, 55, 56, 57, 58, 59):
                for sprite in self.all_sprites:
                    sprite.rect.x -= 39 * TILE_SIZE
                    sprite.rect.y -= 7 * TILE_SIZE
                self.player.rect.x -= 120 * TILE_SIZE
                self.player.rect.y += 8 * TILE_SIZE
                
            self.door_info("Ground floor", "Hall")
        
        # First floor -> Second floor
        elif self.interacted[0] == "Stairs_up" and self.in_room == first_floor:
            self.in_room = self.rooms[SECOND_FLOOR] # Second floor
            self.create_tile_map()
            
            # Right stairs
            if self.interacted[1] in (26, 27, 28, 29) and self.interacted[2] == 181: 
                for sprite in self.all_sprites:
                    sprite.rect.x -= 171 * TILE_SIZE
                    sprite.rect.y -= 18 * TILE_SIZE
            
            # Left stairs
            elif self.interacted[2] in (45, 46, 47, 48, 49, 50, 51) and self.interacted[1] == 24:
                for sprite in self.all_sprites:
                    sprite.rect.x -= 47 * TILE_SIZE
                    sprite.rect.y -= 19 * TILE_SIZE
                self.player.rect.x -= 124 * TILE_SIZE
                self.player.rect.y += 2 * TILE_SIZE
            
            self.door_info("Second floor", "Hall")
                
        # Second floor -> First floor
        elif self.interacted[0] == "Stairs_down" and self.in_room == second_floor:
            self.in_room = self.rooms[FIRST_FLOOR] # First floor
            self.create_tile_map()

            # Right stairs
            if self.interacted[1] in (22, 23, 24, 25) and self.interacted[2] == 181:
                for sprite in self.all_sprites:
                    sprite.rect.x -= 171 * TILE_SIZE
                    sprite.rect.y -= 19 * TILE_SIZE
                self.player.rect.y += 4 * TILE_SIZE

            # Left stairs
            elif self.interacted[1] == 25 and self.interacted[2] in (53, 54, 55, 56, 57, 58, 59):
                for sprite in self.all_sprites:
                    sprite.rect.x -= 39 * TILE_SIZE
                    sprite.rect.y -= 19 * TILE_SIZE
                self.player.rect.x -= 132 * TILE_SIZE
                self.player.rect.y += 2 * TILE_SIZE
                
            self.door_info("First floor", "Hall")
        
        # Second floor -> Third floor
        elif self.interacted[0] == "Stairs_up" and self.in_room == second_floor:
            self.in_room = self.rooms[THIRD_FLOOR]
            self.create_tile_map()
            
            if self.interacted[1] in (26, 27, 28, 29) and self.interacted[2] == 181: 
                for sprite in self.all_sprites:
                    sprite.rect.x -= 62 * TILE_SIZE
                    sprite.rect.y -= 4 * TILE_SIZE

            self.door_info("Third floor", "Hall")
            
        # Third floor -> Second floor
        elif self.interacted[0] == "Stairs_down" and self.in_room == third_floor:
            self.in_room = self.rooms[SECOND_FLOOR]
            self.create_tile_map()
            
            if self.interacted[1] in (8, 9, 10, 11) and self.interacted[2] == 72:
                for sprite in self.all_sprites:
                    sprite.rect.x -= 171 * TILE_SIZE
                    sprite.rect.y -= 20 * TILE_SIZE
                self.player.rect.y += 4 * TILE_SIZE
                    
            self.door_info("Second floor", "Hall")
            
        # Fourth floor -> Third floor
        elif self.interacted[0] == "Stairs_down" and self.in_room == fourth_floor:
            self.in_room = self.rooms[THIRD_FLOOR]
            self.create_tile_map()
            
            if self.interacted[1] in (8, 9, 10, 11) and self.interacted[2] == 72:
                for sprite in self.all_sprites:
                    sprite.rect.x -= 62 * TILE_SIZE
                    sprite.rect.y -= 7 * TILE_SIZE
                self.player.rect.y += 4 * TILE_SIZE
                    
            self.door_info("Third floor", "Hall")
            
        # Third floor -> Fourth floor
        elif self.interacted[0] == "Stairs_up" and self.in_room == third_floor:
            self.in_room = self.rooms[FOURTH_FLOOR]
            self.create_tile_map()
            
            if self.interacted[1] in (13, 14, 15, 16) and self.interacted[2] == 72: 
                for sprite in self.all_sprites:
                    sprite.rect.x -= 62 * TILE_SIZE
                    sprite.rect.y -= 4 * TILE_SIZE

            self.door_info("Fourth floor", "Hall")
                
    def toilet(self):
        """
        PeePeePooPoo time
        """

        self.talking(f"{self.player_name} has PeePeePooPoo time now.")
        

g = Game()
g.intro_screen().new("new").main()
pygame.quit()