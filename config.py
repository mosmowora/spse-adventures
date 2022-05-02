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
GREEN: tuple =          (  0, 255,   0)
BLUE: tuple =           (  0,   0, 255)
GRAY: tuple =           ( 64,  64,  64)
DIM_GRAY: tuple =       (105, 105, 105)
DARK_GRAY: tuple =      ( 32,  32,  32)

# Floors
GROUND_FLOOR = 0
FIRST_FLOOR = 1
SECOND_FLOOR = 2
THIRD_FLOOR = 3
FOURTH_FLOOR = 4
BASEMENT_FLOOR = -1

# Basement
basement: List[str]  = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W.........W............W...........W...........W.........W............W......W....W......W",
    "W.........W............W...........W...........W.........W............W......W....W......W",
    "W.........W............W...........W...........W.........W............W......W....W......W",
    "WWWWWDWWWWWWWWWWDWWWWWWWWWWWWDWWWWWWWWWWWWWWWDWWWWWWWDWWWWWWWWWWDWWWWWWWWWDWWWWWDWWDWWWWWW",
    "W........................................................................................S",
    "W.......................................................................................PS",
    "W.......WWWWDWWWWWWWWWDWWWWWWWWDWWWWWWWWWWDWWWWWWWDWWWWWWWWWWDWWWWWWWWWWDWWWWWWWWWWDWWWWWW",
    "W.......W........W.........W........W.........W........W..........W..........W...........W",
    "S.......W........W.........W........W.........W........W..........W..........W...........W",
    "S.......W........W.........W........W.........W........W..........W..........W...........W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]

# HeHeHeHa
ground_floor: List[str] = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWwwwWWW______________________",
    "W.l..l..ll.W.ĺl..l..l.Wl..llll..lWl..llll..lWZZZZZZZř!!!!!!!!!!W.l..l..l..l..l..l.l.W..l..l..l..l..l..l.Wl....llll....lW..l..l..l..l..l..l..l.W..l..l..l..l..l..l...WĽ.....LW______________________",
    "W.l..l..ll.W.ll..l..l.Wl..llll..lWl..llll..lWZZZZZZZř!!!!!!!!!!W.l..l..l..l..l..l.l.W..l..l..l..l..l..l.Wl....llll....lW..l..l..l..l..l..l..l.W..l..l..l..l..l..l...WĽ..B..LW______________________",
    "W.l..l..l..W..l..l..l.Wl..llll..lWl..llll..lWZZZZZZZř!!!!!!!!!!W....................W...................Wl....llll....lW......................W.....................WĽ..B..LW______________________",
    "W.l..l..l..W..l..l..l.Wl..llll..lWl..llll..lWZZZZZZZř!!!!!!!!!!W....................W...................Wl....llll....lW......................W.....................WĽ..B..LW______________________",
    "W.l..l..l..W..l..l..l.Wl..llll..lWl..llll..lWZZZZZZZř!!!!!!!!!!W.l..l..l..l..l..l...W..l..l..l..l..l....Wl....llll....lW..l..l..l..l..l..l....W..l..l..l..l..l......WĽ..B..LW______________________",
    "W.l..l..l..W..l..l..l.Wl..llll..lWl..llll..lWZZZZZZZř!!!!!!!!!!W.l..l..l..l..l..l...W..l..l..l..l..l....Wl....llll....lW..l..l..l..l..l..l....W..l..l..l..l..l......WĽ..P..LW______________________",
    "W.l..l..l..W..l..l..l.Wl..llll..lWl..llll..lWZZZZZZZř!!!!!!!!!!W....................W...................Wl....llll....lW......................W.....................WĽ.....LW______________________",
    "W.l..l..l..W..l..l..l.Wl..llll..lWl..llll..lWZZZZZZZř!!!!!!!!!!W....................W...................Wl....llll....lW......................W.....................WB..B..LWWWWWWWWWWWWWWWWWWWWWWWW",
    "W.l..l..l..W..l..l..l.Wl..llll..lWl..llll..lWZZZZZZZř!!!!!!!!!!W.l..l..l..l..l..l...W..l..l..l..l..l....W..............W..l..l..l..l..l..l....W..l..l..l..l..l......WB..B..LW......................W",
    "W.l..l..l..W..l..l..l.Wl........lWl........lWZZZZZZZř!!!!!!!!!!W.l..l..l..l..l..l...W..l..l..l..l..l....W..............W..l..l..l..l..l..l....W..l..l..l..l..l......WB..B..LW......................W",
    "W..........W..........W..........WĽ........LWZZZZZZZř!!!!!!!!!!W....................W...................WĽ.............W......................W.....................WB..B..LW......................W",
    "W..........W..........W..........WĽ.........WZZZZZZZř!!!!!!!!!!W....................W...................WĽ............LW......................W.....................W......LW......................W",
    "W..........W..........W..........Wt.........WZZZZZZZř!!!!!!!!!!W...................tWt..................Wt............LW.....................tW....................tWt.....LW......................W",
    "WWWWWWWWWDWWWWWWWWWWDWWWDWWWWWWWWWWDWWWWWWWWW..................WWWWWWWWWWWWWWWWDWWWWWWWWDWWWWWWWWWWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWWWWWWDWWWWWWWDWWWWW......................W",
    "W..........W............................................................................................................................................................................ŘŘŘŘŘŘŘŘ!..W",
    "Wjjj.......W............................................................................................................................................................................SSSSSSSS!..W",
    "W..........D................................................................................................................................C...........................................SSSSSSSS!bbW",
    "Wjjjjjjj...W............................................................................................................................................................................SSSSSSSS!bbW",
    "W..........W............................................................................................................................................................................SSSSSSSS!??W",
    "W..........WWWWWWWWDWWWWWDWWWWWWWDWWWWWWW...................................WWWWWWWWWWWWDWWWWWWWDWWWWWWWWW...............WWDWWWWWWWWWDWWWWWWWWWWWWWWWWWWDWWWWWWDWWWWWWDWWWWWWWWWDWWWWWWWWWWWWWWWWWWW",
    "Wjjjjjjj...W!jjjjjj..tW.......tW....WTWTW...................................W.......W.......Wt...U.U.U.U.W...............W......Wt.....l.l.l.l.l.l...W......W......W.........W...............Ľ..C..W",
    "W..........Wl.........W........W....W.W.W...................................W.......W.......W....J.J.J.J.W...............W......W......l.l.l.l.l.l...W......W......W.........W...............Ľ.....W",
    "W..........Wl.........W........W....W.W.W...................................W.......W.......W............W...............W......W....................W......W......W.........W...............!!!!..W",
    "Wjjjjjjj...Wl.......l.W........W....WDWDW...................................W.......W.......W............W....ľľľľľľľľľľľW......W....................W......W......W.........W..................l..W",
    "W..........Wl.......l.W........W........W...................................D.......W.......W............W....WWWWWWWWWWWW......W......l..l..l.l.l...W......W......W.........W..................l..W",
    "W..........Wl.......l.W........W........W...................................W.......W.......W.l..U.U.U.U.W...........dd??W......W..l...l..l..l.l.l...W......W......W.........W...ll...ll...ll...l..W",
    "W..........W!jjjjjjj!.W........W........W...................................W.......W.......W.l..J.J.J.J.W...........dd??W......W..l...l..l..l.l.l...W......W......W.........W...ll...ll...ll...l..W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWGGWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWwWWwWWwWWwWWwWWWWwWWwWWWwWWWwwWWwwWWwwWWwwWWWwwwWWWWwWWwWWWwWwWwWwWWWwwWwwWwwWwwWwwWwwWwWW"
]

# HoHoHo
first_floor: List[str] = [
    "______________________________________________________________________________________________________________________________________________________________________WWwwwWWWWWWWWWWWWWWWWWWWWWW",
    "______________________________________________________________________________________________________________________________________________________________________W......W..................W",
    "______________________________________________________________________________________________________________________________________________________________________W......W....jjjjjjjjjjjjjjW",
    "______________________________________________________________________________________________________________________________________________________________________W......W..................w",
    "______________________________________________________________________________________________________________________________________________________________________W......W....jjjjjjjjjjjjjjW",
    "______________________________________________________________________________________________________________________________________________________________________W......W..................W",
    "______________________________________________________________________________________________________________________________________________________________________W......D....jjjjjjjjjjjjjjw",
    "______________________________________________________________________________________________________________________________________________________________________WWWDWWWWt.................W",
    "______________________________________________________________________________________________________________________________________________________________________w......WWWWDWWWWWWWWWWWWWWW",
    "______________________________________________________________________________________________________________________________________________________________________w......W..................w",
    "WWWWWwwWWWWWWWWwwWWWWWWwWWWWWwWWWWWwWWWWWwWWWWWwwWWWWWWWwWwWwWWWWWWwwwWWWwwwWWWWWWwWWwWWwWWwWWwWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW......W....jjjjjjjjjjjjjjW",
    "W..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W...l..l..l..l..l..W...l..l..l..l....W................W...l..l..l..l..l..W.........W...l..l..l..l...W.....W......w..................w",
    "W..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W...l..l..l..l..l..W...l..l..l..l..l.W................W...l..l..l..l..l..W.........W...l..l..l..l...W.....D......G....jjjjjjjjjjjjjjW",
    "W..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W..................W...............l.W................W..................W.........W..............l.WDW...W......G..................w",
    "W..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W..................W...............l.W................W..................W.........W..............l.W.W...W......w....jjjjjjjjjjjjjjW",
    "w..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W..l..l..l..l..l...W..l..l..l..l...l.W................W....l..l..l..l....W.........W..l..l..l..l.l..WŤW...W......W..................W",
    "w..........W........W.....W..l..W..l..W..l..WZZZZZZZrzzzzzzzW..l..l..l..l..l...W..l..l..l..l.....W................W....l..l..l..l....W.........W..l..l..l..l.l..WWWWWWW......WWWWWWWWWWWWWWWWWWWW",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..................W.................W................W..................W.........W................W.....W......W..................w",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..................W.................W................W..................W.........W................W.....W......D..................w",
    "w..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW...l..l..l..l..l..W...l..l..l..l....W..N.............W..................W.........W................W.....W......W..................W",
    "w..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW...l..l..l..l..l..W...l..l..l..l....W................W...l..l..l..l..l..W.........W...l..l..l..l...W.....W......WWWWWWWWWWWWWWWWWWWW",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..................W.................D................W...l..l..l..l..l..W.........W...l..l..l..l...WWWWWWW..............sssssssssssW",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..................W.................W................W..................W.........W................W.....W..............sssssssssssW",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW.................tWt................W...............tWt.................W.........W................W.....W.............PsssssssssssW",
    "W..........WWWWWWWWWWWWDWWWWWDWWWWWDWWWWWDWWWZZZZZZZrzzzzzzzWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWDWWWWWWWDWWWWWWWWWWWWWWWWWWDWWWWWWWWWWWt.............sssssssssssW",
    "W..........W.........................................................................................................................................................................RRRRRRRRRRRW",
    "w..........W.........................................................................................................................................................................SSSSSSSSSSSw",
    "w..........D.........................................................................................................................................................................SSSSSSSSSSSW",
    "W..........W.........................................................................................................................................................................SSSSSSSSSSSw",
    "W..........W.........................................................................................................................................................................SSSSSSSSSSSW",
    "w..........WWWWWDWWWWWW.....WWDWWWDWWWDWWWDWW..........................WWWDWWWWWWDWWWWWWWWWWWWWWWWWWWWWWDWWWWWWDWWWWWWWDWWWWWWDWWWWWWWWWWWWWWDWWWWWWWWWWWDWWWWWWDWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "w..........W..........W.....W...W...W...W...W..........................W......W.....WoóóóóóóóóóóóóóóóW.....W.......W.......W.............W.............W...W.......l..l..l..l..l..l..l.....W....W",
    "W..........W..........W.....W...W...W...W...W..........................W......W.....Wo..............ÓW.....W.......W.......W.............W.............D...D.......l..l..l..l..l..l..l..........W",
    "W..........W..........W.....W...W...W...W...W..........................W......W.....Wo..............ÓW.....W.......W.......W.............W.............WWDWW...............................W....W",
    "w..........W..........W.....W...W...W...W...W..........................W......W.....Wo..............ÓW.....W.......W.......W.............W.............W...W..........l..l..l..l..l..l..l..WWWWWW",
    "w..........W..........W.....W...W...W...W...W..........................W......W.....Wo..............ÓW.....W.......W.......W.............W.............W...W..........l..l..l..l..l..l..l..W?????",
    "W..........W..........W.....W...W...W...W...W..........................W......W.....Wo.....................W.......W.......W.............W.............W...W...............................W?????",
    "W..........W..........W.....W...W...W...W...W..........................W......W.....Wo.....................W.......W.......W.............W.............W...W...l...l..l..l..l..l..l..l..l..W?????",
    "Wt.........W..........W.....W...W...W...W...W.........................tW......W.....WOOOOOOOOOOOOOOOOW.....W.......W.......W.............W.............W...Wt..l...l..l..l..l..l..l..l..l..W?????",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWwWWWwWWWwWWWwWWWWwwWWWwwWWWwwWWWwwWWWwwWWWWWwwWWWWwwwWWWWWwwwwWWwwwwWWwwwwWWWWWWwwwWWWWWwwwWWWWWWwwWWWwwWWWWWWWwwWWWWwwWWWWwWWWWwwWWWWwwWWWwwWWWWwwWWWWwwWWWWW?????",
]

# IIIIIIIIIi
second_floor: List[str] = [
    "______________________________________________________________________________________________________________________________________________________________________WWwwwWWWWWWWWWWWWWWWWWWWWWW",
    "______________________________________________________________________________________________________________________________________________________________________W.........................W",
    "______________________________________________________________________________________________________________________________________________________________________W......Wjjjjjjj....jjjjjjjW",
    "______________________________________________________________________________________________________________________________________________________________________W.........................W",
    "______________________________________________________________________________________________________________________________________________________________________W..................jjjjjjjW",
    "______________________________________________________________________________________________________________________________________________________________________W......Wjjjjjjj...........W",
    "______________________________________________________________________________________________________________________________________________________________________W.........................W",
    "______________________________________________________________________________________________________________________________________________________________________W..................jjjjjjjw",
    "______________________________________________________________________________________________________________________________________________________________________W......Wjjjjjjj...........W",
    "______________________________________________________________________________________________________________________________________________________________________W.........................W",
    "______________________________________________________________________________________________________________________________________________________________________W..................jjjjjjjw",
    "______________________________________________________________________________________________________________________________________________________________________W......Wjjjjjjj...........W",
    "______________________________________________________________________________________________________________________________________________________________________Wt...................jjjjjW",
    "______________________________________________________________________________________________________________________________________________________________________w.........................w",
    "WWWWWwwWWWWWWWWwwWWWWWWwWWWWWwWWWWWwWWWWWwWWWWWwwWWWWWWWwWwWwWWWWWWwwwWWWwwwWWWWWWwWWwWWwWWwWWwWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWWWWWW",
    "W..........W..l..l..l..l.W.l..l..l..l..l..l.W!!!!!!!!!!!!!!!W.l..l..l..l..l....W..l..l..l..l.....W................W..l..l..l..l......Wt........W.l..l..l..l.....W.....W......W..................W",
    "Wjj........W..l..l..l..l.W.l..l..l..l..l..l.W!!!!!!!!!!!!!!!W.l..l..l..l..l....W..l..l..l..l.....W................W..l..l..l..l......W.........W.l..l..l..l.....WDW...D......W..................w",
    "W........jjW.............W..................W!!!!!!!!!!!!!!!W..................W.................W................W..................W.........W................W.W...W......W..................w",
    "wjj........W.............W..................W!!!!!!!!!!!!!!!W..................W.................W................W..................W.........W................WŤW...W......W..................W",
    "W..........W..l..l..l....W.l..l..l..l..l....WZZZZZZZŔzzzzzzzW.l..l..l..l..l....W..l..l..l..l.....W................W..l..l..l..l......W.........W.l..l..l..l.....WWWWWWW......D..................w",
    "wjj......jjW..l..l..l....W.l..l..l..l..l....WZZZZZZZŔzzzzzzzW.l..l..l..l..l....W..l..l..l..l.....W................W..l..l..l..l......W.........W.l..l..l..l.....W.....D......W..................W",
    "w..........W.............W..................WZZZZZZZŔzzzzzzzW..................W.................W................W..................W.........W................W.....W......WWWWWWWWWWWWWWWWWWWW",
    "WWWWWWWWDWWW.............W..................WZZZZZZZŔzzzzzzzW..................W.................W................W..................W.........W................WWWWWWW..............sssssssssssW",
    "W..........W..l..l..l....W.l..l..l..l..l....WZZZZZZZŔzzzzzzzW.l..l..l..l..l....W..l..l..l..l.....W................W..l..l..l..l......W.........W.l..l..l..l.....W.....W..............sssssssssssW",
    "Wjjj.......W..l..l..l....W.l..l..l..l..l....WZZZZZZZŔzzzzzzzW.l..l..l..l..l...tW..l..l..l..l....tW...............tW..l..l..l..l.....tW.........W.l..l..l..l.....W.... W.............PsssssssssssW",
    "W..........WWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWDWWŘŘŘŘŘŘŘŕzzzzzzzWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWDWWWWwwwwwwwwwwGGwwwwWWWWWWWWWWWWWWDWWWWWWWWWDWWWWWWWWWWWWWWWWWWDWWWWWWWWWt.............sssssssssssW",
    "W..........W.........................................................................................................................................................................RRRRRRRRRRRW",
    "wjj.....jj.W.........................................................................................................................................................................SSSSSSSSSSSw",
    "w..........D.........................................................................................................................................................................SSSSSSSSSSSW",
    "W..........W.........................................................................................................................................................................SSSSSSSSSSSw",
    "Wjj.....jj.W.........................................................................................................................................................................SSSSSSSSSSSW",
    "w..........WWWWWDWWWWWWWWWWWWWWWWWWWDWWWDWWWWW....................WWWDWWWWWWDWWWWWDWWWWWWWWWWDWWWWWDWWWWWWWWWWDWWWWWWDWWWWWWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "w..........W......l..l..l..l..l..W....W..WTWTW...................!W......W.....W.........W.......W......W.........W.....l..l..l..l...W......l..l..l..l...W.........l..l..l..l..l..l..l.....W....W",
    "Wjj.....jj.W......l..l..l..l..l..W....W..W.W.W....................W......W.....W.........W.......W......W.........W.....l..l..l..l...W......l..l..l..l...W.........l..l..l..l..l..l..l.....D....W",
    "W..........W.....................W....W..WDWDW....................W......W.....W.........W.......W......W.........W..................W...................W.................................W....W",
    "w..........W.....................W....W......W.!....!.....!.....!.W......W.....W.........W.......W......W.........W..................W...................W.................................WWWWWW",
    "wjj.....jj.W.......l..l..l..l....W....W......W.!....!.....!.....!.W......W.....W.........W.......W......W.........W..................W...................W.................................W?????",
    "w..........W.......l..l..l..l....W....W......W.!....!.....!.....!.W......W.....W.........W.......W......W.........W..................W...................W.................................W?????",
    "W..........W..l..................W....W......W.!!!!!.......!!!!!..W......W.....W.........W.......W......W.........W.....l..l..l..l...W....l..l..l..l..l..W.........l..l..l..l..l..l..l.....W?????",
    "Wt.........W..l..................W....W......W...................tW......W.....W.........W.......W......W.........W.....l..l..l..l...W....l..l..l..l..l..W.........l..l..l..l..l..l..l..WWWW?????",
    "WWWWwwWWWWWWWWwwWWWWWWWWWWWWWWwWWWWWwWWWWWwWWWWwwWWWwwWWWwwWWWwwWWWwwWWWWWWwWWWWWwwWWWwwwWWWwwWwWWwwwwWWWWWWwwwWWWWWwwwWWWWWWwwWWWwwWWWWWWWwwWWWWwwWWWWwWWWWwwWWWWwwWWWwwWWWWwwWWWwwWWWWWWWW?????",
]

# Third floor
third_floor: List[str] = [
    "WWWWWWWWWWWWWwwWWWWwwwWWwwwWWwwwWWwwwWWwwwWWwwwWWwwwWWWWWWwwwWWWWWWWWWWWWWWWWWWWWWWW",
    "W..........W..........................................WB.......BW..................W",
    "W..........W.............Y............................WB.......BW..................W",
    "W..........W.............y............................WB.......BW..................W",
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
    "WWWwwwWWwwwWWwwwWWWwwwWWwwwWWwwwWWwwwWWwwwWWwwwWWwwwWWWWWwwWwwWWWwwWwwWWWWWWWWWWWWWW"
]

# Fourth floor
fourth_floor: List[str] = [
    "WWWWWWWWWWWWWwwWWWWwwwWWwwwWWwwwWWwwwWWwwwWWwwwWWwwwWWWWWWwwwWWWWWWWWWWWWWWWWWWWWWWW",
    "W..........W.!jj!....jjjjjjjjjjjjjjjjjjjjjjjjjjj..l...W.........W..................W",
    "W..........W.l..l.................................g...W.........W..................W",
    "W..........W.!jj!.....................................W.........W..................W",
    "W..........D..........................................W.........W..................W",
    "W..........W.........jjjjjjjjjjjjjjjjjjjjjjjjjjjjj....D.........W..................W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW.........W..................W",
    "??????????????????????????????????????????????????????Wt........WWWWDWWWWWWWWWWWWWWW",
    "??????????????????????????????????????????????????????W........D........sssssssssssW",
    "??????????????????????????????????????????????????????WWWWWWWWW.........sssssssssssW",
    "??????????????????????????????????????????????????????Wjjjjjjjj........PsssssssssssW",
    "??????????????????????????????????????????????????????WB................sssssssssssW",
    "??????????????????????????????????????????????????????WB................|//////////W",
    "??????????????????????????????????????????????????????WB................ř!!!!!!!!!!w",
    "??????????????????????????????????????????????????????WB................ř!!!!!!!!!!W",
    "??????????????????????????????????????????????????????W.................ř!!!!!!!!!!w",
    "??????????????????????????????????????????????????????Wt................ř!!!!!!!!!!W",
    "??????????????????????????????????????????????????????WWWWWWWWDWWWWWWWWWWWWWWWWWWWWW",
    "??????????????????????????????????????????????????????W........l..l..l..l..l..l...!W",
    "??????????????????????????????????????????????????????W........l..l..l..l..l..l...!W",
    "??????????????????????????????????????????????????????W........l..l..l..l..l..l....W",
    "??????????????????????????????????????????????????????W....l.......................W",
    "??????????????????????????????????????????????????????W..N.l......................!W",
    "??????????????????????????????????????????????????????W....l......................!W",
    "??????????????????????????????????????????????????????W....l...l..l..l..l..l..l....W",
    "??????????????????????????????????????????????????????W....!...l..l..l..l..l..l....W",
    "??????????????????????????????????????????????????????W....!...l..l..l..l..l..l....W",
    "??????????????????????????????????????????????????????WWwWWwwwWWwwwWWwwwWWwwwWWwwwWW"
]