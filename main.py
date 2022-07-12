# Imports
import base64
from pickle import FALSE
import sys
from tkinter import messagebox
from types import NoneType
import webbrowser
import pygame, random as r, getpass, requests
from leaderboard import Leaderboard
from quest import Quest
from save_progress import SaveProgress
from camera import Camera
from bs4 import BeautifulSoup as bs

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
        
        # Game version
        web = requests.get('https://aeternix-forum.herokuapp.com/releases/')
        soup = bs(web.text, 'html.parser').find('main').find_next('main').find_next('div').find_next('h1').text.split("v")[-1] if web.status_code != 503 else None
        self.__LOCAL_VERSION__ = float(open('version_info.txt', 'r').read())
        self.__REMOTE_VERSION__ = float(soup) if soup is not None else self.__LOCAL_VERSION__
        
        # Screen, time, font, running
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        '''Main game screen'''
        self.clock = pygame.time.Clock()
        '''FPS shenanigans'''
        self.game_running = True
        '''Ye, it's running alright'''
        self.big_font = pygame.font.Font("Caveat.ttf", 40)
        '''BIIG FOOONT'''
        self.font = pygame.font.Font("Roboto.ttf", 22)
        '''just a normal font'''
        self.settings_font = pygame.font.Font("Caveat.ttf", 45)
        '''Another font, but now usable for settings'''
        self.lrob_font = pygame.font.Font("Roboto.ttf", 13) 
        '''And there was also an OSY font'''

        # Spritesheets
        self.character_spritesheet = Spritesheet("img/character.png")
        self.terrain_spritesheet = Spritesheet("img/terrain.png")
        self.npcs_spritesheet = Spritesheet("img/npc.png")

        # Into and Game Over backgrounds
        self.intro_background = pygame.image.load("img/intro_background.png")
        self.settings_background = pygame.image.load("img/settings_bg.jpg")
        
        # Window icon and title
        icon = pygame.image.load('img/spselogo2.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('SPŠE ADVENTURE - REVENGEANCE')

        self.rooms: List[List[str]] = [ground_floor, first_floor, second_floor, third_floor, fourth_floor, ending_hallway, basement]
        '''Rooms where player can go'''
        self.lyz_rooms: List[List[str]] = [lyz_outside, "lyz_ground", "lyz_first", "lyz_second", lyz_diner]
        '''Rooms where player can go in the Lyziarsky DLC'''
        self.in_room: List[str] = self.rooms[GROUND_FLOOR] 
        '''Floor where player is rn (starting point) that's ground floor for those who don't know'''
        self.saved_room_data: str = "017" 
        '''Room where player is rn (starting point) that's Satna for those who don't know'''
        self.quest = Quest(self)
        '''More complex quests'''
        self.grades: dict[str, int] = {}
        '''Player's grades'''
        self.endings: List[str] = []
        '''Endings that player has already achieved'''
        self.camera = Camera(self)
        '''Camera for the game'''
        self.leaderboarding = Leaderboard(self)
        '''Yes, good name for a specific yet easy to use variable, used only once'''
        
        # Settings
        self.music_on: bool = True
        '''Music on/off'''
        self.talking_speed_number: int = 90
        '''Talking speed for the game'''
        self.reseting_game_values()

        # Player name and password
        self.player_name: str = ""
        self._password: str = ""
        self.bought: bool = True

        # Npc list
        self.npc = []

        # Sounds
        self.wow_iphone = pygame.mixer.Sound("sounds/wow_iphone.mp3")
        self.wow_iphone.set_volume(0.5)
        self.theme = pygame.mixer.Sound("sounds/theme.mp3")
        self.theme.set_volume(0.25)
        self.kacurovanie = pygame.mixer.Sound("sounds/kacurovanie.mp3")
        self.kacurovanie.set_volume(0.05)
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
        self.wrong_house = pygame.mixer.Sound("sounds/wrong_house.mp3")
        self.wrong_house.set_volume(0.5)
        self.guy = pygame.mixer.Sound("sounds/lost_guy.mp3")
        self.guy.set_volume(0.15)
        self.lucky = pygame.mixer.Sound("sounds/lucky.mp3")
        self.lucky.set_volume(0.25)
        self.unlucky = pygame.mixer.Sound("sounds/unlucky.mp3")
        self.unlucky.set_volume(0.1)

        # Lost guy
        self.g_move = False
        self.g_leave = False
        self.player_follow = False
        
        self.show_update()
        
    def __new_version(self): return True if self.__LOCAL_VERSION__ < self.__REMOTE_VERSION__ else False
    
    def show_update(self): 
        if self.__new_version():
            if messagebox.askyesno("New update", "Update the game?"):
                webbrowser.open('https://aeternix-forum.herokuapp.com/releases/')
                sys.exit()
            else: sys.exit()
        
    def encode_password(self, password: str): 
        password = base64.b85encode(password.encode('utf-8')).decode('utf-8')
        return password
    
    def decode_password(self, password: str):
        try:
            password = base64.b85decode(password.encode('utf-8')).decode('utf-8')
            return password
        except UnicodeDecodeError:
            password = self.encode_password(password)
            password = base64.b85decode(password.encode('utf-8')).decode('utf-8')
            return password

    def set_level_camera(self, level: List[str]):
        """
        Moves camera and player to stairs
        """
        
        # Ground floor
        if level == self.rooms[GROUND_FLOOR]:
            for sprite in self.all_sprites:
                sprite.rect.x -= 39 * TILE_SIZE
                sprite.rect.y -= 7 * TILE_SIZE
            self.player.rect.x -= 120 * TILE_SIZE
            self.player.rect.y += 8 * TILE_SIZE
        
        # First floor
        elif level == self.rooms[FIRST_FLOOR]:
            for sprite in self.all_sprites:
                sprite.rect.x -= 47 * TILE_SIZE
                sprite.rect.y -= 17 * TILE_SIZE
            self.player.rect.x -= 124 * TILE_SIZE
            self.player.rect.y += 2 * TILE_SIZE
        
        # Second floor
        elif level == self.rooms[SECOND_FLOOR]:
            for sprite in self.all_sprites:
                sprite.rect.x -= 47 * TILE_SIZE
                sprite.rect.y -= 19 * TILE_SIZE
            self.player.rect.x -= 124 * TILE_SIZE
            self.player.rect.y += 2 * TILE_SIZE
        
        # Third floor
        elif level == self.rooms[THIRD_FLOOR]:
            for sprite in self.all_sprites:
                sprite.rect.x -= 62 * TILE_SIZE
                sprite.rect.y -= 4 * TILE_SIZE
                
        # Fourth floor
        elif level == self.rooms[FOURTH_FLOOR]: 
            for sprite in self.all_sprites:
                sprite.rect.x -= 62 * TILE_SIZE
                sprite.rect.y -= 4 * TILE_SIZE

        # Basement
        elif level == self.rooms[BASEMENT_FLOOR]:
            for sprite in self.all_sprites: sprite.rect.x -= 34 * TILE_SIZE
            self.player.rect.x -= 45 * TILE_SIZE
            
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
        self.amper_locked: bool = True
        self.amper_key_in_trash: bool = True
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
        self.mat_test: bool = True
        self.sjl_test: bool = True
        self.obn_test: bool = True
        self.referat: bool = True
        self.gul_quest: bool = True
        self.nepusti: bool = True
        self.closed_window: bool = True
        self.five_min_sooner: bool = True
        self.resistor: bool = True
        self.osy: bool = True
        self.iot: bool = True
        self.icdl: bool = True
        self.haram_test: bool = True
        self.lost_guy: bool = True
        self.not_saint: bool = True
        self.prayed: bool = False
        self.locker_stuff: dict[str, bool] = {"crocs": True, "boots": False, "key": True}

        # Bananok
        self.number_bananok: int = 0
        self.bananky_in_trash: dict[str, dict[str, int]] = {
            "ground floor": {
                "2113": 2,
                "2313": 3, 
                "3413": 4, 
                "8313": 1, 
                "8513": 5, 
                "10513": 3,
                "14113": 2,
                "16313": 1,
                "2021": 4,
                "3021": 2,
                "9321": 3,
                "12921": 2
            },
            "first floor": {
                "1747": 1,
                "7823": 1,
                "8023": 2,
                "11323": 3,
                "11523": 2,
                "16724": 4,
                "10231": 2,
                "138": 2,
                "7038": 5,
                "15638": 2
            },
            "second floor": {
                "16712": 3,
                "13415": 2,
                "9624": 2,
                "11324": 4,
                "13224": 2,
                "16725": 1,
                "139": 1
            },
            "fourth floor":{
                "557": 2,
                "5516": 2
            }
        }
        self.bananky_on_ground: dict[str, dict[str, bool]] = {
            "ground floor": {
                "11": True,
                "151": True, 
                "161": True, 
                "181": True, 
                "191": True, 
                "211": True, 
                "641": True, 
                "831": True, 
                "851": True, 
                "1031": True,
                "1201": True,
                "1411": True,
                "1431": True,
                "1631": True,
                "12": True,
                "152": True,
                "162": True,
                "182": True,
                "192": True,
                "212": True,
                "642": True,
                "832": True,
                "852": True,
                "1032": True,
                "1202": True,
                "1412": True,
                "1432": True,
                "1632": True,
                "13": True,
                "14": True,
                "15": True,
                "16": True,
                "17": True,
                "18": True,
                "1059": True,
                "1189": True,
                "10510": True,
                "11810": True,
                "2311": True,
                "11811": True,
                "2312": True,
                "4312": True,
                "4313": True,
                "10421": True,
                "14721": True,
                "14821": True,
                "14722": True,
                "14822": True,
                "127": True,
                "227": True,
                "327": True,
                "427": True,
                "527": True,
                "627": True,
                "727": True,
                "827": True,
                "927": True,
                "1027": True,
                "10427": True
            },
            "first floor": {
                "1671": True,
                "1681": True,
                "1691": True,
                "1701": True,
                "1891": True,
                "1901": True,
                "1911": True,
                "1672": True,
                "1682": True,
                "1692": True,
                "1673": True,
                "1683": True,
                "1674": True,
                "1897": True,
                "1907": True,
                "1917": True,
                "1899": True,
                "1909": True,
                "1919": True,
                "7611": True,
                "7711": True,
                "7811": True,
                "9311": True,
                "9411": True,
                "9511": True,
                "9611": True,
                "12811": True,
                "12911": True,
                "13011": True,
                "13111": True,
                "13211": True,
                "15711": True,
                "15811": True,
                "15911": True,
                "7612": True,
                "7712": True,
                "7812": True,
                "9312": True,
                "9412": True,
                "9512": True,
                "9612": True,
                "12812": True,
                "12912": True,
                "13012": True,
                "13112": True,
                "13212": True,
                "15712": True,
                "15812": True,
                "15912": True,
                "18915": True,
                "19015": True,
                "19115": True,
                "18831": True,
                "18931": True,
                "19031": True,
                "19131": True,
                "18832": True,
                "18932": True,
                "19032": True,
                "19132": True,
                "18833": True,
                "18933": True,
                "19033": True,
                "19133": True,
                "10238": True,
                "10338": True,
                "10438": True,
                "10538": True
            },
            "second floor": {
                "1671": True,
                "1681": True,
                "1691": True,
                "1701": True,
                "1711": True,
                "1721": True,
                "1731": True,
                "1741": True,
                "1751": True,
                "1761": True,
                "1771": True,
                "1781": True,
                "1791": True,
                "1801": True,
                "1811": True,
                "1821": True,
                "1831": True,
                "1841": True,
                "1851": True,
                "1861": True,
                "1871": True,
                "1881": True,
                "1891": True,
                "1901": True,
                "1911": True,
                "1893": True,
                "1903": True,
                "1913": True,
                "115": True,
                "215": True,
                "315": True,
                "415": True,
                "515": True,
                "615": True,
                "715": True,
                "815": True,
                "915": True,
                "1015": True,
                "1215": True,
                "2615": True,
                "6115": True,
                "8015": True,
                "8115": True,
                "11515": True,
                "11615": True,
                "14415": True,
                "1216": True,
                "2616": True,
                "6116": True,
                "8016": True,
                "8116": True,
                "11516": True,
                "11616": True,
                "14416": True,
                "1217": True,
                "1218": True,
                "1219": True,
                "2619": True,
                "6119": True,
                "8019": True,
                "8119": True,
                "11519": True,
                "11619": True,
                "14419": True,
                "1220": True,
                "2620": True,
                "6120": True,
                "8020": True,
                "8120": True,
                "11520": True,
                "11620": True,
                "14420": True,
                "1221": True,
                "1222": True,
                "1223": True,
                "2623": True,
                "6123": True,
                "8023": True,
                "8123": True,
                "11523": True,
                "11623": True,
                "14423": True,
                "1224": True,
                "2624": True,
                "6124": True,
                "8024": True,
                "8124": True,
                "11524": True,
                "11624": True,
                "14424": True,
                "125": True,
                "126": True,
                "128": True,
                "129": True,
                "131": True,
                "132": True,
                "12132": True,
                "12232": True,
                "12432": True,
                "12532": True,
                "12732": True,
                "12832": True,
                "13032": True,
                "13132": True,
                "13232": True,
                "14132": True,
                "14232": True,
                "14432": True,
                "14532": True,
                "14732": True,
                "14832": True,
                "15032": True,
                "15132": True,
                "15232": True,
                "14133": True,
                "14233": True,
                "14433": True,
                "14533": True,
                "14733": True,
                "14833": True,
                "15033": True,
                "15133": True,
                "15233": True,
                "134": True,
                "135": True,
                "4735": True,
                "4835": True,
                "5135": True,
                "5235": True,
                "5935": True,
                "6035": True,
                "6235": True,
                "6335": True,
                "4736": True,
                "4836": True,
                "5136": True,
                "5236": True,
                "5936": True,
                "6036": True,
                "6236": True,
                "6336": True,
                "4737": True,
                "4837": True,
                "4937": True,
                "5037": True,
                "5137": True,
                "5237": True,
                "5937": True,
                "6037": True,
                "6137": True,
                "6237": True,
                "6337": True,
                "1238": True,
                "1338": True,
                "13938": True,
                "14038": True,
                "14238": True,
                "14338": True,
                "14538": True,
                "14638": True,
                "14838": True,
                "14938": True,
                "15138": True,
                "15238": True,
                "1239": True,
                "1339": True,
                "12139": True,
                "12239": True,
                "12439": True,
                "12539": True,
                "12739": True,
                "12839": True,
                "13039": True,
                "13139": True,
                "13239": True,
                "13939": True,
                "14039": True,
                "14239": True,
                "14339": True,
                "14539": True,
                "14639": True,
                "14839": True,
                "14939": True,
                "15139": True,
                "15239": True,
                "18239": True,
                "18339": True,
                "18439": True,
                "18539": True,
                "18639": True
            },
            "third floor": {
                "11": True,
                "21": True, 
                "31": True, 
                "41": True, 
                "51": True, 
                "61": True, 
                "71": True, 
                "81": True, 
                "91": True, 
                "101": True,
                "12": True, 
                "22": True, 
                "32": True,
                "42": True,
                "52": True,
                "62": True,
                "72": True,
                "82": True,
                "92": True,
                "102": True,
                "13": True,
                "23": True,
                "33": True,
                "43": True,
                "53": True,
                "63": True,
                "73": True,
                "83": True,
                "93": True,
                "103": True,
                "14": True,
                "24": True,
                "34": True,
                "44": True,
                "54": True,
                "64": True,
                "74": True,
                "84": True,
                "94": True,
                "104": True,
                "15": True,
                "25": True,
                "35": True,
                "45": True,
                "55": True,
                "65": True,
                "75": True,
                "85": True,
                "95": True,
                "105": True,
                "16": True,
                "26": True,
                "36": True,
                "46": True,
                "56": True,
                "66": True,
                "76": True,
                "86": True,
                "96": True,
                "106": True,
                "7318": True,
                "7418": True,
                "7518": True,
                "7618": True,
                "7718": True,
                "7818": True,
                "7918": True,
                "8018": True,
                "8118": True,
                "8218": True
            },
            "fourth floor": {
                "5515": True,
                "6418": True,
                "6518": True,
                "6718": True,
                "6818": True,
                "7018": True,
                "7118": True,
                "7318": True,
                "7418": True,
                "7618": True,
                "7718": True,
                "5526": True,
                "5626": True,
                "5726": True,
                "5826": True,
                "6426": True,
                "6526": True,
                "6726": True,
                "6826": True,
                "7026": True,
                "7126": True,
                "7326": True,
                "7426": True,
                "7626": True,
                "7726": True
            }
        }

        # Amper stuff
        self.amper_stuff = ["level teleporter", "referat", "map", "retake", "vujcheek fender"]

        # Grader
        self.grades: dict[str, int] = {}

    def create_tile_map(self):
        """
        Creates tile map
        """

        self.interactive = {}
        floors = ["ground floor", "first floor", "second floor", "third floor", "fourth floor", "ending hallway", "basement"]

        # Destroying previous sprites
        for sprite in self.all_sprites: sprite.kill()

        # Creating sprites
        for i, row in enumerate(self.in_room):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == '´': Ground(self, j, i, dirt=True)
                if column in ("_", "?"): Blockade(self, j, i, column) # Grass or Black
                elif column == "P": self.player = Player(self, j, i) # Player
                elif column in ("!", "W"): Block(self, j, i, column) # No entry ground
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
                elif column == "ä": self.interactive[Block(self, j, i, "ä")] = "ä" + str(i) + str(j) # Desk + chair + baterries (vertical) right
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
                elif column == "č": self.interactive[Block(self, j, i, "č")] = "č" + str(i) + str(j) # dč as in Red (červena) Taburetka
                elif column == "@": self.interactive[Block(self, j, i, "@")] = "@" + str(i) + str(j) # Up facing green chair
                elif column == "#": self.interactive[Block(self, j, i, "#")] = "#" + str(i) + str(j) # Right facing green chair
                elif column == "*": self.interactive[Block(self, j, i, "*")] = "*" + str(i) + str(j) # Left facing green chair
                elif column == "~": self.interactive[Block(self, j, i, "~")] = "~" + str(i) + str(j) # Coffee machine
                elif column == "&": self.interactive[Block(self, j, i, "&")] = "&" + str(i) + str(j) # Gym machine
                elif column == "0": self.interactive[Block(self, j, i, "0")] = "0" + str(i) + str(j) # Basketball hoop (R)
                elif column == "ô": self.interactive[Block(self, j, i, "ô")] = "ô" + str(i) + str(j) # Basketball hoop (L)
                elif column == "ˇ": self.interactive[Block(self, j, i, "ˇ")] = "ˇ" + str(i) + str(j) # Dumbell rack
                elif column == "Ž": self.interactive[Block(self, j, i, "Ž")] = "Ž" + str(i) + str(j) # Rebrina (idk in english)
                elif column == "A": self.interactive[Block(self, j, i, "A")] = "A" + str(i) + str(j) # Pult in Amper
                elif column == "3": self.interactive[Block(self, j, i, "3")] = "3" + str(i) + str(j) # Pong ping
                elif column == "4": self.interactive[Block(self, j, i, "4")] = "4" + str(i) + str(j) # Pong ping
                elif column == "5": self.interactive[Block(self, j, i, "5")] = "5" + str(i) + str(j) # Pong ping
                elif column == "6": self.interactive[Block(self, j, i, "6")] = "6" + str(i) + str(j) # Pong ping
                elif column == "7": self.interactive[Block(self, j, i, "7")] = "7" + str(i) + str(j) # Pong ping
                elif column == "8": self.interactive[Block(self, j, i, "8")] = "8" + str(i) + str(j) # Pong ping
                elif column == "ď": self.interactive[Block(self, j, i, "ď")] = "ď" + str(i) + str(j) # Laďďer
                elif column == "Ú": self.interactive[Block(self, j, i, "Ú")] = "Ú" + str(i) + str(j) # Sink
                elif column == "Ů": self.interactive[Block(self, j, i, "Ů")] = "Ů" + str(i) + str(j) # Sink
                elif column == "˙": self.interactive[Block(self, j, i, "˙")] = "˙" + str(i) + str(j) # Sink
                elif column == "N": self.interactive[Npc(self, j, i, "")] = "N" + str(i) + str(j) # NPC
                elif column == "K": self.interactive[Npc(self, j, i, "K")] = "K" + str(i) + str(j) # Kacka
                elif column == "9": self.npc.append(Npc(self, j, i, "9"))  # NPC VUJ
                elif column == "C": self.npc.append(Npc(self, j, i, "C")) # Cleaner
                elif column == "p": self.npc.append(Npc(self, j, i, "p")) # People
                elif column == "§" and self.lost_guy: self.npc.append(Npc(self, j, i, "§")) # Lost guy
                elif column == "2" and self.bananky_on_ground[floors[self.rooms.index(self.in_room)]][str(j) + str(i)]: Banana(self, j, i) # Bananok 
                elif column == "ś": self.interactive[Block(self, j, i, "ś")] = "ś" + str(j) + str(i)
                elif column == "š": self.interactive[Block(self, j, i, "š")] = "š" + str(j) + str(i)

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
        self.bananky = pygame.sprite.LayeredUpdates()

        # Loads data
        data: list | dict = SaveProgress.load_data(self.player_name)
        
        # Has profile
        if data is not None and t == "new" and self.continue_game:
            
            # DLCs
            self.bought = data['DLC bought']

            # Level
            self.in_room = self.rooms[data["level"]] if self.rooms[data["level"]] not in ('diner', 'outside') else self.lyz_rooms[data["level"]]
            self.saved_room_data = data['room_number']

            # Inventory
            self.inv = {} if "inventory" not in data.keys() else data["inventory"]

            # Variables for endings
            self.without_light = data["quests"]["without_light"]
            self.caught = data["quests"]["caught"]
            self.endings = [] if "endings" not in data.keys() else data["endings"]
            self._password = data['credentials'] if 'credentials' in data.keys() else ""

            # Variables for finding items/doing stuff
            self.key_in_trash = data["quests"]["key_in_trash"]
            self.locked_locker = data["quests"]["locked_locker"]
            self.locked_changing_room = data["quests"]["locked_changing_room"]
            self.amper_locked = data["quests"]["amper_locked"]
            self.amper_key_in_trash = data["quests"]["amper_key_in_trash"]
            self.number_kokosky = data["quests"]["number_kokosky"]
            self.kokosky_in_locker = data["quests"]["kokosky_in_locker"]
            self.kokosky_in_bookshelf = data["quests"]["kokosky_in_bookshelf"]
            self.kokosky_under_bench = data["quests"]["kokosky_under_bench"]
            self.kokosky_in_trash = data["quests"]["kokosky_in_trash"]
            self.locker_stuff = data["quests"]["locker_stuff"]
            self.vtipnicek = data["quests"]["vtipnicek"]
            self.dumbbell_lifted = data["quests"]["dumbbells"]
            self.program_test = data["quests"]["program"]
            self.suplovanie = data["quests"]['suplovanie'] if 'suplovanie' in data['quests'].keys() else False
            self.phone_in_trash = data["quests"]["phone"]
            self.anj_test = data["quests"]["anj_test"]
            self.mat_test = data["quests"]["mat_test"]
            self.sjl_test = data["quests"]["sjl_test"]
            self.obn_test = data["quests"]["obn_test"]
            self.referat = data["quests"]["referat"]
            self.gul_quest = data["quests"]['GUL_quest']
            self.__gul_counter = data["quests"]["gul_counter"]
            self.nepusti = data["quests"]["nepusti"]
            self.connected_router = data["quests"]["router"]
            self.five_min_sooner = data["quests"]["sooner"]
            self.resistor = data["quests"]["resistor"]
            self.osy = data["quests"]["osy"]
            self.iot = data["quests"]["iot"]
            self.icdl = data["quests"]["icdl"]
            self.haram_test = data["quests"]["haram_test"]
            self.lost_guy = data["quests"]["lost_guy"]
            self.not_saint = data["quests"]["saint"]
            self.prayed = data["quests"]["prayed"]

            # Bananok
            self.number_bananok = data["number_bananok"]
            self.bananky_in_trash = data["bananky_in_trash"]
            self.bananky_on_ground = data["bananky_on_ground"]

            # Amper stuff
            self.amper_stuff = data["amper_stuff"]

            # Grades
            self.grades = {} if "grades" not in data.keys() else data["grades"]

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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_i and len(self.inv) != 0: 
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
                    case "Router": self.routering()
                    case "Pult": self.quest.amper(self.amper_stuff)
                    case "Battery": self.batteries()
                    case "Flashlight": self.flashlight()
                    case "Ladder": self.ladder()

                # Reset
                self.interacted = ["", "", ""]  
                
    def flashlight(self):
        """
        Player finds a flashlight
        """

        # Found flashlight
        if self.interacted[2] == 63 and self.interacted[1] == 23 and list(self.inv.keys()).count("light") == 0 and list(self.inv.keys()).count("flashlight") == 0 and self.in_room == self.rooms[THIRD_FLOOR]: 
            self.inv['light'] = "img/light.png"
            self.info("A flashlight. Shit. It doesn't have any batteries.")

        # Has flashlight
        else: 
            self.talking("Why are there 2 flashlights?")
            self.talking("Well, I already have one. I don't need more.")
    
    def batteries(self):
        """
        Player finds batteries for crafting the flashlight
        """

        # Found batteries
        if self.interacted[2] == 26 and self.interacted[1] == 5 and list(self.inv.keys()).count("battery") == 0 and list(self.inv.keys()).count("flashlight") == 0 and self.in_room == self.rooms[GROUND_FLOOR]: 
            self.inv['battery'] = "img/battery.png"
            self.info("Batteries. I wonder how I can use them.")

        # Has batteries
        else: self.info("I already took some.")

    def ladder(self):
        """
        Somehow putting ladder into pocket
        """

        if "ladder" not in self.inv.keys():
            self.inv["ladder"] = "img/ladder.png"
            self.talking("I might need this ladder. Yoink.")
            self.talking("How did I managed to put that in my pocket?")
        
        else: self.talking("There sure is a lot of ladders down here.")

    def routering(self):
        """
        Checks if you know routering
        """
        
        if type(self.connected_router) == list:
            router_outcome = "I rather leave it be."

            # Already connected
            if self.saved_room_data in self.connected_router: self.info("I already connected this.")
            else: router_outcome = self.quest.router()

            # After connecting
            if router_outcome != "I rather leave it be.": 

                # Correct
                if len(router_outcome) == 3:
                    self.connected_router.append(router_outcome) 
                    self.info("Connected routers {}/4".format(len(self.connected_router)))

                # Wrong
                else: self.info(router_outcome)

            # Left
            else: self.info(router_outcome)
                        
        # Didn't talk to (Ne)Pusti yet
        else: self.talking("I don't know what to do with this.")

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

    def show_dlcs(self):
        
        lyziarak_cover = pygame.image.load("img/lyziarak_dlc_cover.png")
        lyziarak_rect: pygame.Rect = pygame.Rect(WIN_WIDTH // 2 - 80, WIN_HEIGHT // 2 - 145, 180, 280)
        lyz_dlc_title = self.font.render("Lyziarsky DLC", True, WHITE)
        lyz_dlc_title_rect = lyz_dlc_title.get_rect(x=lyziarak_rect.left + 25, y=lyziarak_rect.bottom + 10)
        previewing: bool = True
        
        while previewing:
            if self.music_on: pygame.mixer.Sound.stop(self.theme)
            
            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            pressed: bool = False
            
            # Close button
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and lyziarak_rect.collidepoint(mouse_pos) and self.bought:
                    previewing = False
                    self.in_room = self.lyz_rooms[OUTSIDE]
                    self.create_tile_map()
                    self.camera.set_lyz_camera()
                elif event.type == pygame.MOUSEBUTTONDOWN and lyziarak_rect.collidepoint(mouse_pos) and not self.bought: pressed = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: previewing = False; break
            
            
            if lyziarak_rect.collidepoint(mouse_pos): bg = pygame.image.load("img/lyziarak_chata.png")
            else: bg = pygame.image.load("img/exiting.png")
            
            # BG
            self.screen.blit(bg, (0, 0))
            self.screen.blit(lyziarak_cover, (WIN_WIDTH // 2 - 80, WIN_HEIGHT // 2 - 140))
            self.screen.blit(lyz_dlc_title, lyz_dlc_title_rect)
            if pressed:
                for _ in range(self.talking_speed_number):
                    self.screen.blit(self.font.render("Not yet bought", True, RED), (lyz_dlc_title_rect.centerx - 75, 50))
                    pygame.draw.rect(self.screen, BLACK, lyziarak_rect, 5, 6)
                    self.clock.tick(FPS)
                    pygame.display.update()
            pygame.draw.rect(self.screen, BLACK, lyziarak_rect, 5, 6)

            # Updates
            self.clock.tick(FPS)
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
        dlc_button = Button(WIN_WIDTH // 2 - 155, WIN_HEIGHT // 2 + 50, 310, 40, fg=WHITE, bg=BLACK, content="Available DLCs", fontsize=32)
        exit_pause: bool = False
        
        while True:

            # Close button
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
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
            if sq_button.is_pressed(mouse_pos, mouse_pressed): self.save_game(); sys.exit()
            
            # Show all DLCs
            if dlc_button.is_pressed(mouse_pos, mouse_pressed): self.show_dlcs(); break
            # BG
            self.screen.blit(bg, (0, 0))

            # Buttons
            self.screen.blit(return_button.image, return_button.rect)
            self.screen.blit(settings_button.image, settings_button.rect)
            self.screen.blit(sq_button.image, sq_button.rect)
            self.screen.blit(dlc_button.image, dlc_button.rect)

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
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and len(self.inv.keys()) > max_items: max_items += 7; min_items += 7; inventory_coords = {}

                # Left arrow
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and min_items != 0: max_items -= 7; min_items -= 7; inventory_coords = {}
                
                # Items in inv
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in inventory_coords:
                        if inventory_coords[i].collidepoint(event.pos): open_inventory = self.inventory_item_info(i); break

            # Updates
            self.clock.tick(FPS)
            pygame.display.update()
                         
    def inventory_item_info(self, img: str):
        """
        Player talks about item in inventory
        """
        
        match img:
            
            case "img/locker key.png": self.info("A key from my locker. It's 10th from the door.", BRITISH_WHITE, 90) # Locker key
            case "img/light.png": self.info("A flashlight without batteries.", BRITISH_WHITE, 90) # Light without batteries
            case "img/flashlight.png": self.info("Working flashlight.", BRITISH_WHITE, 90) # Flashlight for basement
            case "img/battery.png": self.info("Batteries. I wonder how I can use them.", BRITISH_WHITE, 90), # Batteries
            case "img/changing_room key.png": self.info("This key is used for OUR changing room.", BRITISH_WHITE, 90) # Changing room key
            case "img/vtipnicek_small.png": self.info("I can read you.", BRITISH_WHITE, 90); self.open_vtipnicek() # Vtipnicek
            case "img/Iphone_small.png": self.info("Let's check my phone.", BRITISH_WHITE, 90); self.suplovanie = self.quest.check_suplovanie() # Iphone
            case "img/amper key.png": self.info("A suspicious key from buffet Amper,", BRITISH_WHITE, 90) # Amper key
            case "img/kokosky1_small.png": self.info("1 of 4 parts of Forbidden Kokosky.", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky2_small.png": self.info("1 of 4 parts of Forbidden Kokosky.", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky3_small.png": self.info("1 of 4 parts of Forbidden Kokosky.", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky4_small.png": self.info("1 of 4 parts of Forbidden Kokosky.", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky12_small.png": self.info("2 of 4 parts of Forbidden Kokosky.", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky13_small.png": self.info("2 of 4 parts of Forbidden Kokosky.", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky14_small.png": self.info("2 of 4 parts of Forbidden Kokosky.", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky23_small.png": self.info("2 of 4 parts of Forbidden Kokosky.", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky24_small.png": self.info("2 of 4 parts of Forbidden Kokosky.", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky34_small.png": self.info("2 of 4 parts of Forbidden Kokosky.", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky123_small.png": self.info("3 of 4 parts of Forbidden Kokosky.", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky124_small.png": self.info("3 of 4 parts of Forbidden Kokosky.", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky234_small.png": self.info("3 of 4 parts of Forbidden Kokosky.", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/kokosky_small.png": self.info("Forbidden Kokosky", BRITISH_WHITE, 90); self.show_kokosky(img) # Kokosky
            case "img/bananok.png": self.info("You have " + str(self.number_bananok) + " of bananoks.", BRITISH_WHITE, 90) # Bananok
            case "img/map.png": return self.teleporter_map() # Teleport-Map
            case "img/level teleporter.png": return self.level_teleporter() # Portable elevator
            case "img/ultra_teleporter.png": return self.ultra_teleporter() # Ultra teleporter
            case "img/referat.png": self.info("This might help with my grades.", BRITISH_WHITE, 90) # Referat
            case "img/master_key.png": self.info("Now I can escape this mansion.", BRITISH_WHITE, 90) # Master key
            case "img/retake.png": return self.retake() # Retake
            case "img/vujcheek fender.png": self.info("That old geezer can't touch me with this.", BRITISH_WHITE, 90) # Vujcheek fender
            case "img/ladder.png": self.info("I still don't know how I put it in my pocket.", BRITISH_WHITE, 90) # Ladder

        return True

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
        
        if "battery" in inv and "light" in inv:
            self.inv.pop("battery"); self.inv.pop("light")
            self.inv['flashlight'] = "img/flashlight.png"
            self.talking("I put the batteries in the flashlight.")
            self.talking("Now the flashlight has batteries and works.")
            self.info("You acquired working flashlight.", GREEN)
        
        if "level teleporter" in inv and "map" in inv:
            self.inv.pop("level teleporter"); self.inv.pop("map")
            self.inv["ultra_teleporter"] = "img/ultra_teleporter.png" # for now

        if "Kokosky1" in inv and "Kokosky2" in inv:
            self.inv.pop("Kokosky1"); self.inv.pop("Kokosky2")
            self.inv["Kokosky12"] = "img/kokosky12_small.png"
            self.info("Your Kokosky are now level 2.", GREEN)

        if "Kokosky1" in inv and "Kokosky3" in inv:
            self.inv.pop("Kokosky1"); self.inv.pop("Kokosky3")
            self.inv["Kokosky13"] = "img/kokosky13_small.png"
            self.info("Your Kokosky are now level 2.", GREEN)

        if "Kokosky1" in inv and "Kokosky4" in inv:
            self.inv.pop("Kokosky1"); self.inv.pop("Kokosky4")
            self.inv["Kokosky14"] = "img/kokosky14_small.png"
            self.info("Your Kokosky are now level 2.", GREEN)

        if "Kokosky2" in inv and "Kokosky3" in inv:
            self.inv.pop("Kokosky2"); self.inv.pop("Kokosky3")
            self.inv["Kokosky23"] = "img/kokosky23_small.png"
            self.info("Your Kokosky are now level 2.", GREEN)

        if "Kokosky2" in inv and "Kokosky4" in inv:
            self.inv.pop("Kokosky2"); self.inv.pop("Kokosky4")
            self.inv["Kokosky24"] = "img/kokosky24_small.png"
            self.info("Your Kokosky are now level 2.", GREEN)

        if "Kokosky3" in inv and "Kokosky4" in inv:
            self.inv.pop("Kokosky3"); self.inv.pop("Kokosky4")
            self.inv["Kokosky34"] = "img/kokosky34_small.png"
            self.info("Your Kokosky are now level 2.", GREEN)

        if "Kokosky12" in inv and "Kokosky3" in inv:
            self.inv.pop("Kokosky12"); self.inv.pop("Kokosky3")
            self.inv["Kokosky123"] = "img/kokosky123_small.png"
            self.info("Your Kokosky are now level 3.", GREEN)

        if "Kokosky12" in inv and "Kokosky4" in inv:
            self.inv.pop("Kokosky12"); self.inv.pop("Kokosky4")
            self.inv["Kokosky124"] = "img/kokosky124_small.png"
            self.info("Your Kokosky are now level 3.", GREEN)

        if "Kokosky13" in inv and "Kokosky2" in inv:
            self.inv.pop("Kokosky13"); self.inv.pop("Kokosky2")
            self.inv["Kokosky123"] = "img/kokosky123_small.png"
            self.info("Your Kokosky are now level 3.", GREEN)

        if "Kokosky13" in inv and "Kokosky4" in inv:
            self.inv.pop("Kokosky13"); self.inv.pop("Kokosky4")
            self.inv["Kokosky134"] = "img/kokosky134_small.png"
            self.info("Your Kokosky are now level 3.", GREEN)

        if "Kokosky14" in inv and "Kokosky2" in inv:
            self.inv.pop("Kokosky14"); self.inv.pop("Kokosky2")
            self.inv["Kokosky124"] = "img/kokosky124_small.png"
            self.info("Your Kokosky are now level 3.", GREEN)

        if "Kokosky14" in inv and "Kokosky3" in inv:
            self.inv.pop("Kokosky14"); self.inv.pop("Kokosky3")
            self.inv["Kokosky134"] = "img/kokosky134_small.png"
            self.info("Your Kokosky are now level 3.", GREEN)

        if "Kokosky23" in inv and "Kokosky1" in inv:
            self.inv.pop("Kokosky23"); self.inv.pop("Kokosky1")
            self.inv["Kokosky123"] = "img/kokosky123_small.png"
            self.info("Your Kokosky are now level 3.", GREEN)

        if "Kokosky23" in inv and "Kokosky4" in inv:
            self.inv.pop("Kokosky23"); self.inv.pop("Kokosky4")
            self.inv["Kokosky234"] = "img/kokosky234_small.png"
            self.info("Your Kokosky are now level 3.", GREEN)

        if "Kokosky24" in inv and "Kokosky1" in inv:
            self.inv.pop("Kokosky24"); self.inv.pop("Kokosky1")
            self.inv["Kokosky124"] = "img/kokosky124_small.png"
            self.info("Your Kokosky are now level 3.", GREEN)

        if "Kokosky24" in inv and "Kokosky3" in inv:
            self.inv.pop("Kokosky24"); self.inv.pop("Kokosky3")
            self.inv["Kokosky234"] = "img/kokosky234_small.png"
            self.info("Your Kokosky are now level 3.", GREEN)

        if "Kokosky34" in inv and "Kokosky1" in inv:
            self.inv.pop("Kokosky34"); self.inv.pop("Kokosky1")
            self.inv["Kokosky134"] = "img/kokosky134_small.png"
            self.info("Your Kokosky are now level 3.", GREEN)

        if "Kokosky34" in inv and "Kokosky3" in inv:
            self.inv.pop("Kokosky34"); self.inv.pop("Kokosky3")
            self.inv["Kokosky234"] = "img/kokosky234_small.png"
            self.info("Your Kokosky are now level 3.",  GREEN)

        if "Kokosky123" in inv and "Kokosky4" in inv:
            self.inv.pop("Kokosky123"); self.inv.pop("Kokosky4")
            self.inv["Kokosky"] = "img/kokosky_small.png"
            self.info("Your Kokosky are now max level.", GREEN)

        if "Kokosky124" in inv and "Kokosky3" in inv:
            self.inv.pop("Kokosky124"); self.inv.pop("Kokosky3")
            self.inv["Kokosky"] = "img/kokosky_small.png"
            self.info("Your Kokosky are now max level.", GREEN)

        if "Kokosky134" in inv and "Kokosky2" in inv:
            self.inv.pop("Kokosky134"); self.inv.pop("Kokosky2")
            self.inv["Kokosky"] = "img/kokosky_small.png"
            self.info("Your Kokosky are now max level.", GREEN)

        if "Kokosky234" in inv and "Kokosky1" in inv:
            self.inv.pop("Kokosky234"); self.inv.pop("Kokosky1")
            self.inv["Kokosky"] = "img/kokosky_small.png"
            self.info("Your Kokosky are now max level.", GREEN)
               
    def level_teleporter(self):
        """
        Device that let's you teleport through various levels of our school
        """
        
        solo_leveling = True
        
        zero = Button(40,  200,80, 80, fg=DIM_GRAY, bg=NEARLY_BLACK, content="0", fontsize=32)
        one = Button(160, 200, 80, 80, fg=DIM_GRAY, bg=NEARLY_BLACK, content="1", fontsize=32)
        two = Button(280, 200, 80, 80, fg=DIM_GRAY, bg=NEARLY_BLACK, content="2", fontsize=32)
        three = Button(400, 200, 80, 80, fg=DIM_GRAY, bg=NEARLY_BLACK, content="3", fontsize=32)
        four = Button(520, 200, 80, 80, fg=DIM_GRAY, bg=NEARLY_BLACK, content="4", fontsize=32)
        
        while solo_leveling:
            
            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Event loop
            for event in pygame.event.get():
                
                # Close button
                if event.type == pygame.QUIT: self.exiting()
                
                # Keys pressed
                if event.type == pygame.KEYDOWN:

                    # Escape
                    if event.key == pygame.K_ESCAPE: solo_leveling = False; return True

                    # Ground floor
                    elif event.key == pygame.K_0: solo_leveling = False; self.in_room = self.rooms[GROUND_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.set_level_camera(self.in_room); return False

                    # First floor
                    elif event.key == pygame.K_1: solo_leveling = False; self.in_room = self.rooms[FIRST_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.set_level_camera(self.in_room); return False

                    # Second floor
                    elif event.key == pygame.K_2: solo_leveling = False; self.in_room = self.rooms[SECOND_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.set_level_camera(self.in_room); return False

                    # Third floor
                    elif event.key == pygame.K_3: solo_leveling = False; self.in_room = self.rooms[THIRD_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.set_level_camera(self.in_room); return False

                    # Fourth floor
                    elif event.key == pygame.K_4: solo_leveling = False; self.in_room = self.rooms[FOURTH_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.set_level_camera(self.in_room); return False

            # Ground floor
            if zero.is_pressed(mouse_pos, mouse_pressed): solo_leveling = False; self.in_room = self.rooms[GROUND_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.set_level_camera(self.in_room); return False

            # First floor
            if one.is_pressed(mouse_pos, mouse_pressed): solo_leveling = False; self.in_room = self.rooms[FIRST_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.set_level_camera(self.in_room); return False

            # Second floor
            if two.is_pressed(mouse_pos, mouse_pressed): solo_leveling = False; self.in_room = self.rooms[SECOND_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.set_level_camera(self.in_room); return False

            # Third floor
            if three.is_pressed(mouse_pos, mouse_pressed): solo_leveling = False; self.in_room = self.rooms[THIRD_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.set_level_camera(self.in_room); return False

            # Fourth floor
            if four.is_pressed(mouse_pos, mouse_pressed): solo_leveling = False; self.in_room = self.rooms[FOURTH_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.set_level_camera(self.in_room); return False

            # Draws buttons on screen
            self.screen.blit(zero.image, zero.rect)
            self.screen.blit(one.image, one.rect)
            self.screen.blit(two.image, two.rect)
            self.screen.blit(three.image, three.rect)
            self.screen.blit(four.image, four.rect)
            
            # Updates
            self.clock.tick(FPS)
            pygame.display.update()

    def teleporter_map(self):
        """
        Map that teleports you to selected room on your current floor
        """
        
        mapping = True 

        maps = ["img/ground_floor_map.png", "img/first_floor_map.png", "img/second_floor_map.png", "img/third_floor_map.png", "img/fourth_floor_map.png"]
        
        rooms_to_rooms: dict[str, dict[str, pygame.Rect]] = {
            "ground_floor": {
                "002": pygame.Rect(168, 253, 48, 102),
                "003": pygame.Rect(119, 253, 49, 102),
                "004": pygame.Rect(61, 253, 58, 102),
                "006": pygame.Rect(3, 250, 58, 105),
                "007": pygame.Rect(4, 357, 58, 108),
                "008": pygame.Rect(62, 404, 56, 60),
                "010": pygame.Rect(160, 404, 40, 62),
                "012": pygame.Rect(243, 252, 65, 104),
                "013": pygame.Rect(308, 252, 65, 104),
                "014": pygame.Rect(373, 252, 45, 103),
                "015": pygame.Rect(418, 252, 65, 102),
                "016": pygame.Rect(483, 252, 65, 102),
                "017": pygame.Rect(548, 252, 21, 103),
                "019": pygame.Rect(569, 402, 65, 63),
                "023": pygame.Rect(438, 402, 65, 64),
                "025": pygame.Rect(329, 402, 44, 64)
            },
            
            "first_floor": {
                "112": pygame.Rect(248, 333, 60, 61),
                "113": pygame.Rect(306, 333, 67, 60),
                "114": pygame.Rect(371, 333, 48, 59),
                "115": pygame.Rect(417, 333, 67, 59),
                "117": pygame.Rect(499, 333, 58, 59),
                "Toilets_1": pygame.Rect(556, 333, 15, 59),
                "122/2": pygame.Rect(588, 220, 48, 61),
                "122/1": pygame.Rect(588, 281, 48, 57),
                "123": pygame.Rect(588, 338, 46, 32),
                "124": pygame.Rect(536, 414, 83, 63),
                "126": pygame.Rect(473, 414, 46, 63),
                "127": pygame.Rect(414, 414, 57, 63),
                "130": pygame.Rect(305, 414, 69, 37)
            },
            
            "second_floor": {
                "202": pygame.Rect(74, 328, 63, 60),
                "201": pygame.Rect(140, 330, 68, 58),
                "204": pygame.Rect(8, 329, 64, 28),
                "208": pygame.Rect(237, 327, 64, 62),
                "209": pygame.Rect(304, 330, 58, 56),
                "210": pygame.Rect(412, 330, 60, 55),
                "212": pygame.Rect(496, 330, 60, 57),
                "216": pygame.Rect(572, 243, 60, 89),
                "217": pygame.Rect(589, 333, 41, 33),
                "218": pygame.Rect(543, 410, 72, 60),
                "219": pygame.Rect(480, 410, 61, 61),
                "220": pygame.Rect(412, 410, 64, 59),
                "Toilets_21": pygame.Rect(169, 411, 24, 35),
                "Toilets_22": pygame.Rect(558, 327, 12, 19),
                "205": pygame.Rect(73, 410, 75, 38),
                "203": pygame.Rect(8, 359, 65, 91),
            },
            
            "third_floor": {
                "304": pygame.Rect(28, 274, 416, 189),
                "302": pygame.Rect(132, 237, 313, 30),
                "Gym - chr": pygame.Rect(447, 236, 46, 55),
                "305": pygame.Rect(448, 354, 112, 112),
                "Showers": pygame.Rect(565, 353, 49, 116)
            },
            
            "fourth_floor": {
                "402": pygame.Rect(123, 262, 323, 35),
                "403": pygame.Rect(446, 368, 171, 108)
            }
        }
        
        on_level = self.rooms.index(self.in_room)
        bg = pygame.image.load(maps[on_level])

        while mapping:

            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: self.exiting()

                # Esc
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: mapping = False

                # Mouse
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    
                    for room in rooms_to_rooms[maps[on_level][4:-8]]:
                        if rooms_to_rooms[maps[on_level][4:-8]][room].collidepoint(event.pos): 
                            match room:
                                case "002": self.saved_room_data = "002"
                                case "003": self.saved_room_data = "003"
                                case "004": self.saved_room_data = "004"
                                case "006": self.saved_room_data = "006"
                                case "007": self.saved_room_data = "007"
                                case "008": self.saved_room_data = "008"
                                case "010": self.saved_room_data = "010"
                                case "012": self.saved_room_data = "012"
                                case "013": self.saved_room_data = "013"
                                case "014": self.saved_room_data = "014"
                                case "015": self.saved_room_data = "015"
                                case "016": self.saved_room_data = "016"
                                case "017": self.saved_room_data = "017"
                                case "019": self.saved_room_data = "Amper"
                                case "023": self.saved_room_data = "023"
                                case "025": self.saved_room_data = "025"
                                case "112": self.saved_room_data = "112"
                                case "113": self.saved_room_data = "113"
                                case "114": self.saved_room_data = "114"
                                case "115": self.saved_room_data = "115"
                                case "117": self.saved_room_data = "117"
                                case "Toilets_1": self.saved_room_data = "Toilets_1"
                                case "122/2":self.saved_room_data = "122/2"
                                case "122/1":self.saved_room_data = "122/1"
                                case "123": self.saved_room_data = "123"
                                case "124": self.saved_room_data = "124"
                                case "126": self.saved_room_data = "126"
                                case "127": self.saved_room_data = "127"
                                case "130": self.saved_room_data = "130"
                                case "202": self.saved_room_data = "202"
                                case "201": self.saved_room_data = "201"
                                case "204": self.saved_room_data = "Cabinet HAR"
                                case "208": self.saved_room_data = "208"
                                case "209": self.saved_room_data = "209"
                                case "210": self.saved_room_data = "210"
                                case "212": self.saved_room_data = "212"
                                case "216": self.saved_room_data = "216"
                                case "217": self.saved_room_data = "217"
                                case "218": self.saved_room_data = "218"
                                case "219": self.saved_room_data = "219"
                                case "220": self.saved_room_data = "220"
                                case "Toilets_21": self.saved_room_data = "Toilets_21"
                                case "Toilets_22": self.saved_room_data = "Toilets_22"
                                case "205": self.saved_room_data = "205"
                                case "203": self.saved_room_data = "203"
                                case "204": self.saved_room_data = "204"
                                case "304": self.saved_room_data = "304" 
                                case "302": self.saved_room_data = "302" 
                                case "Gym - chr": self.saved_room_data = "Gym - chr"
                                case "305": self.saved_room_data = "Gymnasium - chr"
                                case "Showers": self.saved_room_data = "Showers"
                                case "402": self.saved_room_data = "402" 
                                case "403": self.saved_room_data = "403" 

                            # Moving the player
                            self.create_tile_map()
                            if on_level == 0: self.camera.set_ground_camera()
                            elif on_level == 1: self.camera.set_first_camera()
                            elif on_level == 2: self.camera.set_second_camera()
                            elif on_level == 3: self.camera.set_third_camera()
                            elif on_level == 4: self.camera.set_fourth_camera()

                            mapping = False

                            return False

            # Bg
            self.screen.blit(bg, (0, 0))
            for room in rooms_to_rooms[maps[on_level][4:-8]]: pygame.draw.rect(self.screen, BLACK, rooms_to_rooms[maps[on_level][4:-8]][room], 2)
            
            # Updates
            self.clock.tick(FPS)
            pygame.display.update()

    def ultra_teleporter(self):
        """
        Ultra teleporter, can teleport between floors and rooms
        """

        mapping = True 

        zero = Button(40, 115, 80, 80, fg=DIM_GRAY, bg=NEARLY_BLACK, content="0", fontsize=32)
        one = Button(160, 115, 80, 80, fg=DIM_GRAY, bg=NEARLY_BLACK, content="1", fontsize=32)
        two = Button(280, 115, 80, 80, fg=DIM_GRAY, bg=NEARLY_BLACK, content="2", fontsize=32)
        three = Button(400, 115, 80, 80, fg=DIM_GRAY, bg=NEARLY_BLACK, content="3", fontsize=32)
        four = Button(520, 115, 80, 80, fg=DIM_GRAY, bg=NEARLY_BLACK, content="4", fontsize=32)

        maps = ["img/ground_floor_map.png", "img/first_floor_map.png", "img/second_floor_map.png", "img/third_floor_map.png", "img/fourth_floor_map.png"]
        
        rooms_to_rooms: dict[str, dict[str, pygame.Rect]] = {
            "ground_floor": {
                "002": pygame.Rect(168, 253, 48, 102),
                "003": pygame.Rect(119, 253, 49, 102),
                "004": pygame.Rect(61, 253, 58, 102),
                "006": pygame.Rect(3, 250, 58, 105),
                "007": pygame.Rect(4, 357, 58, 108),
                "008": pygame.Rect(62, 404, 56, 60),
                "010": pygame.Rect(160, 404, 40, 62),
                "012": pygame.Rect(243, 252, 65, 104),
                "013": pygame.Rect(308, 252, 65, 104),
                "014": pygame.Rect(373, 252, 45, 103),
                "015": pygame.Rect(418, 252, 65, 102),
                "016": pygame.Rect(483, 252, 65, 102),
                "017": pygame.Rect(548, 252, 21, 103),
                "019": pygame.Rect(569, 402, 65, 63),
                "023": pygame.Rect(438, 402, 65, 64),
                "025": pygame.Rect(329, 402, 44, 64)
            },
            
            "first_floor": {
                "112": pygame.Rect(248, 333, 60, 61),
                "113": pygame.Rect(306, 333, 67, 60),
                "114": pygame.Rect(371, 333, 48, 59),
                "115": pygame.Rect(417, 333, 67, 59),
                "117": pygame.Rect(499, 333, 58, 59),
                "Toilets_1": pygame.Rect(556, 333, 15, 59),
                "122/2": pygame.Rect(588, 220, 48, 61),
                "122/1": pygame.Rect(588, 281, 48, 57),
                "123": pygame.Rect(588, 338, 46, 32),
                "124": pygame.Rect(536, 414, 83, 63),
                "126": pygame.Rect(473, 414, 46, 63),
                "127": pygame.Rect(414, 414, 57, 63),
                "130": pygame.Rect(305, 414, 69, 37)
            },
            
            "second_floor": {
                "202": pygame.Rect(74, 328, 63, 60),
                "201": pygame.Rect(140, 330, 68, 58),
                "204": pygame.Rect(8, 329, 64, 28),
                "208": pygame.Rect(237, 327, 64, 62),
                "209": pygame.Rect(304, 330, 58, 56),
                "210": pygame.Rect(412, 330, 60, 55),
                "212": pygame.Rect(496, 330, 60, 57),
                "216": pygame.Rect(572, 243, 60, 89),
                "217": pygame.Rect(589, 333, 41, 33),
                "218": pygame.Rect(543, 410, 72, 60),
                "219": pygame.Rect(480, 410, 61, 61),
                "220": pygame.Rect(412, 410, 64, 59),
                "Toilets_21": pygame.Rect(169, 411, 24, 35),
                "Toilets_22": pygame.Rect(558, 327, 12, 19),
                "205": pygame.Rect(73, 410, 75, 38),
                "203": pygame.Rect(8, 359, 65, 91),
            },
            
            "third_floor": {
                "304": pygame.Rect(28, 274, 416, 189),
                "302": pygame.Rect(132, 237, 313, 30),
                "Gym - chr": pygame.Rect(447, 236, 46, 55),
                "305": pygame.Rect(448, 354, 112, 112),
                "Showers": pygame.Rect(565, 353, 49, 116)
            },
            
            "fourth_floor": {
                "402": pygame.Rect(123, 262, 323, 35),
                "403": pygame.Rect(446, 368, 171, 108)
            }
        }
        
        while mapping:

            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: self.exiting()

                # Esc
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: mapping = False

                # Mouse
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    for room in rooms_to_rooms[maps[on_level][4:-8]]:
                        if rooms_to_rooms[maps[on_level][4:-8]][room].collidepoint(event.pos): 
                            match room:
                                case "002": self.saved_room_data = "002"
                                case "003": self.saved_room_data = "003"
                                case "004": self.saved_room_data = "004"
                                case "006": self.saved_room_data = "006"
                                case "007": self.saved_room_data = "007"
                                case "008": self.saved_room_data = "008"
                                case "010": self.saved_room_data = "010"
                                case "012": self.saved_room_data = "012"
                                case "013": self.saved_room_data = "013"
                                case "014": self.saved_room_data = "014"
                                case "015": self.saved_room_data = "015"
                                case "016": self.saved_room_data = "016"
                                case "017": self.saved_room_data = "017"
                                case "019": self.saved_room_data = "Amper"
                                case "023": self.saved_room_data = "023"
                                case "025": self.saved_room_data = "025"
                                case "112": self.saved_room_data = "112"
                                case "113": self.saved_room_data = "113"
                                case "114": self.saved_room_data = "114"
                                case "115": self.saved_room_data = "115"
                                case "117": self.saved_room_data = "117"
                                case "Toilets_1": self.saved_room_data = "Toilets_1"
                                case "122/2":self.saved_room_data = "122/2"
                                case "122/1":self.saved_room_data = "122/1"
                                case "123": self.saved_room_data = "123"
                                case "124": self.saved_room_data = "124"
                                case "126": self.saved_room_data = "126"
                                case "127": self.saved_room_data = "127"
                                case "130": self.saved_room_data = "130"
                                case "202": self.saved_room_data = "202"
                                case "201": self.saved_room_data = "201"
                                case "204": self.saved_room_data = "Cabinet HAR"
                                case "208": self.saved_room_data = "208"
                                case "209": self.saved_room_data = "209"
                                case "210": self.saved_room_data = "210"
                                case "212": self.saved_room_data = "212"
                                case "216": self.saved_room_data = "216"
                                case "217": self.saved_room_data = "217"
                                case "218": self.saved_room_data = "218"
                                case "219": self.saved_room_data = "219"
                                case "220": self.saved_room_data = "220"
                                case "Toilets_21": self.saved_room_data = "Toilets_21"
                                case "Toilets_22": self.saved_room_data = "Toilets_22"
                                case "205": self.saved_room_data = "205"
                                case "203": self.saved_room_data = "203"
                                case "204": self.saved_room_data = "204"
                                case "304": self.saved_room_data = "304" 
                                case "302": self.saved_room_data = "302" 
                                case "Gym - chr": self.saved_room_data = "Gym - chr"
                                case "305": self.saved_room_data = "Gymnasium - chr"
                                case "Showers": self.saved_room_data = "Showers"
                                case "402": self.saved_room_data = "402" 
                                case "403": self.saved_room_data = "403" 

                            # Moving the player
                            self.create_tile_map()
                            if on_level == 0: self.camera.set_ground_camera()
                            elif on_level == 1: self.camera.set_first_camera()
                            elif on_level == 2: self.camera.set_second_camera()
                            elif on_level == 3: self.camera.set_third_camera()
                            elif on_level == 4: self.camera.set_fourth_camera()

                            mapping = False

                            return False

                # Keys pressed
                if event.type == pygame.KEYDOWN:

                    # Escape
                    if event.key == pygame.K_ESCAPE: mapping = False; return False

                    # Ground floor
                    elif event.key == pygame.K_0: self.in_room = self.rooms[GROUND_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.saved_room_data = "Hall"; self.set_level_camera(self.in_room)

                    # First floor
                    elif event.key == pygame.K_1: self.in_room = self.rooms[FIRST_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.saved_room_data = "Hall"; self.set_level_camera(self.in_room)

                    # Second floor
                    elif event.key == pygame.K_2: self.in_room = self.rooms[SECOND_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.saved_room_data = "Hall"; self.set_level_camera(self.in_room)

                    # Third floor
                    elif event.key == pygame.K_3: self.in_room = self.rooms[THIRD_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.saved_room_data = "Hall"; self.set_level_camera(self.in_room)

                    # Fourth floor
                    elif event.key == pygame.K_4: self.in_room = self.rooms[FOURTH_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.saved_room_data = "Hall"; self.set_level_camera(self.in_room)

            # Ground floor
            if zero.is_pressed(mouse_pos, mouse_pressed): self.in_room = self.rooms[GROUND_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.set_level_camera(self.in_room); self.draw(); self.update()

            # First floor
            if one.is_pressed(mouse_pos, mouse_pressed): self.in_room = self.rooms[FIRST_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.set_level_camera(self.in_room); self.draw()

            # Second floor
            if two.is_pressed(mouse_pos, mouse_pressed): self.in_room = self.rooms[SECOND_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.set_level_camera(self.in_room); self.draw()

            # Third floor
            if three.is_pressed(mouse_pos, mouse_pressed): self.in_room = self.rooms[THIRD_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.set_level_camera(self.in_room); self.draw()

            # Fourth floor
            if four.is_pressed(mouse_pos, mouse_pressed): self.in_room = self.rooms[FOURTH_FLOOR]; self.create_tile_map(); self.saved_room_data = "Hall"; self.set_level_camera(self.in_room); self.draw()

            # Bg
            on_level = self.rooms.index(self.in_room)
            bbg = pygame.image.load("img/screen.png")
            bg = pygame.image.load(maps[on_level])
            self.screen.blit(bbg, (0, 0))
            self.screen.blit(bg, (0, 0))
            for room in rooms_to_rooms[maps[on_level][4:-8]]: pygame.draw.rect(self.screen, BLACK, rooms_to_rooms[maps[on_level][4:-8]][room], 2)

            # Draws buttons on screen
            self.screen.blit(zero.image, zero.rect)
            self.screen.blit(one.image, one.rect)
            self.screen.blit(two.image, two.rect)
            self.screen.blit(three.image, three.rect)
            self.screen.blit(four.image, four.rect)
            
            # Updates
            self.clock.tick(FPS)
            pygame.display.update()

    def retake(self):
        """
        Player can retake any test that could go wrong
        """
        
        retaking = True
        
        x: int = 2.5
        y: int = 200

        retakeable = ["MAT", "SJL", "OBN", "OSY", "AEN", "IOT", "TSV", "ICD", "PRO", "ANJ"]
        
        # Button
        lessons: list[Button] = [Button(x + retakeable.index(lesson) * 64, y, 60, 60, fg=BRITISH_WHITE, bg=BLACK, content=lesson, fontsize=28) for lesson in retakeable]
        
        while retaking:
            
            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Events
            for event in pygame.event.get():

                # Close button
                if event.type == pygame.QUIT: self.exiting()

                # Esc
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: retaking = False
                
            # Buttons
            for button in lessons: self.screen.blit(button.image, button.rect)
            
            for index in range(len(lessons)): 
                if lessons[index].is_pressed(mouse_pos, mouse_pressed) and lessons[index].content in self.grades.keys():
                    self.grades.pop(lessons[index].content); self.inv.pop("retake")
                    match lessons[index].content:
                        case "MAT": self.mat_test = True
                        case "SJL": self.sjl_test = True
                        case "OBN": self.obn_test = True  
                        case "OSY": self.osy = True
                        case "AEN": self.resistor = True
                        case "IOT": self.iot = True
                        case "TSV": self.dumbbell_lifted= True
                        case "ICD": self.icdl = True
                        case "PRO": self.program_test = True
                        case "ANJ": self.anj_test = True
                    return False

            # Updates
            self.clock.tick(FPS)
            pygame.display.update()

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
                        "amper_locked": self.amper_locked,
                        "amper_key_in_trash": self.amper_key_in_trash,
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
                        "mat_test": self.mat_test,
                        "sjl_test": self.sjl_test,
                        "obn_test": self.obn_test,
                        "referat": self.referat,
                        "window": self.closed_window,
                        "GUL_quest": self.gul_quest,
                        "gul_counter": self.__gul_counter,
                        "nepusti": self.nepusti,
                        "router": self.connected_router,
                        "sooner": self.five_min_sooner, 
                        "resistor": self.resistor,
                        "osy": self.osy,
                        "iot": self.iot,
                        "icdl": self.icdl,
                        "haram_test": self.haram_test,
                        "lost_guy": self.lost_guy,
                        "saint": self.not_saint,
                        "prayed": self.prayed,
                        "locker_stuff": self.locker_stuff, 
                        "without_light": self.without_light,
                        "caught": self.caught
                        }
        
        # Refreshing the password to it's original state for further encodings
        if self._password == "": self._password = open('tfa.txt', 'r').read()
        
        # If the password is already encoded -> decode it first
        elif self._password != open('tfa.txt', 'r').read(): self._password = self.decode_password(self._password)
        
        # Saving
        self.database = SaveProgress(self.player_name, 
                                    self.encode_password(self._password),
                                    self.inv,
                                    self.endings,
                                    self.quests,
                                    self.number_bananok,
                                    self.bananky_in_trash,
                                    self.bananky_on_ground,
                                    self.amper_stuff,
                                    self.rooms.index(self.in_room) if self.in_room in self.rooms else self.lyz_rooms.index(self.in_room),
                                    self.saved_room_data,
                                    self.bought,
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
        endings = ["img/lost.png", "img/you_never_learn.png", "img/window_fail.png", "img/early.png", "img/canon_ending.gif", "img/lucky.png", "img/unlucky.png", "img/unofficial_ending.png", "img/you_tried.png"]
        all_endings = tuple(self.endings)

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

        # Lucky
        elif img == "img/lucky.png" and self.music_on: pygame.mixer.Sound.play(self.lucky, -1)

        # Unlucky
        elif img == "img/unlucky.png" and self.music_on: pygame.mixer.Sound.play(self.unlucky, -1)
        
        # Removing every sprite
        for sprite in self.all_sprites: sprite.kill()

        # Loop
        while self.game_running:

            # Close button
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

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
                self.save_game(); sys.exit()
            
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
            
            elif img == "img/unofficial_ending.png": 
                self.screen.blit(self.game_over_background, (0, 0))
                self.screen.blit(restart_button.image, restart_button.rect)
                self.screen.blit(iamdone_button.image, iamdone_button.rect)
                
                
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
                if event.type == pygame.QUIT: sys.exit()

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
    
    def verifying_user(self, player_name: str) -> str:
        
        # Main verifying data
        data = SaveProgress.load_data(player_name)
        bg = pygame.image.load('img/login_background.png')
        verifying: bool = True
        active_pass: bool = False
        
        # Drawings for inputs etc.
        color_pass = BLACK
        password_info = pygame.Rect(210, 230, 210, 40)
        password = self.font.render("Your password", True, WHITE)
        password_rect = password.get_rect(x=220, y=200)
        wrong = False
        wrong_secret = self.font.render('Wrong password', True, RED)
        wrong_secret_rect = wrong_secret.get_rect(x=200, y=320)
        
        if 'credentials' not in data.keys(): 
            data['credentials'] = ""
            # ↓ TESTING PURPOSES ONLY ↓
            # print(data['credentials'])
        
        if data['credentials'] == "":
            webbrowser.open('https://aeternix-forum.herokuapp.com/register/')
            secret = ''.join((r.choice('abcdefghijklmnopqrstuvwxyz123456789') for _ in range(8)))
            with open('tfa.txt', 'w') as f: f.write(secret)
            
            while verifying:
                for event in pygame.event.get():
                        # Quit
                    if event.type == pygame.QUIT: sys.exit()
                
                        # Click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if password_info.collidepoint(event.pos): active_pass = True
                        else: active_pass = False
                        
                            
                    elif event.type == pygame.KEYDOWN:
                        # Check for backspace
                        if event.key == pygame.K_RETURN:
                            print("Your auth password for account can be found in 'tfa.txt' file")
                            # Add authentication
                            if self._password == secret:
                                verifying = False
                                return self._password
                            else: wrong = True
                        elif event.key == pygame.K_BACKSPACE and active_pass and len(self._password) > 0: self._password = self._password[:-1]
                        
                        elif active_pass: 
                            if secret != "":
                                color_pass = GRAY
                                self._password += event.unicode
                            else: 
                                color_pass = GRAY
                                secret += event.unicode
                        elif not active_pass: color_pass = BLACK

                        elif len(self._password) == 0: active_pass = False
                                
                dots = ""
                for _ in range(len(self._password)): dots += "*"
                                
                    
                self.screen.blit(bg, (0, 0))
                pygame.draw.rect(self.screen, color_pass, password_info)
                self.screen.blit(password, password_rect)
                self.screen.blit(self.font.render(dots, True, WHITE), (password_rect.x + 5, password_rect.y + 35))
                if wrong: self.screen.blit(wrong_secret, wrong_secret_rect)

                # Updates
                self.clock.tick(FPS)
                pygame.display.update()
        elif data['credentials'] != "":
            # encoded password -> WpH<5Z+K&P
            secret: str = self.decode_password(data['credentials'])
            
            while verifying:
                for event in pygame.event.get():
                    # Quit
                    if event.type == pygame.QUIT: sys.exit()
                
                    # Click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if password_info.collidepoint(event.pos): active_pass = True
                        else: active_pass = False
                        
                            
                    elif event.type == pygame.KEYDOWN:
                        # Check for backspace
                        if event.key == pygame.K_RETURN:
                            print("Your auth password for account can be found in 'tfa.txt' file")
                            # Add authentication
                            if self._password == secret:
                                verifying = False
                                return self._password
                            else: wrong = True
                        elif event.key == pygame.K_BACKSPACE and active_pass and len(self._password) > 0: self._password = self._password[:-1]
                        
                        elif active_pass: 
                            if secret != "":
                                color_pass = GRAY
                                self._password += event.unicode
                            else: 
                                color_pass = GRAY
                                secret += event.unicode
                        elif not active_pass: color_pass = BLACK

                        elif len(self._password) == 0: active_pass = False

                dots = ""
                for _ in range(len(self._password)): dots += "*"
                                
                    
                self.screen.blit(bg, (0, 0))
                pygame.draw.rect(self.screen, color_pass, password_info)
                self.screen.blit(password, password_rect)
                self.screen.blit(self.font.render(dots, True, WHITE), (password_rect.x + 5, password_rect.y + 35))
                if wrong: self.screen.blit(wrong_secret, wrong_secret_rect)
                
                # Updates
                self.clock.tick(FPS)
                pygame.display.update()

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
            
            # Position and click of the mouse
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            for event in pygame.event.get():
      
                # Quit
                if event.type == pygame.QUIT: sys.exit()
        
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
                        if len(self.player_name) > 0: 

                            data = SaveProgress.load_data(self.player_name) 

                            if data is not None:

                                deciding = True

                                # Buttons
                                new_button = Button(140, 190, 150, 50, fg=WHITE, bg=BLACK, content="New", fontsize=32)
                                con_button = Button(360, 190, 150, 50, fg=WHITE, bg=BLACK, content="Continue", fontsize=32)

                                while deciding:
                                    # Position and click of the mouse
                                    mouse_pos = pygame.mouse.get_pos()
                                    mouse_pressed = pygame.mouse.get_pressed()
                                    
                                    # Events
                                    for event in pygame.event.get():

                                        # Close button
                                        if event.type == pygame.QUIT: sys.exit()

                                        # Keyboard
                                        elif event.type == pygame.KEYDOWN:

                                            # Esc
                                            if event.key == pygame.K_ESCAPE: deciding = False

                                    # New
                                    if new_button.is_pressed(mouse_pos, mouse_pressed):
                                        picking_name = deciding = intro = False
                                        self.continue_game = False
                                        self._password = self.verifying_user(self.player_name)
                                        
                                    # Continue
                                    if con_button.is_pressed(mouse_pos, mouse_pressed):
                                        picking_name = deciding = intro = False
                                        self.continue_game = True
                                        # self._password = self.verifying_user(self.player_name)
                                    
                                    # Buttons
                                    self.screen.blit(new_button.image, new_button.rect)
                                    self.screen.blit(con_button.image, con_button.rect)
                                    
                                    # Updates
                                    self.clock.tick(FPS)
                                    pygame.display.update()

                            else: picking_name = intro = False
 
                    # Unicode
                    elif active: self.player_name += event.unicode

            
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
                if event.type == pygame.QUIT: sys.exit()
                
                # Keyboard
                elif event.type == pygame.KEYDOWN:

                    # Esc
                    if event.key == pygame.K_ESCAPE: opened = not opened

                    # M
                    elif event.key == pygame.K_m:
                        
                        # Turning on
                        if self.music_on:
                            for _ in range(12):
                                slider.rect.x -= 4
                                slider_inside.rect.x -= 4
                                self._settings_animation(title, title_rect, sound_effects, sound_effects_rect, talking_speed, talking_speed_rect, slider_back, slider, slider_inside, back, slow, medium, fast)
                            self.music_on = not self.music_on
                            slider_inside.rect.x -= 2
                            slider = Button(250, 140, 50, 50, fg=BLACK, bg=RED, content="", fontsize=0)

                        # Turning off
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
            r = pygame.Rect(5, 10-2.5, text_rect.width+5, text_rect.height+5)
            pygame.draw.rect(self.screen, BLACK, r)
            self.screen.blit(text, text_rect)
            self.clock.tick(FPS)
            pygame.display.update()
        self.update()
        self.draw()
        self.saved_room_data = room_number
              
    def talking(self, msg_content: str, change_color: bool = False, additional_color: tuple[int, int, int] = BRITISH_WHITE, g: bool = False, time: int = 0):
        """
        When character is talking
        """

        for _ in range(self.talking_speed_number if not g else time):
            text = self.font.render(msg_content, True, WHITE) if not change_color else self.font.render(msg_content, True, additional_color)
            text_rect = text.get_rect(x=10, y=10)
            r = pygame.Rect(5, 10-2.5, text_rect.width+5, text_rect.height+5)
            pygame.draw.rect(self.screen, BLACK, r)
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
            r = pygame.Rect(5, i-2.5, text_rect.width+5, text_rect.height+5)
            pygame.draw.rect(self.screen, BLACK, r)
            self.screen.blit(text, text_rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def trashcan(self):
        """
        Poking around in trashcan
        """

        # In changing room
        if self.interacted[1] == 13 and self.interacted[2] == 165 and self.in_room == self.rooms[GROUND_FLOOR]:
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
        elif self.interacted[1] == 24 and self.interacted[2] == 43 and self.in_room == self.rooms[SECOND_FLOOR]: 

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
        elif self.interacted[1] == 24 and self.interacted[2] == 78 and self.in_room == self.rooms[SECOND_FLOOR]:
        
            # Kokosky
            if self.kokosky_in_trash:
                self.talking("Why would someone throw away such yummy food.")
                self.number_kokosky += 1
                self.talking(f"{self.player_name} found the forbidden Kokosky fragment. [{self.number_kokosky}/4]")
                self.inv["Kokosky4"] = "img/kokosky4_small.png"
                self.kokosky_in_trash = False

            # Empty
            else: self.talking("There's nothing interesting.")

        # Near green chairs
        elif self.interacted[1] == 39 and self.interacted[2] == 65 and self.in_room == self.rooms[SECOND_FLOOR]:

            # Key
            if self.amper_key_in_trash:
                self.talking("Why is this key there?")
                self.amper_key_in_trash = False
                self.inv["amper key"] = "img/amper key.png"

            # Empty
            else: self.talking("Wow, you found nothing.")
            
        # Referat in 2.SA
        elif self.interacted[1] == 13 and self.interacted[2] == 163 and self.in_room == self.rooms[GROUND_FLOOR] and self.referat:
                self.talking("OMG!")
                self.talking("Why would someone throw this in the trash")
                self.talking("It's someone's OBN referat")
                self.inv["referat"] = "img/referat.png"
                self.referat = False

        # Bananky
        else:

            floors = ["ground floor", "first floor", "second floor", "third floor", "fourth floor", "ending hallway", "basement"]

            # Bananky in
            if self.bananky_in_trash[floors[self.rooms.index(self.in_room)]][str(self.interacted[2]) + str(self.interacted[1])] > 0:
                if "bananok" in self.inv.keys(): self.number_bananok += self.bananky_in_trash[floors[self.rooms.index(self.in_room)]][str(self.interacted[2]) + str(self.interacted[1])]
                else: self.inv["bananok"] = "img/bananok.png"; self.number_bananok += self.bananky_in_trash[floors[self.rooms.index(self.in_room)]][str(self.interacted[2]) + str(self.interacted[1])]
                self.talking(f"{self.player_name} found {self.bananky_in_trash[floors[self.rooms.index(self.in_room)]][str(self.interacted[2]) + str(self.interacted[1])]} of bananoks.")
                self.bananky_in_trash[floors[self.rooms.index(self.in_room)]][str(self.interacted[2]) + str(self.interacted[1])] = 0
            
            # Empty
            else: self.talking(r.choice(["Wow, you found nothing.", "There's nothing interesting.", "Just some rubbish."]))
            
    def window(self):
        """
        Player looks outside of window or falls
        """

        # Window fail ending
        if self.interacted[1] == 27 and self.interacted[2] in (65, 66): pygame.mixer.Sound.play(self.fall); pygame.time.delay(500); self.game_over("img/window_fail.png")

        # Vyvetraj
        elif self.interacted[1] == 28 and self.interacted[2] in (138, 139) and self.closed_window and self.in_room == self.rooms[GROUND_FLOOR]:

            # Has ladder
            if "ladder" in self.inv.keys(): 
                self.quest.vetry()
                if "DSY" in self.grades.keys(): self.draw(); self.update(); self.info("You've recieved a grade for DSY"); self.closed_window = False

            # No ladder
            else: 
                self.talking("I can't reach it.")
                self.talking("Maybe I can find something that will help me in basement.")

        # Windows between classrooms
        elif self.interacted[1] not in (11, 14, 25) and self.interacted[2] not in (98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 110, 111, 112, 113, 173): self.sans() if r.randint(1, 100) == 100 else self.talking("What a pretty day.")

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
            
    def ending_hallway(self):
        """
        Canon ending for the game
        """
        
        self.in_room = self.rooms[ENDING_HALLWAY]
        self.create_tile_map()
        self.camera.set_ending_camera()
            
    def end(self, tried: bool = False):
        """
        Main ending for the game
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
                if event.type == pygame.QUIT: sys.exit()
                

            # Background
            self.screen.blit(ending_screen, (0, 0)) if not tried else self.screen.blit(pygame.image.load("img/you_tried.png"), (0, 0))

            # Exit button
            self.screen.blit(exit_button.image, exit_button.rect)
            if exit_button.is_pressed(mouse_pos, mouse_pressed): self.endings.append("canon_ending") if "canon_ending" not in self.endings else None; self.save_game(); sys.exit()

            # Main menu button
            self.screen.blit(main_menu_button.image, main_menu_button.rect)
            if main_menu_button.is_pressed(mouse_pos, mouse_pressed): self.endings.append("canon_ending") if "canon_ending" not in self.endings else None; self.reseting_game_values(); self.save_game(); pygame.mixer.Sound.stop(self.theme); self.intro_screen().new("old").main()

            # Updates
            self.clock.tick(FPS)
            pygame.display.update()
            
    def lyz_doors(self):
        if self.in_room == self.lyz_rooms[OUTSIDE]:
            if self.player.facing == 'left' and self.interacted[1] in (6, 7) and self.interacted[2] == 7:
                self.in_room = self.lyz_rooms[LYZ_DINER]
                self.door_info("Eat 'n games", 'diner')
                self.create_tile_map()
                self.camera.set_lyz_camera()
            elif self.player.facing == 'right' and self.interacted[1] in (11, 12) and self.interacted[2] == 27:
                self.in_room = self.lyz_rooms[OUTSIDE]
                self.door_info("Brrr... it's cold", 'outside')
                self.create_tile_map()
                self.camera.set_lyz_camera()
            
            elif self.player.facing == 'down' and self.interacted[1] == 27 and self.interacted[2] in (57, 58):  self.info("I shouldn't go there")
            elif self.player.facing == 'right' and self.interacted[1] in (49, 50) and self.interacted[2] == 50: self.info("Not my lodge")
            elif self.player.facing == 'down' and self.interacted[1] == 51 and self.interacted[2] in (12, 13):
                self.in_room = self.lyz_rooms[LYZ_GROUND]
                self.create_tile_map()
            
        
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
            if len(self.grades) == ALL_GRADES:
                if sum(self.grades.values()) // len(self.grades) <= 1.5 and "master_key" in self.inv.keys(): self.talking("This is the end"); self.ending_hallway() # self.end()
                elif 1.5 < sum(self.grades.values()) // len(self.grades) <= 3.5 and "master_key" in self.inv.keys(): self.talking("Well, I got everything"); self.end(tried=True)
                else: self.talking("I don't have the master key to this door."); self.talking("Maybe someone from the school can has it.")

            # Permission to go home sooner
            elif self.five_min_sooner == self.nepusti == self.gul_quest == False: 
                self.talking("Now I can go home sooner!")

                # Didn't have talk with Zo Sarisa
                if self.not_saint: self.game_over("img/early.png")

                # Had talk
                else:

                    # Prayed
                    if self.prayed: self.game_over("img/lucky.png")

                    # Didn't pray
                    elif not self.prayed: self.game_over("img/unlucky.png")

            # Not yet
            elif len(self.grades) < ALL_GRADES: self.talking("I can't go home yet"); self.talking("I must fulfil what is left")
        
        # Hall -> Buffet Amper
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 176:

            # Locked & No key
            if self.amper_locked and "amper key" not in self.inv.keys():
                self.talking("Buffet Amper. I like to buy food here.")
                self.talking("Sadly it's closed now.")
            
            # Locked & Key
            elif self.amper_locked and "amper key" in self.inv.keys():
                pygame.mixer.Sound.play(self.lock)
                self.talking(f"{self.player_name} unlocked the door.")
                self.amper_locked = False

            # Unlocked
            elif not self.amper_locked: self.door_info("Buffet Amper", "Amper"); self.center_player_after_doors()

        # Buffet Amper -> Hall
        elif self.player.facing == "up" and self.interacted[1] == 20 and self.interacted[2] == 176: self.door_info("Hall", "Hall"); self.center_player_after_doors()

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
        elif self.player.facing == "down" and self.interacted[1] == 20 and self.interacted[2] == 88: self.talking("026 - not a classroom")

        # Hall -> 027
        elif self.player.facing == "right" and self.interacted[1] == 25 and self.interacted[2] == 76: self.talking("027 - not a classroom")

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
        elif self.player.facing == "left" and self.interacted[2] == 166 and self.interacted[1] == 12: self.door_info("Toilets", "Toilets_1"); self.center_player_after_doors()
        
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
        elif self.player.facing == "right" and self.interacted[2] == 97 and self.interacted[1] == 21: self.door_info("Cabinet LIA", "114"); self.center_player_after_doors()
        
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
        if self.player.facing == "left" and self.interacted[2] == 11 and self.interacted[1] == 28:
            self.door_info("203 - III.A", "203"); self.center_player_after_doors()
            if self.haram_test: self.haram_test = self.quest.haram()
        
        # Women's Toilets 1
        elif self.player.facing == "down" and self.interacted[2] == 69 and self.interacted[1] == 31: self.talking("I don't know what this is", False, PINK)
        
        # Women's Toilets 2
        elif self.player.facing == "down" and self.interacted[2] == 99 and self.interacted[1] == 31: self.talking("I don't know what this is", False, PINK)

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
        elif self.player.facing == "up" and self.interacted[2] == 41 and self.interacted[1] == 25: self.door_info("201 - II.SB", "201"); self.center_player_after_doors()

        # 201 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 41 and self.interacted[1] == 25: self.door_info("Hall", "Hall"); self.center_player_after_doors()
    
        # Hall -> Toilets
        elif self.player.facing == "down" and self.interacted[2] == 40 and self.interacted[1] == 31: self.door_info("Toilets", "Toilets_21"); self.center_player_after_doors()

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

        # Hall -> 212
        elif self.player.facing == "up" and self.interacted[2] == 157 and self.interacted[1] == 25: self.door_info("212 - IV.A", "212"); self.center_player_after_doors()

        # 212 -> Hall
        elif self.player.facing == "down" and self.interacted[2] == 157 and self.interacted[1] == 25: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Hall -> Toilets
        elif self.player.facing == "left" and self.interacted[2] == 166 and self.interacted[1] == 16: self.door_info("Toilets", "Toilets_22"); self.center_player_after_doors()

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

        # Hall -> 219
        elif self.player.facing == "down" and self.interacted[2] == 139 and self.interacted[1] == 31: self.door_info("219 - I.SA", "219"); self.center_player_after_doors()

        # 219 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 139 and self.interacted[1] == 31: self.door_info("Hall", "Hall"); self.center_player_after_doors()
        
        # Hall -> 220
        elif self.player.facing == "down" and self.interacted[2] == 117 and self.interacted[1] == 31: self.door_info("220 - I.C", "220"); self.center_player_after_doors()

        # 220 -> Hall
        elif self.player.facing == "up" and self.interacted[2] == 117 and self.interacted[1] == 31: self.door_info("Hall", "Hall"); self.center_player_after_doors()
        
    def third_floor_doors(self):
        """
        Doors on the third floor
        """

        # Hall -> Gym changing rooms
        if self.player.facing in ("up", "left") and self.interacted[2] == 63 and self.interacted[1] == 8: self.door_info("Gym - Changing rooms", "Gym - chr"); self.center_player_after_doors()

        # Gym changing rooms -> Hall
        elif self.player.facing in ("down", "right") and self.interacted[2] == 63 and self.interacted[1] == 8: self.door_info("Hall", "Hall"); self.center_player_after_doors()

        # Gym changing rooms -> Toilets
        elif self.player.facing == "left" and self.interacted[2] == 57 and self.interacted[1] == 7: self.door_info("Toilets", "Toilets_3"); self.center_player_after_doors()

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

    def ending_hallway_doors(self):
        """
        Doors in the ending hallway
        """

        if self.player.facing == "up" and self.interacted[2] in (5, 6, 7) and self.interacted[1] == 9: 
            self.center_player_after_doors()
            temp_speed = self.talking_speed_number
            self.talking_speed_number = 120
            self.talking("So this is the end?")
            self.talking("There's nothing, just an empty room.")
            self.talking("Maybe it was supposed to be a room with a TV.")
            self.talking("Or maybe just me in this room.")
            self.talking("Did I do a good job?")
            self.talking("Was I a good student?")
            self.talking("Person?")
            self.talking("What do you think?")
            
            deciding = True

            # Buttons
            yes_button = Button(140, 190, 120, 50, fg=WHITE, bg=BLACK, content="Yes", fontsize=32)
            no_button = Button(360, 190, 120, 50, fg=WHITE, bg=BLACK, content="No", fontsize=32)
            
            while deciding:

                # Position and click of the mouse
                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()
                
                # Events
                for event in pygame.event.get():

                    # Close button
                    if event.type == pygame.QUIT: print("You ruined the whole thing"); sys.exit()

                    # Keyboard
                    elif event.type == pygame.KEYDOWN:

                        # Esc
                        if event.key == pygame.K_ESCAPE: print("You ruined the whole thing"); deciding = False

                # Yes
                if yes_button.is_pressed(mouse_pos, mouse_pressed):
                    self.talking("I did a good job.")
                    self.talking("Thank you for navigating me through this journey.")
                    # Gets the name of the current machine user (account) 4th WALL BREAK
                    self.talking("Thank you {}".format(getpass.getuser()))
                    self.talking_speed_number = temp_speed
                    self.game_over("img/unofficial_ending.png")
                    
                # No
                elif no_button.is_pressed(mouse_pos, mouse_pressed):
                    self.talking("At least I got the thing I wanted.")
                    self.talking("And that is all there can be to it.")
                    self.talking("We both can rest now.")
                    self.talking_speed_number = temp_speed
                    self.game_over("img/unofficial_ending.png")
                
                # Buttons
                self.screen.blit(yes_button.image, yes_button.rect)
                self.screen.blit(no_button.image, no_button.rect)
                
                # Updates
                self.clock.tick(FPS)
                pygame.display.update()

    def talking_with_teachers(self):
        """
        Player chatting with a teacher
        """
        
        if self.interacted[0] == "Teacher":

            # Liascinska
            if self.interacted[2] == 100 and self.interacted[1] == 19:

                # Before test 
                if self.mat_test: 
                    self.talking("LIA is just standing here.")
                    self.talking("MENACINGLY!")
                    self.talking("Oh, hey {}, fancy seeing you here.".format(self.player_name), True, LIGHTBLUE)
                    self.talking("School work can't be postponed.", True, LIGHTBLUE)
                    self.talking("I found something you can understand.", True, LIGHTBLUE)
                    math_values = self.quest.maths()
                    if isinstance(math_values, tuple): self.grades["MAT"], self.mat_test = math_values[0], math_values[1]
                
                # After test
                else: 

                    # Too many bananoks
                    if self.number_bananok > 120:
                        self.talking("Oh, hey {}.".format(self.player_name), True, LIGHTBLUE)
                        self.talking("Sorry I gotta grade test.", True, LIGHTBLUE)
                        self.talking("We can talk later.", True, LIGHTBLUE)

                    # Grading tests
                    else:
                        self.talking("Oh, hey {}.".format(self.player_name), True, LIGHTBLUE)
                        self.talking("I have a deal you may be interested in.", True, LIGHTBLUE) 
                        self.talking("You help me grade tests and I give you bananoks.", True, LIGHTBLUE)
                        self.talking("What do you say?", True, LIGHTBLUE)       

                        # Buttons
                        yes_button = Button(140, 190, 120, 50, fg=WHITE, bg=BLACK, content="Yes", fontsize=32)
                        no_button = Button(360, 190, 120, 50, fg=WHITE, bg=BLACK, content="No", fontsize=32)

                        deciding = True
                        
                        while deciding:

                            # Position and click of the mouse
                            mouse_pos = pygame.mouse.get_pos()
                            mouse_pressed = pygame.mouse.get_pressed()
                            
                            # Events
                            for event in pygame.event.get():

                                # Close button
                                if event.type == pygame.QUIT: self.exiting()

                                # Keyboard
                                elif event.type == pygame.KEYDOWN:

                                    # Esc
                                    if event.key == pygame.K_ESCAPE: deciding = False

                            if no_button.is_pressed(mouse_pos, mouse_pressed): 
                                deciding = False
                                self.draw(); self.update()
                                self.talking("Oh, I see. Well I have to do it by myself", True, LIGHTBLUE)

                            if yes_button.is_pressed(mouse_pos, mouse_pressed):
                                self.draw(); self.update()
                                self.talking("Thank you very much for your help.", True, LIGHTBLUE)
                                self.quest.grading_tests()
                                break

                            # Buttons
                            self.screen.blit(yes_button.image, yes_button.rect)
                            self.screen.blit(no_button.image, no_button.rect)
                            
                            # Updates
                            self.clock.tick(FPS)
                            pygame.display.update()  
                
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

                    # No chalks
                    if "chalks" not in list(self.inv.keys()) and "DEJ" not in list(self.grades.keys()): 
                        self.talking("Can you bring me chalks for the next lesson?", True)
                        self.talking("Thanks in advance", True)
                        self.talking("They should be in the first floor cabinet", True)
                        self.talking("On the right that is...", True)

                    # Yes chalks
                    elif "chalks" in list(self.inv.keys()):
                        self.talking("Thank you {}".format(self.player_name), True)
                        self.talking("I can give you any grade", True)
                        self.talking("Since I teach history...", True)
                        self.info("You've recieved a grade for history")
                        self.grades["DEJ"] = 1
                        self.inv.pop("chalks")

                    # Chatting
                    else: self.talking("Do you want to learn more about history?", True)
                        
            # Guydosova
            if self.interacted[2] == 94 and self.interacted[1] == 24:
                
                # Before test
                if "ANJ" not in list(self.grades.keys()):
                    self.talking(f"{self.player_name} I've got the test you didn't attend", True)
                    anj_values = self.quest.anglictina()
                    if isinstance(anj_values, tuple): self.grades["ANJ"], self.anj_test = anj_values[0], anj_values[1]
                    elif isinstance(anj_values, NoneType | bool): self.talking("Come back later", True); return
                    self.draw(); self.update()

                    # Grade talk
                    anj_grade = self.grades["ANJ"]
                    if anj_grade in (1, 2): self.talking("You got " + str(anj_grade) + ". I am proud of you.", True)
                    elif anj_grade == 3: self.talking("You got " + str(anj_grade) + ". Not great, not terrible.", True)
                    elif anj_grade in (4, 5): self.talking("You got " + str(anj_grade) + ". You need to practice more.", True)

                # Already took the test
                else: self.talking("Will you come to my kruzok?", True) # pls someone translate this  


            # Koky
            if self.interacted[2] == 111 and self.interacted[1] == 9:

                # Resistor
                if self.resistor:
                    self.talking("It's time for your AEN test today.", True, BLUE)
                    self.talking("I Hope you studied resistors yesterday.", True, BLUE)
                    self.grades["AEN"] = self.quest.resistor()
                    self.draw(); self.update()

                    # Grade talk
                    if self.grades["AEN"] == 1: self.talking("You did well my student, that's a 1 for you.", True, WHITE)
                    elif self.grades["AEN"] == 3: self.talking("Not the best, but I'll give you a 3.", True, WHITE)
                    elif self.grades["AEN"] == 5: self.talking("At least try. Sorry, but that's a 5!", True, WHITE)
                    self.resistor = False
                
                # 5 Minutes sooner
                elif not self.resistor and self.five_min_sooner:
                    self.talking("Can you let us go 5 minutes sooner?")
                    self.talking("No, I can't do that.", True)
                    self.talking("But I will let you go 10 minutes sooner.", True)
                    self.five_min_sooner = False
                
                # Talking with Koky while nothing interesting
                elif not self.five_min_sooner: self.talking("What are you still doing here?", True)

            # Michal (Ne)pusti
            if self.interacted[2] == 188 and self.interacted[1] == 13:

                # Already talked
                if not self.nepusti: self.talking("Would you like to learn more about Sie?", True)

                # Not yet done
                elif self.nepusti:

                    # Not completed misson
                    if type(self.connected_router) != list and len(self.grades) > 3:
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
                
                    # Didn't do much
                    else: 
                        self.talking("Sorry, I don't see the results", True)
                        self.talking("From other lessons", True)
                        self.talking("Come back when you're a bit...", True)
                        self.talking("Richer", True)
            
            # Whygusova
            elif self.interacted[2] == 77 and self.interacted[1] == 16:

                # Taking test
                if self.sjl_test:
                    self.talking("Oh, you're finally here", True, RED)
                    self.talking("Where have you been?", True, RED)
                    self.talking("I've been standing here waiting", True, RED)
                    self.talking("Nevermind. Finish this so I can move on", True, RED)
                    self.talking("Just fill in the blanks", True, RED)
                    sjl_test = self.quest.slovak_bs()
                    if isinstance(sjl_test, tuple): self.grades["SJL"], self.sjl_test = sjl_test[0], sjl_test[1]
                    self.draw(); self.update()

                    # Grade talk
                    if "SJL" in self.grades.keys():
                        if self.grades["SJL"] == 1: self.talking("You got 1. That's great.", True, RED)
                        elif self.grades["SJL"] == 2: self.talking("Nearly perfect. 2 is your grade.", True, RED)
                        elif self.grades["SJL"] in (3, 4, 5): 
                            self.talking("Of course, you didn't study for the test you didn't expect.", True, RED)
                            self.talking("None of you ever do." + str(self.grades["SJL"]) + ".", True, RED)
                        
                # OBN test 
                elif self.obn_test:
                    self.talking("Well while you're still here...", True, RED)
                    self.talking("You need a mark for OBN too.", True, RED)
                    
                    # Easy cop out if you found a referat
                    if "referat" in self.inv.keys():
                        self.talking("Is that a referat in your hand?", True, RED)
                        self.talking("What is it about?", True, RED)
                        self.talking("Uhh...")
                        self.talking("Oh, it's about the OSN!")
                        self.talking("And I made it myself!")
                        self.talking("Well, that makes my job easier.", True, RED)
                        self.talking("I'll just take it.", True, RED)
                        self.talking("And give you a mark.", True, RED)
                        self.inv.pop("referat")
                        self.grades["OBN"] = 1
                        self.obn_test = False
                        
                    # Other way if you don't have a referat
                    else: 
                        self.talking("I don't see that you made a referat.", True, RED)
                        self.talking("So I'll make sure to test you some other way.", True, RED)
                        self.grades["OBN"] = self.quest.obn_testo()
                        self.obn_test = False
                        if self.grades["OBN"] == 1: self.talking("I'll give you a 1. You did great.", True, RED)
                        elif self.grades["OBN"] == 2: self.talking("I'll give you a 2. That's not bad.", True, RED)
                        elif self.grades["OBN"] == 3: self.talking("I'll give you a 3. That's not the worst.", True, RED)
                        elif self.grades["OBN"] == 4: self.talking("I'll give you a 4. That's bad.", True, RED)
                        else: self.talking("Just go away! 5!", True, RED)
                        
                # After test
                else: self.talking("What do you want? Get lost", True, RED)
                
            # Martin šeky
            elif self.interacted[2] == 180 and self.interacted[1] == 5:

                # Quest here
                if self.osy:
                    self.talking("Oh, hey there", True, YELLOW)
                    self.talking("I wasn't planning to give you a test today", True, YELLOW)
                    self.talking("But while you're here", True, YELLOW)
                    self.talking("I think I should.", True, YELLOW)
                    osy_test = self.quest.bash()
                    if isinstance(osy_test, int): self.osy = not self.osy; self.grades["OSY"] = osy_test; self.talking("You can't leave without a mark", True, YELLOW)
                    else: self.talking("I'm not sure if I can help you with that", True, YELLOW); return
                    self.draw(); self.update()
                    

                    # After grade talk 
                    if self.grades["OSY"] == 1: self.talking("Good linux knowledge, that's a 1 for you.", True, YELLOW)
                    elif self.grades["OSY"] == 3: self.talking("You have a lot to learn, but I'll give you a 3.", True, YELLOW)

                # When quest completed
                else: self.talking("Hi, leave me alone i need to", True, YELLOW); self.talking("install Linux on this machine", True, YELLOW)
                
            # Kôňtura
            elif self.interacted[2] == 21 and self.interacted[1] == 3: 

                # Test
                if self.iot:
                    self.talking(f"Hello student {self.player_name},", True, BLUE)
                    self.talking("you missed the last lesson", True, BLUE)
                    self.talking("I have a test for you", True, BLUE)
                    self.talking("you have to take it or else you'll recieve an a.", True, BLUE)
                    iot_test = self.quest.iotest()
                    if isinstance(iot_test, int): self.grades["IOT"] = iot_test
                    else: self.talking("I need you to do this test later", True, BLUE); return
                    self.draw(); self.update()
                    self.iot = not self.iot

                    # After grade talk with Kôňtura
                    if self.grades["IOT"] == 1: self.talking("Good work my student, that's a 1 for you.", True, BLUE)
                    elif self.grades["IOT"] == 3: self.talking("You need to learn more about IoT my student.", True, BLUE); self.talking("But I'll give you a 3", True, BLUE); self.talking("since you missed the last lesson and are my student.", True, BLUE)
                    elif self.grades["IOT"] == 5: self.talking("Why would you give up, my student.", True, BLUE); self.talking("Oh, he seems very sad.")

                # Vtipnicek gone
                elif not self.vtipnicek: self.talking("Someone took my vtipnicek. Now I am not funny.", True, BLUE)

                # After test, vtipnicek in safe
                else: self.talking("Dang, those bad students broke my 3D printer.", True, BLUE)

            # Haramgozo
            elif self.interacted[2] == 8 and self.interacted[1] == 28: 
                self.talking("Ohm's law is used to calculate....", True, RED)
                self.talking("I rather leave him be.")
            
            # Mohyla
            elif self.interacted[2] == 190 and self.interacted[1] == 19:

                # Before test
                if self.icdl:
                    self.talking("Oh... hello Nosil", True, WHITE)
                    self.talking("Well you're not him, nevermind", True, WHITE)
                    self.talking("You still haven't done previous exam", True, WHITE)
                    self.talking("You can use my PC", True, WHITE)
                    icdl_test = self.quest.icdl()
                    if isinstance(icdl_test, int): self.icdl = False; self.grades["ICD"] = icdl_test; self.talking(f"I'll give you a {self.grades['ICD']} for effort", True, WHITE)
                    else: self.talking("I need you to do this test later", True, WHITE)

                # After test
                else: self.talking("Uh, let me be.", True, WHITE); self.talking("I have... Uh", True, WHITE); self.talking("Important work to do...", True, WHITE)
            
            # Bartin Moda
            elif self.interacted[2] == 25 and self.interacted[1] == 36:

                # Getting the key
                if len(self.grades) == ALL_GRADES and "master_key" not in self.inv.keys():
                    self.talking("So... you've finally finished the game.", True)
                    self.talking("You've done well, so in return.", True)
                    self.talking("I'll give you this key.", True)
                    self.info("You have revicieved the master key", GREEN)
                    self.inv["master_key"] = "img/master_key.png"

                # Not enough grades
                else: self.talking("This is not the time to chat.", True); self.talking("Come back later.", True)

            # Gabriela 2-metrova
            elif self.interacted[2] == 130 and self.interacted[1] == 26:

                # Before quest
                if self.closed_window:
                    self.talking("We finally entered the room.", True, YELLOW)
                    self.talking("You know what to do.", True, YELLOW)
                    self.talking("I hope you can reach the window.", True, YELLOW)

                # Completed quest
                else: self.talking("At least I teached you how to open window.", True, YELLOW)

            # HeadWeedGone Wa
            elif self.interacted[2] == 28 and self.interacted[1] == 1:
                
                # Has grade
                if "PRO" in self.grades.keys(): self.talking("Congrats on your test.", True, ORANGE)

                #  No grade? (insert megamind meme here)
                else: self.talking("I'll get to you in a minute.", True, ORANGE); self.talking("I need to find my rovnitko.", True, ORANGE)

            # Rolada
            elif self.interacted[2] == 42 and self.interacted[1] == 18: 

                # Lost fella
                if self.lost_guy:
                    self.talking("Yooo {}, I need your help".format(self.player_name), True, LIGHTBLUE)
                    self.talking("Someone got lost in school and I need you to find them.", True , LIGHTBLUE)
                    self.talking("Could be please do that?", True, LIGHTBLUE)

                else:
                    self.talking("Good job finding them.", True, LIGHTBLUE)
                    self.talking("Did you know that something similiar happened before?", True, LIGHTBLUE)
                    self.talking("It was few years back...", True, LIGHTBLUE)
                    self.talking("Oh no. He's at it again. Gotta go.")

            # Zo Sarisa
            elif self.interacted[1] == 7 and self.interacted[2] == 139:

                # Before praying
                if self.not_saint:
                    self.talking("Welcome my child.", True, SILVER)
                    self.talking("Will you pray with me?", True, SILVER)
                    self.quest.pray()

                # Did pray
                elif self.prayed:
                    self.talking("I am glad you prayed with me.", True, SILVER)
                    self.talking("May the Lord bless you.", True, SILVER)
                
                # Didn't pray
                elif not self.prayed:
                    self.talking("Why are you still here?", True, SILVER)
                    self.talking("I believe the Lord will forgive you.", True, SILVER)
                
    def shoes_on(self):
        """
        Checks if player has shoes on
        """

        if self.locker_stuff["crocs"] and self.caught >= 3: self.game_over("img/you_never_learn.png")
        elif self.locker_stuff["crocs"] and self.caught < 3: 
            self.caught += 1
            self.saved_room_data = "017"
            self.in_room = self.rooms[GROUND_FLOOR]
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
                if event.type == pygame.QUIT: sys.exit()

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

            # Phone
            if not looking and "phone" not in self.inv.keys():
                self.draw(); self.update()
                self.talking("Crap, I don't have my phone with me.")
                self.talking("I think I left it somewhere in our class.")
                self.info("Find your iPhone", GREEN)

            # Updates
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
        if self.in_room == self.rooms[GROUND_FLOOR]: self.ground_floor_doors()

        # First floor
        elif self.in_room == self.rooms[FIRST_FLOOR]: self.first_floor_doors()

        # Second floor
        elif self.in_room == self.rooms[SECOND_FLOOR]: self.second_floor_doors()  
        
        # Third floor
        elif self.in_room == self.rooms[THIRD_FLOOR]: self.third_floor_doors()
        
        # Fourth floor
        elif self.in_room == self.rooms[FOURTH_FLOOR]: self.fourth_floor_doors()
        
        # Ending hall
        elif self.in_room == self.rooms[ENDING_HALLWAY]: self.ending_hallway_doors()
        
        # Lyziarsky doors (with creating tile map)
        elif any(self.in_room for self.in_room in self.lyz_rooms): self.lyz_doors()

        # Lost guy
        elif self.in_room == self.rooms[BASEMENT_FLOOR] and self.interacted[1] == 4 and self.interacted[2] == 45 and self.lost_guy: self.quest.guy_lost_in_school()
        
               
    def basement(self):
        """
        Going into the basement
        """
        
        # Light in inventory
        if "flashlight" in self.inv.keys():

            # Going in
            self.talking("I got light with me.")
            self.talking("I'll be able to see now.")
            self.talking("Bravo six, going dark.")

            # From right
            if self.interacted[1] == 17 and self.interacted[2] in (193, 194):
                self.in_room = self.rooms[BASEMENT_FLOOR] # Basement
                self.create_tile_map()
                for sprite in self.all_sprites: sprite.rect.x -= 79 * TILE_SIZE

            # From left
            elif self.interacted[1] in (26, 27) and self.interacted[2] == 117:
                self.in_room = self.rooms[BASEMENT_FLOOR] # Basement
                self.create_tile_map()
                for sprite in self.all_sprites: sprite.rect.x += 9 * TILE_SIZE; sprite.rect.y -= 3 * TILE_SIZE
                self.player.rect.x -= 87 * TILE_SIZE
                self.player.rect.y += 3 * TILE_SIZE

            self.draw()
            self.update()

            if r.randint(1, 10) == 10: self.talking("Legend says this basement was"); self.talking("dug by David Baník in one day.")

        # No light
        else:

            if self.without_light <= 3:
                self.talking("No way I am going down there without light.")
                self.talking("I don't want to get lost in school.")
                self.talking("I'll go there when I have some light with me.")
                self.without_light += 1
            else:
                self.talking("Welp, you really want me to go down there?")
                self.talking("Let's see. Bravo six, going dark.")
                self.game_over("img/lost.png")

    def bookshelf(self):
        """
        Searching bookshelfs
        """

        self.talking("There is a lot of books.")

        # Otec IoT book
        if self.interacted[1] in (34, 35, 36) and self.interacted[2] == 85: self.otec_iot()

        # Kokosky
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
                if event.type == pygame.QUIT: sys.exit()

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
                    sprite.rect.x -= 174 * TILE_SIZE
                    sprite.rect.y -= 11 * TILE_SIZE
                self.player.rect.x += 15 * TILE_SIZE
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
            
            if self.interacted[1] in (27, 28, 29, 30) and self.interacted[2] == 181: 
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

        self.talking(f"Wash your hands afterwards {self.player_name}")

    def found_guy(self):
        """
        After you found the lost guy
        """

        self.g_leave = False
        self.g_move = False
        self.lost_guy = False
        self.player_follow = False
        self.in_room = self.rooms[GROUND_FLOOR]
        self.create_tile_map()
        for sprite in self.all_sprites: 
            sprite.rect.x -= 107 * TILE_SIZE
            sprite.rect.y -= 20 * TILE_SIZE
        self.player.rect.x -= 52 * TILE_SIZE
        self.player.rect.y += 20 * TILE_SIZE
        pygame.mixer.Sound.stop(self.guy)
        if self.music_on: pygame.mixer.Sound.play(self.theme)
        self.talking("", True, WHITE, True, 1)
        self.talking("Thanks for getting me out.", True, GOLD)
        self.talking("Where did he run off?")
        self.talking("And why was he spinning the entire time?")
        self.talking("So many question and no answers.")
        self.talking("Such is life at SPSE.")
        

# Main program
g = Game()
g.intro_screen().new("new").main()
sys.exit()