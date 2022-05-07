# Import
from typing import List

# Sizes
WIN_WIDTH: int = 640
WIN_HEIGHT: int = 480
TILE_SIZE: int = 32

# Fps
FPS: int = 50

# Layers
PLAYER_LAYER: int = 5
NPC_LAYER: int = 4
OBJECT_LAYER: int = 3
BLOCK_LAYER: int = 2
GROUND_LAYER: int = 1

# Speeds
PLAYER_SPEED: int = 10
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
NAVY: tuple =           ( 11,  19,  30)
BRITISH_WHITE: tuple =  (237, 225, 187)

# Floors
GROUND_FLOOR = 0
FIRST_FLOOR = 1
SECOND_FLOOR = 2
THIRD_FLOOR = 3
FOURTH_FLOOR = 4
BASEMENT_FLOOR = -1

# Number of quests to go home
ALL_QUESTS: int = 8

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
    "WWwwWWwwWWWWWwwWwwWwwWWWwwWwwWwwWWwwWwwWwwWWWWWWWWWWWWWWWWWWWWWWWwWWwwWWwwWWwwWWwwWWWWWwwWWwwWWwwWWwwWWWWWwwWwwWwwWwwWWWWWWWWWWWWWWWWWWWWWWWWWWWwWWwWWwWWwWWwWWwWWwWWWWwwwWWW______________________",
    "W.u..u..uk.W.él..l..l.Wl..ukel..uWl..ukel..uWZZZZZZZř!!!!!!!!!!W.u..u..u..u..u..u.k.W..u..u..u..u..u..k.Wl....ukel....uW..u..u..u..u..u..u..k.W..u..u..u..u..u..k...WĽ.....LW______________________",
    "w.e..e..el.x.uk..k..k.Wk..ekek..eWk..ekek..eWZZZZZZZř!!!!!!!!!!W.u..u..u..u..u..u.l.W..u..u..u..u..u..l.Wk....ekek....eW..u..u..u..u..u..u..l.W..u..u..u..u..u..l...WĽ..B..LW______________________",
    "w.u..u..u..x..l..l..l.Wl..ukel..uWl..ukel..uWZZZZZZZř!!!!!!!!!!W....................{...................{l....ukel....uW......................{.....................{Ľ..B..LW______________________",
    "W.e..e..e..x..k..k..k.Wk..ekek..eWk..ekek..eWZZZZZZZř!!!!!!!!!!W....................{...................{k....ekek....eW......................{.....................{Ľ..B..LW______________________",
    "W.u..u..u..x..l..l..l.Wl..ukel..uWl..ukel..uWZZZZZZZř!!!!!!!!!!W.u..u..u..u..u..u...{..u..u..u..u..u....{l....ukel....uW..u..u..u..u..u..u....{..u..u..u..u..u......{Ľ..B..LW______________________",
    "w.e..e..e..W..k..k..k.Wk..ekek..eWk..ekek..eWZZZZZZZř!!!!!!!!!!W.u..u..u..u..u..u...{..u..u..u..u..u....{k....ekek....eW..u..u..u..u..u..u....{..u..u..u..u..u......{Ľ..P..LW______________________",
    "w.u..u..u..W..l..l..l.Wl..ukel..uWl..ukel..uWZZZZZZZř!!!!!!!!!!W....................{...................{l....ukel....uW......................{.....................{Ľ.....LW______________________",
    "W.e..e..e..W..k..k..k.Wk...jm...eWk...jm...eWZZZZZZZř!!!!!!!!!!W....................{...................{k.....jm.....eW......................{.....................{B..B..LWWWWWWWWWWWWWWWWWWWWWWWW",
    "W.u..u..u..W..l..l..l.WĽ........LWĽ........LWZZZZZZZř!!!!!!!!!!W.u..u..u..u..u..u...{..u..u..u..u..u....{..............W..u..u..u..u..u..u....{..u..u..u..u..u......{B..B..LW......................W",
    "w.e..e..e..W..........WĽ........LWĽ........LWZZZZZZZř!!!!!!!!!!W.u..u..u..u..u..u...W..u..u..u..u..u....W..............W..u..u..u..u..u..u....W..u..u..u..u..u......WB..B..LW......................W",
    "w..........W..........W.........LW.........LWZZZZZZZř!!!!!!!!!!W....................W...................WĽ.............W......................W.....................WB..B..LW......................W",
    "W..........W..........W..........W..........WZZZZZZZř!!!!!!!!!!W....................W...................WĽ............LW......................W.....................W......LW......................W",
    "W..........W.........tWt.........Wt.........WZZZZZZZř!!!!!!!!!!W...................tWt..................Wt............LW.....................tW....................tWt.....LW......................W",
    "WWW====WWDWWWWWWWWWWDWWWDW----WWWWWDW----WWWW..................WWWWWWWWWWWWWWWWDWWWWWWWWDWWWWWWWWWWWWWWWWWWWWW----DWWWWWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWWWWWWDWWWWWWWDWWWWW......................W",
    "W..........W............................................................................................................................................................................ŘŘŘŘŘŘŘŘ!..W",
    "wnin.......W............................................................................................................................................................................SSSSSSSS!..W",
    "w..........D................................................................................................................................C...........................................SSSSSSSS!bbW",
    "Wjmjmjmj...W............................................................................................................................................................................SSSSSSSS!bbW",
    "w..........W............................................................................................................................................................................SSSSSSSS!??W",
    "w..........WWWWWWWWDWWWWWDWWWWWWWDWWWWWWW...................................WWWWWWWWWWWWDWWWWWWWDWWWWWWWWW...............WWDWWWWWWWWWDWWWWWWWWWWWWWWWWWWDWWWWWWDWWWWWWDWWWWWWWWWDWWWWWWWWWWWWWWWWWWW",
    "Wjmjmjmj...W!mjmjmj.tW........tW....WTWTW...................................W.......W.......Wt...U.U.U.U.W...............W......Wt....k..k..k..k..k..W......W......W.........W...............Ľ..C..W",
    "w..........Wl........W.........W....W.W.W...................................W.......W.......]....J.J.J.J.W...............W......].....l..l..l..l..l..W......W......W.........W...............Ľ.....W",
    "w..........Wk........[.........W....W.W.W...................................W.......W.......]............W...............W......]....................W......W......W.........W...............!!!!..W",
    "Wjmjmjmj...Wl.......u[.........W....WDWDW...................................W.......W.......].N..........W....ľľľľľľľľľľľW......W....................W......W......W.........W..................l..W",
    "w..........Wk.......e[.........W........W...................................D.......W.......W............W....WWWWWWWWWWWW......].....l..l..l..l..l..W......W......W.........W..................l..W",
    "w..........Wl.......uW.........W........W...................................W.......W.......].u..U.U.U.U.W...........dd??W......]..u..k..k..k..k..k..W......W......W.........W...ll...ll...ll...l..W",
    "W..........W!nininin!W.........W........W...................................W.......W.......].e..J.J.J.J.W...........dd??W......]..e..l..l..l..l..l..W......W......W.........W...ll...ll...ll...l..W",
    "WwwWwwWWwwWWWWwwWWwwWWWWwWwWwWWWwWwWwWwWWWWWWWWWWWWWWWGGWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWwwWwwWwwWwwWWwWWwWWwWWwWWwWWWWwWWwWWWwWWWwwWWwwWWwwWWwwWWWwwwWWWWwWWwWWWwWwWwWwWWWwwWwwWwwWwwWwwWwwWwWW"
]

# HoHoHo
first_floor: List[str] = [
    "______________________________________________________________________________________________________________________________________________________________________WWwwwWWWWWWWWWWWWWWWWWWWWWW",
    "______________________________________________________________________________________________________________________________________________________________________W......W..................W",
    "______________________________________________________________________________________________________________________________________________________________________W......W......ninininininiW",
    "______________________________________________________________________________________________________________________________________________________________________W......W..................w",
    "______________________________________________________________________________________________________________________________________________________________________W......W......ninininininiW",
    "______________________________________________________________________________________________________________________________________________________________________W......W..................W",
    "______________________________________________________________________________________________________________________________________________________________________W......D......ninininininiW",
    "______________________________________________________________________________________________________________________________________________________________________WWWDWWWWt.................W",
    "______________________________________________________________________________________________________________________________________________________________________w......WWWWDWWWWXXXXWWXXXXW",
    "______________________________________________________________________________________________________________________________________________________________________w......W..................w",
    "WWWWWwwWWWWWWWWwwWWWWWWwWWWWWwWWWWWwWWWWWwWWWWWwwWWWWWWWwWwWwWWWWWWwwwWWWwwwWWWWWWwWWwWWwWWwWWwWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW......W......mjmjmjmjmjmjW",
    "W..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W..u..u..u..u..u...W...u..u..u..u....W................W...u..u..u..u.....W.........W...u..u..u..u...W.....W......w..................w",
    "W..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W..u..u..u..u..u...W...u..u..u..u....W................W...u..u..u..u.....W.........W...u..u..u..u...W.....D......G......mjmjmjmjmjmjW",
    "W..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W..................W.................W................W..................W.........W................WDW...W......G..................w",
    "W..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W................k.[...............k.[................W...............k..[.........W..............k.[.W...W......w......mjmjmjmjmjmjW",
    "w..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W..u..u..u..u..u.k.[...u..u..u..u..k.[................W...u..u..u..u..k..[.........W...u..u..u..u.k.[ŤW...W......W..................W",
    "w..........W........W.....W..l..W..l..W..l..WZZZZZZZrzzzzzzzW..u..u..u..u..u.l.[...u..u..u..u..l.[................W...u..u..u..u..l..[.........W...u..u..u..u.l.[WWWWWW......WWWWWWWWWWWWWWWWWWWW",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..u..u..u..u..u.k.[...u..u..u..u..k.[................W...u..u..u..u..k..[.........W...u..u..u..u.k.[.....W......W.................Lw",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW................k.[...............k.[................W...............k..[.........W..............k.[.....W......D..................w",
    "w..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..................W.................W..N.............W..................W.........W................W.....W......W..................W",
    "w..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..u..u..u..u..u...W...u..u..u..u....W................W...u..u..u..u.....W.........W...u..u..u..u...W.....W......WWWWWWWWWWWWWWWWWWWW",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..u..u..u..u..u...W...u..u..u..u....D................W...u..u..u..u.....W.........W...u..u..u..u...WWWWWWW..............sssssssssssW",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..................W.................W................W..................W.........W................W.....W..............sssssssssssW",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW.................tWt................W...............tWt.................W.........W................W.....W.............PsssssssssssW",
    "W..........WWWWWWWWWWWWDWWWWWDWWWWWDWWWWWDWWWZZZZZZZrzzzzzzzWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWDWWWWWWWDWWWWWWWWWWWWWWWWWWWWDWWWWWWWWWt.............sssssssssssW",
    "W..........W.........................................................................................................................................................................RRRRRRRRRRRW",
    "w..........W.........................................................................................................................................................................SSSSSSSSSSSw",
    "w..........D.........................................................................................................................................................................SSSSSSSSSSSW",
    "W..........W.........................................................................................................................................................................SSSSSSSSSSSw",
    "W..........W.........................................................................................................................................................................SSSSSSSSSSSW",
    "w..........WWWWWDWWWWWW.....WWDWWWDWWWDWWWDWW..........................WWWDWWWWWWDWWWWWWWWWWWWWWWWWWWWWWDWWWWWWDWWWWWWWDWWWWWWDWWWWWWWWWWWWWWDWWWWWWWWWWWDWWWWWWDWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "w..........W..........W.....W...W...W...W...W..........................W......W.....WoóóóóóóóóóóóóóóóW.....W.......W.......W.............W.............W...W.......l..l..l..l..l..l..l.....W....W",
    "W..........W..........W.....W...W...W...W...W..........................W......W.....Wo..............ÓW.....W.......W.......W.............W.............D...D.......l..l..l..l..l..l..l..........W",
    "W..........W..........W.....W...W...W...W...W..........................W......W.....Wo..............ÓW.....W.......W.......W.............W.............WWDWW...............................W....W",
    "w..........W..........W.....W...W...W...W...W..........................W......W.....Wo..............ÓW.....W.......W.......W.............W.............W...]..........l..l..l..l..l..l..l..WWWWWW",
    "w..........W..........W.....W...W...W...W...W..........................W......W.....Wo..............ÓW.....W.......W.......W.............W.............W...]..........l..l..l..l..l..l..l..W?????",
    "W..........W..........W.....W...W...W...W...W..........................W......W.....Wo.....................W.......W.......W.............W.............W...]...............................W?????",
    "W..........W..........W.....W...W...W...W...W..........................W......W.....Wo.....................W.......W.......W.............W.............W...]...u...l..l..l..l..l..l..l..l..W?????",
    "Wt.........W..........W.....W...W...W...W...W.........................tW......W.....WOOOOOOOOOOOOOOOOW.....W.......W.......W.............W.............W...Wt..e...l..l..l..l..l..l..l..l..W?????",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWwWWWwWWWwWWWwWWWWwwWWWwwWWWwwWWWwwWWWwwWWWWWwwWWWWwwwWWWWWwwwwWWwwwwWWwwwwWWWWWWwwwWWWWWwwwWWWWWWwwWWWwwWWWWWWWwwWWWWwwWWWWwWWWWwwWWWWwwWWWwwWWWWwwWWWWwwWWWWW?????",
]

# IIIIIIIIIi
second_floor: List[str] = [
    "______________________________________________________________________________________________________________________________________________________________________WWwwwWWWWWWWWWWWWWWWWWWWWWW",
    "______________________________________________________________________________________________________________________________________________________________________W.........................W",
    "______________________________________________________________________________________________________________________________________________________________________W......Wininini....inininiW",
    "______________________________________________________________________________________________________________________________________________________________________W.........................W",
    "______________________________________________________________________________________________________________________________________________________________________W..................inininiW",
    "______________________________________________________________________________________________________________________________________________________________________W......Wininini...........W",
    "______________________________________________________________________________________________________________________________________________________________________W.........................W",
    "______________________________________________________________________________________________________________________________________________________________________W..................inininiw",
    "______________________________________________________________________________________________________________________________________________________________________W......Wininini...........W",
    "______________________________________________________________________________________________________________________________________________________________________W.........................W",
    "______________________________________________________________________________________________________________________________________________________________________W..................inininiw",
    "______________________________________________________________________________________________________________________________________________________________________W......Wininini...........W",
    "______________________________________________________________________________________________________________________________________________________________________Wt...................mmjmmW",
    "______________________________________________________________________________________________________________________________________________________________________w.........................w",
    "WWWWWwwWWWWWWWWwwWWWWWWwWWWWWwWWWWWwWWWWWwWWWWWwwWWWWWWWwWwWwWWWWWWwwwWWWwwwWWWWWWwWWwWWwWWwWWwWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWDWWWWWWWW-----WW^^^^^^WW",
    "W..........W..u..u..u..k.W.u..u..u..u..u..k.W!!!!!!!!!!!!!!!W.u..u..u..u..u.k..[..u..u..u..u..k..W................W..u..u..u..u...k..Wt........W.u..u..u..u..k..W.....W......W..................W",
    "Wmm........W..u..u..u..l.W.u..u..u..u..u..l.W!!!!!!!!!!!!!!!W.u..u..u..u..u.l..[..u..u..u..u..l..W................W..u..u..u..u...l..W.........W.u..u..u..u..l..WDW...D......W..................w",
    "W........mmW.............{..................{!!!!!!!!!!!!!!!W..................[.................{................W..................{.........W................{.W...W......W..................w",
    "wmm........W.............{..................{!!!!!!!!!!!!!!!W..................W.................{................W..................{.........W................{ŤW...W......W..................W",
    "W..........W..u..u..u....{.u..u..u..u..u....{ZZZZZZZŔzzzzzzzW.u..u..u..u..u....{..u..u..u..u.....{................W..u..u..u..u......{.........W.u..u..u..u.....{WWWWWW......D..................w",
    "wmm......mmW..u..u..u....{.u..u..u..u..u....{ZZZZZZZŔzzzzzzzW.u..u..u..u..u....{..u..u..u..u.....{................W..u..u..u..u......{.........W.u..u..u..u.....{.....D......W..................W",
    "w..........W.............{..................{ZZZZZZZŔzzzzzzzW..................{.................{................W..................{.........W................{.....W......WWWWWWWWWWWWWWWWWWWW",
    "WWVVVVVWDWWW.............W..................{ZZZZZZZŔzzzzzzzW..................{.................W................W..................W.........W................WWWWWWW..............sssssssssssW",
    "W..........W..u..u..u....W.u..u..u..u..u....WZZZZZZZŔzzzzzzzW.u..u..u..u..u....W..u..u..u..u.....W................W..u..u..u..u......W.........W.u..u..u..u.....W.....W..............sssssssssssW",
    "Wmmm.......W..u..u..u....W.u..u..u..u..u...tWZZZZZZZŔzzzzzzzW.u..u..u..u..u...tW..u..u..u..u....tW...............tW..u..u..u..u.....tW.........W.u..u..u..u.....W.... W.............PsssssssssssW",
    "W..........WWWWWWWWWWWWDWWWWWWWWWWWWWWWWWDWWWŘŘŘŘŘŘŘŕzzzzzzzWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWDWWWWwwwwwwwwwwGGwwwwWWWWWWWWWWWWWWDWWWWWWWWWDWWWWWWWWWWWWWWWWWWDWWWWWWWWWt.............sssssssssssW",
    "W..........W.........................................................................................................................................................................RRRRRRRRRRRW",
    "wjjj...jjj.W.........................................................................................................................................................................SSSSSSSSSSSw",
    "w..........D.........................................................................................................................................................................SSSSSSSSSSSW",
    "W..........W.........................................................................................................................................................................SSSSSSSSSSSw",
    "Wjjj...jjj.W.........................................................................................................................................................................SSSSSSSSSSSW",
    "w..........WWWWWDWWWWWWWWWWWWWWWWWWWDWWWDWWWWW....................WWWDWWWWWWDWWWWWDWWWWWWWWWWDWWWWWDWWWWWWWWWWDWWWWWWDWWWWWWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "w..........W......l..l..l..l..l..W....W..WTWTW...................!W......W.....W.........W.......W......W.........W.....l..l..l..l...W......l..l..l..l...W.........l..l..l..l..l..l..l.....W....W",
    "Wjjj...jjj.]......l..l..l..l..l..W....W..W.W.W....................W......W.....W.........W.......W......W.........W.....l..l..l..l...W......l..l..l..l...W.........l..l..l..l..l..l..l.....D....W",
    "W..........].....................W....W..WDWDW....................W......W.....W.........W.......W......W.........}..................}...................}.................................W....W",
    "w..........].....................W....W......W.!....!.....!.....!.W......W.....W.........W.......W......W.........}..................}...................}.................................WWWWWW",
    "wjjj...jjj.].......l..l..l..l....W....W......W.!....!.....!.....!.W......W.....W.........W.......W......W.........}..................}...................}.................................W?????",
    "w..........].......l..l..l..l....W....W......W.!....!.....!.....!.W......W.....W.........W.......W......W.........}..................}...................}.N...............................W?????",
    "W..........W..k..................W....W......W.!!!!!.......!!!!!..W......W.....W.........W.......W......W.........}.....l..l..l..l...}....l..l..l..l..l..}...u.....l..l..l..l..l..l..l.....W?????",
    "Wt.........W..k..................W....W......W...................tW......W.....W.........W.......W......W.........W.....l..l..l..l...W....l..l..l..l..l..W...e.....l..l..l..l..l..l..l..WWWW?????",
    "WWWWwwWWWWWWWWwwWWWWWWWWWWWWWWwWWWWWwWWWWWwWWWWwwWWWwwWWWwwWWWwwWWWwwWWWWWWwWWWWWwwWWWwwwWWWwwWwWWwwwwWWWWWWwwwWWWWWwwwWWWWWWwwWWWwwWWWWWWWwwWWWWwwWWWWwWWWWwwWWWWwwWWWwwWWWWwwWWWwwWWWWWWWW?????",
]

# Third floor
third_floor: List[str] = [
    "WWWWWWWWWWWWWwwWWWWwwwWWwwwWWwwwWWwwwWWwwwWWwwwWWwwwWWWWWWwwwWWWWWWWWWWWWWWWWWWWWWWW",
    "W..........W.............Y............................WB.......BW..................W",
    "W..........W.............y............................WB.......BW..................W",
    "W..........W..........................................WB.......BW..................W",
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
    "?????????WWWWWWWWWWWWWwwWWWWwwwwWWwwwWWwwwWWwwwWWwwwWWWWWWwwwWWWWWWWWWWWWWWWWWWWWWWW",
    "?????????W..........W.!m!.....jmjmjmjmjmjmjmjmjmj.k...[.........W..................W",
    "?????????W..........W.k.k.........................g...[.........W..................W",
    "?????????W..........W.!m!.............................[.........W..................W",
    "?????????W..........D.................................W.........W..................W",
    "?????????W..........W.........ininininininininini.....D.........W..................W",
    "?????????WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW--WWW.........W..................W",
    "??????????????????????????????????????????????????????Wt........WWWWDWWWWWWWWWWWWWWW",
    "??????????????????????????????????????????????????????W........D........sssssssssssW",
    "??????????????????????????????????????????????????????WWWWWWWWW.........sssssssssssW",
    "??????????????????????????????????????????????????????Whhhhhhhh........PsssssssssssW",
    "??????????????????????????????????????????????????????WB................sssssssssssW",
    "??????????????????????????????????????????????????????WB................|//////////W",
    "??????????????????????????????????????????????????????WB................ř!!!!!!!!!!w",
    "??????????????????????????????????????????????????????WB................ř!!!!!!!!!!W",
    "??????????????????????????????????????????????????????W.................ř!!!!!!!!!!w",
    "??????????????????????????????????????????????????????Wt................ř!!!!!!!!!!W",
    "??????????????????????????????????????????????????????WWWWWWWWDWWWWWWWWWWWWWWWWWWWWW",
    "??????????????????????????????????????????????????????W........l..l..l..l..l..l...!W",
    "??????????????????????????????????????????????????????]........k..k..k..k..k..k...!W",
    "??????????????????????????????????????????????????????]........l..l..l..l..l..l....W",
    "??????????????????????????????????????????????????????]....k.......................W",
    "??????????????????????????????????????????????????????]..N.k......................!W",
    "??????????????????????????????????????????????????????]....k......................!W",
    "??????????????????????????????????????????????????????W....k...l..l..l..l..l..l....W",
    "??????????????????????????????????????????????????????W....!...k..k..k..k..k..k....W",
    "??????????????????????????????????????????????????????W....!...l..l..l..l..l..l....W",
    "??????????????????????????????????????????????????????WWwWWwwwWWwwwWWwwwWWwwwWWwwwWW"
]