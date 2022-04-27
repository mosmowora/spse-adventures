# Import
from typing import List

# Sizes
WIN_WIDTH: int = 640
WIN_HEIGHT: int = 480
TILE_SIZE: int = 32

# Fps
FPS: int = 60

# Layers
PLAYER_LAYER: int = 5
NPC_LAYER: int = 4
OBJECT_LAYER: int = 3
BLOCK_LAYER: int = 2
GROUND_LAYER: int = 1

# Speeds
PLAYER_SPEED: int = 5
NPC_SPEED: int = 3

# Colors
WHITE: tuple =          (255, 255, 255)
BLACK: tuple =          (  0,   0,   0)
NEARLY_BLACK: tuple =   (  1,   1,   1)
RED: tuple =            (255,   0,   0)
BLUE: tuple =           (  0,   0, 255)
GRAY: tuple =           ( 64,  64,  64)
DIM_GRAY: tuple =       (105, 105, 105)

basement: List[str]  = [
    "???????????????????????????",
    "???????????????????????????",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W!!W!!W!!W!!W!!W!!W!!W!!W.W",
    "W!!W!!W!!W!!W!!W!!W!!W!!W.W",
    "W.........................W",
    "S.........................S",
    "S........................PS",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWW"
]

# HeHeHeHa
ground_floor: List[str] = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWwwwWWW______________________",
    "W..........W..........W..........W..........WZZZZZZZř!!!!!!!!!!W....................W...................W..............W......................W.....................WĽ.....LW______________________",
    "W..........W..........W..........W..........WZZZZZZZř!!!!!!!!!!W....................W...................W..............W......................W.....................WĽ..B..LW______________________",
    "W..........W..........W..........W..........WZZZZZZZř!!!!!!!!!!W....................W...................W..............W......................W.....................WĽ..B..LW______________________",
    "W..........W..........W..........W..........WZZZZZZZř!!!!!!!!!!W....................W...................W..............W......................W.....................WĽ..B..LW______________________",
    "W..........W..........W..........W..........WZZZZZZZř!!!!!!!!!!W....................W...................W..............W......................W.....................WĽ..B..LW______________________",
    "W..........W..........W..........W..........WZZZZZZZř!!!!!!!!!!W....................W...................W..............W......................W.....................WĽ..P..LW______________________",
    "W..........W..........W..........W..........WZZZZZZZř!!!!!!!!!!W....................W...................W..............W......................W.....................WĽ.....LW______________________",
    "W..........W..........W..........W..........WZZZZZZZř!!!!!!!!!!W....................W...................W..............W......................W.....................WB..B..LWWWWWWWWWWWWWWWWWWWWWWW",
    "W..........W..........W..........W..........WZZZZZZZř!!!!!!!!!!W....................W...................W..............W......................W.....................WB..B..LW.....................W",
    "W..........W..........W..........W..........WZZZZZZZř!!!!!!!!!!W....................W...................W..............W......................W.....................WB..B..LW.....................W",
    "W..........W..........W..........W..........WZZZZZZZř!!!!!!!!!!W....................W...................W..............W......................W.....................WB..B..LW.....................W",
    "W..........W..........W..........W..........WZZZZZZZř!!!!!!!!!!W....................W...................W..............W......................W.....................W......LW.....................W",
    "W..........W..........W..........W..........WZZZZZZZř!!!!!!!!!!W...................tWt..................Wt.............W.....................tW....................tWt...NNLW.....................W",
    "WWWWWWWWWDWWWWWWWWWWDWWWDWWWWWWWWWWDWWWWWWWWW..................WWWWWWWWWWWWWWWWDWWWWWWWWDWWWWWWWWWWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWWWWWWDWWWWWWWDWWWWW.....................W",
    "W..........W...........................................................................................................................................................................ŘŘŘŘŘŘŘŘ!..W",
    "W..........W...........................................................................................................................................................................SSSSSSSS!..W",
    "W..........D................................................................................................................................C..........................................SSSSSSSS!bbW",
    "W..........W...........................................................................................................................................................................SSSSSSSS!bbW",
    "W..........W...........................................................................................................................................................................SSSSSSSS!??W",
    "W..........WWWWWWWWDWWWWWDWWWWWWWDWWWWWWW...................................WWWWWWWWWWWWDWWWWWWWDWWWWWWWW...............WWWDWWWWWWWWWDWWWWWWWWWWWWWWWWWWDWWWWWWDWWWWWWDWWWWWWWWWDWWWWWWWWWWWWWWWWWW",
    "W..........W..........W........W....WTWTW...................................W.......W.......Wt..........W...............W......Wt...................W......W......W.........W.....................W",
    "W..........W..........W........W....W.W.W...................................W.......W.......W...........W...............W......W....................W......W......W.........W.....................W",
    "W..........W..........W........W....W.W.W...................................W.......W.......W...........W...............W......W....................W......W......W.........W.....................W",
    "W..........W..........W........W....WDWDW...................................W.......W.......W...........W...ľľľľľľľľľľľľW......W....................W......W......W.........W.....................W",
    "W..........W..........W........W........W...................................D.......W.......W...........W...WWWWWWWWWWWWW......W....................W......W......W.........W.....................W",
    "W..........W..........W........W........W...................................W.......W.......W...........W...........dd??W......W....................W......W......W.........W.....................W",
    "W..........W..........W........W........W...................................W.......W.......W...........W...........dd??W......W....................W......W......W.........W.....................W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWGGWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]

# HoHoHo
first_floor: List[str] = [
    "______________________________________________________________________________________________________________________________________________________________________WWwwwWWWWWWWWWWWWWWWWWWWWWW",
    "______________________________________________________________________________________________________________________________________________________________________W......W..................W",
    "______________________________________________________________________________________________________________________________________________________________________W......W..................W",
    "______________________________________________________________________________________________________________________________________________________________________W......W..................w",
    "______________________________________________________________________________________________________________________________________________________________________W......W..................W",
    "______________________________________________________________________________________________________________________________________________________________________W......W..................W",
    "______________________________________________________________________________________________________________________________________________________________________W......D..................w",
    "______________________________________________________________________________________________________________________________________________________________________WWWDWWWWt.................W",
    "______________________________________________________________________________________________________________________________________________________________________w......WWWWDWWWWWWWWWWWWWWW",
    "______________________________________________________________________________________________________________________________________________________________________w......W..................w",
    "WWWWWwwWWWWWWWWwwWWWWWWwWWWWWwWWWWWwWWWWWwWWWWWwwWWWWWWWwWwWwWWWWWWwwwWWWwwwWWWWWWwWWwWWwWWwWWwWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW......W..................W",
    "W..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W..................W.................W................W..................W.........W................W.....W......w..................w",
    "W..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W..................W.................W................W..................W.........W................W.....D......G..................W",
    "W..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W..................W.................W................W..................W.........W................WDW...W......G..................w",
    "W..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W..................W.................W................W..................W.........W................W.W...W......w..................w",
    "w..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W..................W.................W................W..................W.........W................WŤW...W......W..................W",
    "w..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..................W.................W................W..................W.........W................WWWWWWW......WWWWWWWWWWWWWWWWWWWW",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..................W.................W................W..................W.........W................W.....W......W..................w",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..................W.................W................W..................W.........W................W.....W......D..................w",
    "w..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..................W.................W................W..................W.........W................W.....W......W..................W",
    "w..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..................W.................W................W..................W.........W................W.....W......WWWWWWWWWWWWWWWWWWWW",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..................W.................W................W..................W.........W................WWWWWWW..............sssssssssssW",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..................W.................W................W..................W.........W................W.....W..............sssssssssssW",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW.................tWt................W...............tWt.................W.........W................W.....W.............PsssssssssssW",
    "W..........WWWWWWWWWWWWDWWWWWDWWWWWDWWWWWDWWWZZZZZZZrzzzzzzzWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWDWWWWWWWDWWWWWWWWWWWWWWWWWWDWWWWWWWWWWWt.............sssssssssssW",
    "W..........W.........................................................................................................................................................................RRRRRRRRRRRW",
    "w..........W.........................................................................................................................................................................SSSSSSSSSSSw",
    "w..........D.........................................................................................................................................................................SSSSSSSSSSSW",
    "W..........W.........................................................................................................................................................................SSSSSSSSSSSw",
    "W..........W.........................................................................................................................................................................SSSSSSSSSSSW",
    "w..........WWWWWDWWWWWW.....WWDWWWDWWWDWWWDWW..........................WWWDWWWWWWDWWWWWWWWWWWWWWWWWWWWWWDWWWWWWDWWWWWWWDWWWWWWDWWWWWWWWWWWWWWDWWWWWWWWWWWDWWWWWWDWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "w..........W..........W.....W...W...W...W...W..........................W......W.....W......................W.......W.......W.............W.............W...W...............................W....W",
    "W..........W..........W.....W...W...W...W...W..........................W......W.....W......................W.......W.......W.............W.............D...D....................................W",
    "W..........W..........W.....W...W...W...W...W..........................W......W.....W......................W.......W.......W.............W.............WWDWW...............................W....W",
    "w..........W..........W.....W...W...W...W...W..........................W......W.....W......................W.......W.......W.............W.............W...W...............................WWWWWW",
    "w..........W..........W.....W...W...W...W...W..........................W......W.....W......................W.......W.......W.............W.............W...W...............................W?????",
    "W..........W..........W.....W...W...W...W...W..........................W......W.....W......................W.......W.......W.............W.............W...W...............................W?????",
    "Wt.........W..........W.....W...W...W...W...W.........................tW......W.....W......................W.......W.......W.............W.............W...Wt..............................W?????",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWwWWWwWWWwWWWwWWWWwwWWWwwWWWwwWWWwwWWWwwWWWWWwwWWWWwwwWWWWWwwwwWWwwwwWWwwwwWWWWWWwwwWWWWWwwwWWWWWWwwWWWwwWWWWWWWwwWWWWwwWWWWwWWWWwwWWWWwwWWWwwWWWWwwWWWWwwWWWWW?????",
]

# IIIIIIIIIi
second_floor: List[str] = [
    "______________________________________________________________________________________________________________________________________________________________________WWwwwWWWWWWWWWWWWWWWWWWWWWW",
    "______________________________________________________________________________________________________________________________________________________________________W.........................W",
    "______________________________________________________________________________________________________________________________________________________________________W.........................W",
    "______________________________________________________________________________________________________________________________________________________________________W.........................W",
    "______________________________________________________________________________________________________________________________________________________________________W.........................W",
    "______________________________________________________________________________________________________________________________________________________________________W.........................W",
    "______________________________________________________________________________________________________________________________________________________________________W.........................W",
    "______________________________________________________________________________________________________________________________________________________________________W.........................w",
    "______________________________________________________________________________________________________________________________________________________________________W.........................W",
    "______________________________________________________________________________________________________________________________________________________________________W.........................W",
    "______________________________________________________________________________________________________________________________________________________________________W.........................w",
    "______________________________________________________________________________________________________________________________________________________________________Wt........................W",
    "______________________________________________________________________________________________________________________________________________________________________W.........................W",
    "______________________________________________________________________________________________________________________________________________________________________w.........................w",
    "WWWWWwwWWWWWWWWwwWWWWWWwWWWWWwWWWWWwWWWWWwWWWWWwwWWWWWWWwWwWwWWWWWWwwwWWWwwwWWWWWWwWWwWWwWWwWWwWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWWWWWW",
    "W..........W.............W..................W!!!!!!!!!!!!!!!W..................W.................W................W..................Wt........W................W.....W......W..................W",
    "W..........W.............W..................W!!!!!!!!!!!!!!!W..................W.................W................W..................W.........W................WDW...D......W..................w",
    "W..........W.............W..................W!!!!!!!!!!!!!!!W..................W.................W................W..................W.........W................W.W...W......W..................w",
    "w..........W.............W..................W!!!!!!!!!!!!!!!W..................W.................W................W..................W.........W................WŤW...W......W..................W",
    "W..........W.............W..................WZZZZZZZŔzzzzzzzW..................W.................W................W..................W.........W................WWWWWWW......D..................w",
    "w..........W.............W..................WZZZZZZZŔzzzzzzzW..................W.................W................W..................W.........W................W.....D......W..................W",
    "w..........W.............W..................WZZZZZZZŔzzzzzzzW..................W.................W................W..................W.........W................W.....W......WWWWWWWWWWWWWWWWWWWW",
    "WWWWWWWWDWWW.............W..................WZZZZZZZŔzzzzzzzW..................W.................W................W..................W.........W................WWWWWWW..............sssssssssssW",
    "W..........W.............W..................WZZZZZZZŔzzzzzzzW..................W.................W................W..................W.........W................W.....W..............sssssssssssW",
    "W..........W.............W..................WZZZZZZZŔzzzzzzzW.................tWt................W...............tWt.................W.........W................W.... W.............PsssssssssssW",
    "W..........WWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWDWWŘŘŘŘŘŘŘŕzzzzzzzWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWDWWWWWWWWWDWWWWWWWWWWWWWWWWWWDWWWWWWWWWt.............sssssssssssW",
    "W..........W.........................................................................................................................................................................RRRRRRRRRRRW",
    "w..........W.........................................................................................................................................................................SSSSSSSSSSSw",
    "w..........D.........................................................................................................................................................................SSSSSSSSSSSW",
    "W..........W.........................................................................................................................................................................SSSSSSSSSSSw",
    "W..........W.........................................................................................................................................................................SSSSSSSSSSSW",
    "w..........WWWWWDWWWWWWWWWWWWWWWWWWWDWWWDWWWWW....................WWWDWWWWWWDWWWWWDWWWWWWWWWWDWWWWWDWWWWWWWWWWDWWWWWWDWWWWWWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "w..........W.....................W....W..WTWTW...................!W......W.....W.........W.......W......W.........W..................W...................W.................................W....W",
    "W..........W.....................W....W..W.W.W....................W......W.....W.........W.......W......W.........W..................W...................W.................................D....W",
    "W..........W.....................W....W..WDWDW.!....!.....!.....!.W......W.....W.........W.......W......W.........W..................W...................W.................................W....W",
    "w..........W.....................W....W......W.!....!.....!.....!.W......W.....W.........W.......W......W.........W..................W...................W.................................WWWWWW",
    "w..........W.....................W....W......W.!....!.....!.....!.W......W.....W.........W.......W......W.........W..................W...................W.................................W?????",
    "W..........W.....................W....W......W.!!!!!.......!!!!!..W......W.....W.........W.......W......W.........W..................W...................W.................................W?????",
    "Wt.........W.....................W....W......W...................tW......W.....W.........W.......W......W.........W..................W...................W..............................WWWW?????",
    "WWWWwwWWWWWWWWwwWWWWWWWWWWWWWWwWWWWWwWWWWWwWWWWwwWWWwwWWWwwWWWwwWWWwwWWWWWWwWWWWWwwWWWwwwWWWwwWwWWwwwwWWWWWWwwwWWWWWwwwWWWWWWwwWWWwwWWWWWWWwwWWWWwwWWWWwWWWWwwWWWWwwWWWwwWWWWwwWWWwwWWWWWWWW?????",
]

# Third floor
third_floor: List[str] = [
    "WWWWWWWWWWWWWwwWWWWwwwWWwwwWWwwwWWwwwWWwwwWWwwwWWwwwWWWWWWwwwWWWWWWWWWWWWWWWWWWWWWWW",
    "W..........W.............R............................WB.......BW..................W",
    "W..........W.............B............................WB.......BW..................W",
    "W..........W.............B............................WB.......BW..................W",
    "W..........W..........................................WB.......BWWWWWWW............W",
    "W..........W..........................................D........BW.....W............W",
    "W..........WWWWWDDWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW......W.....D............W",
    "W.....................................................W..D......W.....WWWWWWWWWWWWWW",
    "W.....................................................WŤ.W.....D........sssssssssssW",
    "W.....................................................WWWWWWWWW.........sssssssssssW",
    "W.....................................................W................PsssssssssssW",
    "W.....................................................D.................sssssssssssW",
    "W.....................................................D.................RRRRRRRRRRRW",
    "W.....................................................W.................SSSSSSSSSSSw",
    "W.....................................................W.................SSSSSSSSSSSW",
    "W.....................................................W.................SSSSSSSSSSSw",
    "W.....................................................W.................SSSSSSSSSSSW",
    "W.....................................................W.................WWWWWWWWWWWW",
    "W.....................................................WWWWWWWWWWWWWDWWWWW..........W",
    "W.....................................................WB...............BW..........W",
    "W.....................................................WB...............BW..........W",
    "W.....................................................WB...............BW..........W",
    "W.....................................................WB...............BW..........W",
    "W.....................................................WB...............BW..........W",
    "W.....................................................WB...............BW..........W",
    "W.....................................................D.................D..........W",
    "W.....................................................W.................W..........W",
    "WWWwwwWWwwwWWwwwWWWwwwWWwwwWWwwwWWwwwWWwwwWWwwwWWwwwWWWWWWwwWwwWWwwWwwWWWWWWWWWWWWWW"
]