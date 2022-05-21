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
VUJ_SPEED: float = 1.5

# Colors
WHITE: tuple =          (255, 255, 255)
BLACK: tuple =          (  0,   0,   0)
NEARLY_BLACK: tuple =   (  1,   1,   1)
RED: tuple =            (255,   0,   0)
GREEN: tuple =          (  0, 255,   0)
BLUE: tuple =           (  0,   0, 255)
LIGHTBLUE: tuple =      (  0, 100, 250)
GRAY: tuple =           ( 64,  64,  64)
DIM_GRAY: tuple =       (105, 105, 105)
DARK_GRAY: tuple =      ( 32,  32,  32)
NAVY: tuple =           ( 11,  19,  30)
BRITISH_WHITE: tuple =  (237, 225, 187)
PAPER_WHITE: tuple =    (248, 236, 194)
YELLOW: tuple =         (232, 216,  17)
PINK: tuple =           (255, 192, 203)
SILVER: tuple =         (192, 192, 192)
GOLD: tuple =           (255, 215,   0)
BROWN: tuple =          ( 60,  30,   6)
ORANGE: tuple =         (255, 165,   0)
VIOLET: tuple =         ( 60,  11,  81)

# Floors
GROUND_FLOOR = 0
FIRST_FLOOR = 1
SECOND_FLOOR = 2
THIRD_FLOOR = 3
FOURTH_FLOOR = 4
ENDING_HALLWAY = 5
BASEMENT_FLOOR = -1

# Number of grades
ALL_GRADES: int = 13

# Basement
basement: List[str]  = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W.........W............W...........W...........W.........W............W......W....W......W",
    "W.........W............W...........W...........W.........W............W......W....W......W",
    "W.........W............W...........W.........ô.W.........W............W......W....W......W",
    "WWWWWDWWWWWWWWWWDWWWWWWWWWWWWDWWWWWWWWWWWWWWWDWWWWWWWDWWWWWWWWWWDWWWWWWWWWDWWWWWDWWDWWWWWW",
    "W........................................................................................S",
    "W.......................................................................................PS",
    "W......ďWWWWDWWWWWWWWWDWWWWWWWWDWWWWWWWWWWDWWWWWWWDWWWWWWWWWWDWWWWWWWWWWDWWWWWWWWWWDWWWWWW",
    "W......ďW........W.........W........W.........W........W..........W..........W...........W",
    "S......ďW........W.........W........W.........W........W..........W..........W...........W",
    "S......ďW........W.........W........W.........W........W..........W..........W...........W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]

# HeHeHeHa
ground_floor: List[str] = [
    "WWwwWWwwWWWWWwwWwwWwwWWWwwWwwWwwWWwwWwwWwwWWWWWWWWWWWWWWWWWWWWWWWwWWwwWWwwWWwwWWwwWWWWWwwWWwwWWwwWWwwWWWWWwwWwwWwwWwwWWWWWWWWWWWWWWWWWWWWWWWWWWWwWWwWWwWWwWWwWWwWWwWWWWwwwWWW______________________",
    "W2a..a..ak.W.ég22g22g2Wl..ukel..uWl..ukel..uWZZZZZZZř!!!!!!!!!!W2u..u..u..u..u..u.k2W2.u..u..u..u..u..k2Wg....akeg....aW2.u..u..u..u..u..u..k2W2.u..u..u..u..u..k..2WĽ.....LW______________________",
    "w2e..e..eg.x.ak22k22k2Wk..ekek..eWk..ekek..eWZZZZZZZř!!!!!!!!!!W2u..u..u..u..u..u.l2W2.u..u..u..u..u..l2Wk....ekek....eW2.u..u..u..u..u..u..l2W2.u..u..u..u..u..l..2WĽ..B..LW______________________",
    "w2a..a..a..x..g..g..gNWl..ukel..uWl..ukel..uWZZZZZZZř!!!!!!!!!!W....................{...................{g....akeg....aW......................{.....................{Ľ..B..LW______________________",
    "W2e..e..e..x..k..k..k.Wk..ekek..eWk..ekek..eWZZZZZZZř!!!!!!!!!!W....................{...................{k....ekek....eW......................{.....................{Ľ..B..LW______________________",
    "W2a..a..a..x..g..g..g.Wl..äkel..uWl..ukel..uWZZZZZZZř!!!!!!!!!!W.u..u..u..u..u..u...{..u..u..u..u..u....{g....akeg....aW..u..u..u..u..u..u....{..u..u..u..u..u......{Ľ..B..LW______________________",
    "w2e..e..e..W..k..k..k.Wk..ekek..eWk..ekek..eWZZZZZZZř!!!!!!!!!!W.u..u..u..u..u..u...{..u..u..u..u..u....{k....ekek....eW..u..u..u..u..u..u....{..u..u..u..u..u......{Ľ..P..LW______________________",
    "w2a..a..a..W..g..g..g.Wl..ukel..uWl..ukel..uWZZZZZZZř!!!!!!!!!!W....................{...................{g....akeg....aW......................{.....................{Ľ.....LW______________________",
    "W2e..e..e..W..k..k..k.Wk...jm...eWk...jm...eWZZZZZZZř!!!!!!!!!!W....................{...................{k.....qm.....eW......................{.....................{B..B..LWWWWWWWWWWWWWWWWWWWWWWWW",
    "W.a..a..a..W..g..g..g.WĽ........LWĽ........LWZZZZZZZř!!!!!!!!!!W.u..u..u..u..u..u...{..u..u..u..u..u....{2.....N......2W..u..u..u..u..u..u....{..u..u..u..u..u......{B..B..LW......................W",
    "w.e..e..e..W..........WĽ........LWĽ........LWZZZZZZZř!!!!!!!!!!W.u..u..u..u..u..u...W..u..u..u..u..u....W2............2W..u..u..u..u..u..u....W..u..u..u..u..u......WB..B..LW......................W",
    "w..........W..........W2........LW.........LWZZZZZZZř!!!!!!!!!!W....................W...................WĽ............2W......................W.....................WB..B..LW..............p.......W",
    "W..........W..........W2.........W.........2WZZZZZZZř!!!!!!!!!!W....................W...................WĽ............LW......................W.....................Wp.....LW......................W",
    "W..........W.........tWt.........Wt........2WZZZZZZZř!!!!!!!!!!W...................tWt..................Wt............LW.....................tW....................tWt.....LW......................W",
    "WWW====WWDWWWWWWWWWWDWWWDW----WWWWWDW----WWWW..................WWWWWWWWWWWWWWWWDWWWWWWWWDWWWWWWWWWWWWWWWWWWWWW----DWWWWWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWWWWWWDWWWWWWWDWWWWW......................W",
    "W..........W.........................................................................................................p..................................................................ŘŘŘŘŘŘŘŘ!..W",
    "wnQn.......W...................................................p..................................9.....................................................................................SSSSSSSS!..W",
    "w..........D................................................................p...............................................................C......p...........................p........SSSSSSSS!bbW",
    "Wqmqmqmq...W.........................................................................................p..................................................................................SSSSSSSS!bbW",
    "w..........W............................................p........p......................................................................................................................SSSSSSSS!??W",
    "w..........WWWWWWWWDWWWWWDWWWWWWWDWWWWWWW...................................WWWWWWWWWWWWDWWWWWWWDWWWWWWWWW...............WWDWWWWWWWWWDWWWWWWWWWWWWWWWWWWDWWWWWWDWWWWWWDWWWWWWWWWDWWWWWWWWWWWWWWWWWWW",
    "Wqmqmqmq...W!mjmjmj.tW........tW....WTWTW.mm$..........p....................W.......W.......Wt...U.U.U.U2W...............W......Wt....k..k..k..k..k22W......W......W.........W...............!Ľ....W",
    "w..........Wl........W.........W....W.W.W...e.....................p.........W.......W.......]....J.J.J.J.W...............W......].....g..g..g..g..g22W......W......W.........W...............!Ľ....W",
    "w..........Wk........[.........W....W.W.W...a...............................W.......W.......]............W...............W......]....................W......W......W.........W...............!!!!..W",
    "Wqmqmqmq...Wl.......u[.........W....WDWDW...e...............................W.......W.......].N..........W....ľľľľľľľľľľľW......W...................EW......W......W.........W..................A..W",
    "w..........Wk.......e[.........W........W...e...............................D.......W.......W............W....WWWWWWWWWWWW......].....g..g..g..g..g..W......W......W.........W..................AN.W",
    "w..........Wl.......uW.........W........Wmmmm....K..........................W.......W.......].a..U.U.U.U.W...........dd??W......].Na..k..k..k..k..k..W......W......W.........W...ul...ul...ul...A..W",
    "W2222222222W!nininin!W.........W........W...................................W.......W.......].e..J.J.J.J2W...........dd??W......]..e..g..g..g..g..g..W......W......W.........W...ul...ul...ul...A..W",
    "WwwWwwWWwwWWWWwwWWwwWWWWwWwWwWWWwWwWwWwWWWWWWWWWWWWWWWGGWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWwwWwwWwwWwwWWwWWwWWwWWwWWwWWWWwWWwWWWwWWWwwWWwwWWwwWWwwWWWwwwWWWWwWWwWWWwWwWwWwWWWwwWwwWwwWwwWwwWwwWwWW"
]

# HoHoHo
first_floor: List[str] = [
    "______________________________________________________________________________________________________________________________________________________________________WWwwwWWWWWWWWWWWWWWWWWWWWWW",
    "______________________________________________________________________________________________________________________________________________________________________W2222..W...............222W",
    "______________________________________________________________________________________________________________________________________________________________________W222...W......nQnQnQnQnQnQW",
    "______________________________________________________________________________________________________________________________________________________________________W22....W..................w",
    "______________________________________________________________________________________________________________________________________________________________________W2.....W......nQnQnQnQnQnQW",
    "______________________________________________________________________________________________________________________________________________________________________W......W......N...........W",
    "______________________________________________________________________________________________________________________________________________________________________W......D......nQnQnQnQnQnQW",
    "______________________________________________________________________________________________________________________________________________________________________WWWDWWWWt..............222W",
    "______________________________________________________________________________________________________________________________________________________________________w......WWWWDWWWWXXXXWWXXXXW",
    "______________________________________________________________________________________________________________________________________________________________________w......W...............222w",
    "WWWWWwwWWWWWWWWwwWWWWWWwWWWWWwWWWWWwWWWWWwWWWWWwwWWWWWWWwWwWwWWWWWWwwwWWWwwwWWWWWWwWWwWWwWWwWWwWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW......W......mqmqmqmqmqmqW",
    "W..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W..u..u..u..u..u222W...u..u..u..u2222W................W...u..u..u..u22222W.........W...u..u..u..u222W.....W......w..................w",
    "W..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W..u..u..u..u..u222W...u..u..u..u2222W................W...u..u..u..u22222W.........W...u..u..u..u222W.....D......G......mqmqmqmqmqmqW",
    "W..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W..................W.................W................W..................W.........W................WDW...W..p...G..................w",
    "W..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W................k.[...............k.[................W...............k..[.........W..............k.[.W...W......w......mqmqmqmqmqmqW",
    "w..........W........W.....W.....W.....W.....W!!!!!!!!!!!!!!!W..u..u..u..u..u.k.[...u..u..u..u..k.[................W...u..u..u..u..k..[.........W...u..u..u..u.k.[ŤW...W......W...............222W",
    "w..........W........W.....W..l..W..l..W..l..WZZZZZZZrzzzzzzzW..u..u..u..u..u.l.[...u..u..u..u..l.[................W...u..u..u..u..l..[.........W...u..u..u..u.l.[WWWWWW......WWWWWWWWWWWWWWWWWWWW",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..u..u..u..u..u.k.[...u..u..u..u..k.[................W...u..u..u..u..k..[.........W...u..u..u..u.k.[.....W......W.................Lw",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW................k.[...............k.[................W...............k..[.........W..............k.[.....W......D..................w",
    "w..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..................W.................W..N.............W..................W.........W................W.....W......W................N.W",
    "w..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..u..u..u..u..u...W...u..u..u..u....W................W...u..u..u..u.....W.........W...u..u..u..u...W.....Wň.....WWWWWWWWWWWWWWWWWWWW",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..u..u..u..u..u...W...u..u..u..u....D................W...u..u..u..u.....W.........W...u..u..u..u...WWWWWWWň.............sssssssssssW",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW..................W.................W................W..................W.........W................W.....Wň.............sssssssssssW",
    "W..........W........W.....W.....W.....W.....WZZZZZZZrzzzzzzzW.................tWt................W...............tWt.................W.........W................W.....Wň...p........PsssssssssssW",
    "W..........WWWWWWWWWWWWDWWWWWDWWWWWDWWWWWDWWWZZZZZZZrzzzzzzzWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWDWWWWWWWDWWWWWWWWWWWWWWWWWWWWDWWWWWWWWWt.............sssssssssssW",
    "W..........W.........................................................................................................................................................................RRRRRRRRRRRW",
    "w..........W.........................................................................................................................................................................SSSSSSSSSSSw",
    "w..........D......................p....................................................................p..................................................................p..........SSSSSSSSSSSW",
    "W..........W.........................................................................................................................................................................SSSSSSSSSSSw",
    "W..........W.........................................................................................................................................................................SSSSSSSSSSSW",
    "w..........WWWWWDWWWWWW.....WWDWWWDWWWDWWWDWW..........................WWWDWWWWWWDWWWWWWWWWWWWWWWWWWWWWWDWWWWWWDWWWWWWWDWWWWWWDWWWWWWWWWWWWWWDWWWWWWWWWWWDWWWWWWDWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "w..........W..........W.....W...W...W...W...W..........................W......W.....WoóóóóóóóóóóóóóóóWt....W.......W.......W.............W.............W...W.......l..l..l..l..l..l..l.....W2222W",
    "W..........W..........W.....W...W...W...W...W..........................W......W.....Wo..............ÓW.....W.......W.......W.............W.............D...D.......l..l..l..l..l..l..l......2222W",
    "W..........W..........W.....W...W...W...W...W..........................W......W.....Wo..............ÓW.....W.......W.......W.............W.............WWDWW...............................W2222W",
    "w..........W..........W.....W...W...W...W...W...........p..............W......W.....Wo..............ÓW.....W.......W.......W.............W.............W...]..........l..l..l..l..l..l..l..WWWWWW",
    "w..........W..........W.....W...W...W...W...W..........................W......W.....Wo..............ÓW.....W.......W.......W.............W.............W...]..........l..l..l..l..l..l..l..W?????",
    "W..........W..........W..N..W...W...W...W...W..........................W......W.....Wo.....................W.......W.......W.............W.............W...]...............................W?????",
    "W..........W..........W.....W...W...W...W...W..........................W......W.....Wo.....................W.......W.......W.............W.............W...]...u...l..l..l..l..l..l..l..l..W?????",
    "Wt.........W..........W.....W...W...W...W...W.........................tW......W.....WOOOOOOOOOOOOOOOOW2222EW.......W.......W.............W.............W...Wt..e...l..l..l..l..l..l..l..l..W?????",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWwWWWwWWWwWWWwWWWWwwWWWwwWWWwwWWWwwWWWwwWWWWWwwWWWWwwwWWWWWwwwwWWwwwwWWwwwwWWWWWWwwwWWWWWwwwWWWWWWwwWWWwwWWWWWWWwwWWWWwwWWWWwWWWWwwWWWWwwWWWwwWWWWwwWWWWwwWWWWW?????",
]

# IIIIIIIIIi
second_floor: List[str] = [
    "______________________________________________________________________________________________________________________________________________________________________WWwwwWWWWWWWWWWWWWWWWWWWWWW",
    "______________________________________________________________________________________________________________________________________________________________________W2222222222222222222222222W",
    "______________________________________________________________________________________________________________________________________________________________________W......Wininini....inininiW",
    "______________________________________________________________________________________________________________________________________________________________________W......................222W",
    "______________________________________________________________________________________________________________________________________________________________________W..................inininiW",
    "______________________________________________________________________________________________________________________________________________________________________W......Wininini...........W",
    "______________________________________________________________________________________________________________________________________________________________________W.........................W",
    "______________________________________________________________________________________________________________________________________________________________________W..................inininiw",
    "______________________________________________________________________________________________________________________________________________________________________W......Wininini...........W",
    "______________________________________________________________________________________________________________________________________________________________________W.........................W",
    "______________________________________________________________________________________________________________________________________________________________________W..................inininiw",
    "______________________________________________________________________________________________________________________________________________________________________W......Wininini...........W",
    "______________________________________________________________________________________________________________________________________________________________________Wt...................mmqmmW",
    "______________________________________________________________________________________________________________________________________________________________________w.....................N...w",
    "WWWWWwwWWWWWWWWwwWWwwWwwWWWWwwWwwWwwWwwWwwWWWWWwwWWWWWWWwWwWWWwwwWWwwwWWWwwwWWWWWWwWWwWWwWWwWWwWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWDWWWWWWWW-----WW^^^^^^WW",
    "W2222222222W2.u..u..u..k.W2u..u..u..u..u..k.W!!!!!!!!!!!!!!!W2u..u..u..u..u.k..[22u..u..u..u..k..W................W22u..u..u..u...k..Wt........W2u..u..u..u..k..W.....W......W..................W",
    "Wmm........W2.u..u..u..l.W2u..u..u..u..u..l.W!!!!!!!!!!!!!!!W2u..u..u..u..u.lN.[22u..u..u..u..l..W................W22u..u..u..u...l..W.........W2u..u..u..u..l..WDW...D......W..................w",
    "W........mmW2............{..................{!!!!!!!!!!!!!!!W..................[.................{................W..................{.........W................{.W...W......W..................w",
    "wmm........W2............{................N.{!!!!!!!!!!!!!!!W..................W.................{................W..................{.........W................{ŤW...W......W..................W",
    "W..........W2.u..u..u....{2u..u..u..u..u....{ZZZZZZZŔzzzzzzzW2u..u..u..u..u....{22u..u..u..u.....{................W22u..u..u..u......{.........W2u..u..u..u.....{WWWWWW......D..................w",
    "wmm......mmW2.u..u..u....{2u..u..u..u..u....{ZZZZZZZŔzzzzzzzW2u..u..u..u..u....{22u..u..u..u.....{................W22u..u..u..u......{.........W2u..u..u..u.....{.....D......W.................EW",
    "w..........W2............{..................{ZZZZZZZŔzzzzzzzW..................{.................{................W..................{.........W................{.....Wč.....WWWWWWWWWWWWWWWWWWWW",
    "WWVVVVVWDWWW2............W..................{ZZZZZZZŔzzzzzzzW..................{.................W................W..................W.........W................WWWWWWWč.............sssssssssssW",
    "W..........W2.u..u..u....W2u..u..u..u..u....WZZZZZZZŔzzzzzzzW2u..u..u..u..u....W22u..u..u..u.....W................W22u..u..u..u......W.........W2u..u..u..u.....W.....Wč.............sssssssssssW",
    "WnQn.......W2.u..u..u....W2u..u..u..u..u...tWZZZZZZZŔzzzzzzzW2u..u..u..u..u...tW22u..u..u..u....tW...............tW22u..u..u..u.....tW.........W2u..u..u..u.....W.... Wč............PsssssssssssW",
    "W2.........WWWWWWWWWWWWDWWWWWWWWWWWWWWWWWDWWWŘŘŘŘŘŘŘŕzzzzzzzWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWDWWWWwwwwwwwwwwGGwwwwWWWWWWWWWWWWWWDWWWWWWWWWDWWWWWWWWWWWWWWWWWWDWWWWWWWWWt.............sssssssssssW",
    "W2.........W.....žžžžž...............................................................................úúúúúúú.........................................................................RRRRRRRRRRRW",
    "wjjj...jjj.W.........................................................................................................................................................................SSSSSSSSSSSw",
    "w2......N..D.........................................................................................................................................................................SSSSSSSSSSSW",
    "W2.........W.........................................................................................................................................................................SSSSSSSSSSSw",
    "Wjjj...jjj.W.........ýýýýý...........................................................................úúúúúúúú........................................................................SSSSSSSSSSSW",
    "w2.........WWWWWDWWWWWWWWWWWWWWWWWWWDWWWDWWWWW.........p..........WWWDWWWWWWDWWWWWDWWWWWWWWWWDWWWWWDWWWWWWWWWWDWWWWWWDWWWWWWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWDWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "w2.........W......l..l..l..l..l..W....W..WTWTW...................~W......W.....W.........W.......W......W.........W.....l22l22l22l222W......l22l22l22l222W.........l..l..l..l..l..l..l.....W....W",
    "Wjjj...jjj.]......l..l..l..l..l..W....W..W.W.W....................W......W.....W.........W.......W......W.........W.....l..l..l..l...W......l22l22l22l222W.........l..l..l..l..l..l..l.....D....W",
    "W2.........].....................W....W..WDWDW....................W......W.....W.........W.......W......W.........}..................}...................}.................................W....W",
    "w2.........].....................W....W......W#22!!22*....#22!22*.W......W.....W.........W.......W......W.........}..................}...................}.................................WWWWWW",
    "wjjj...jjj.].......l..l..l..l....W....W......W#22!!22*....#22!22*.W......W.....W.........W.......W......W.........}..................}...................}.................................W?????",
    "w..........].......l..l..l..l....W....W......W#222222*....#22222*.W......W.....W.........W.......W......W.........}..................}...................}.N...............................W?????",
    "W..........W22k..................W....W......W.!@@@@!......!@@@!..W......W.....W.........W.......W......W.........}.....l..l..l..l...}....l22l22l22l22l22}...u.....l..l..l..l..l..l..l.....W?????",
    "Wt.........W22k..................W....W......W...................tW......W.....W.........W.......W......W.........W.....l22l22l22l222W....l22l22l22l22l22W...e.....l..l..l..l..l..l..l22222W?????",
    "WWWWwwWWWWWWWWwwWWWWWWWWWWWWWWwWWWWWwWWWWWwWWWWwwWWWwwWWWwwWWWwwWWWwwWWWWWWwWWWWWwwWWWwwwWWWwwWwWWwwwwWWWWWWwwwWWWWWwwwWWWWWWwwWWWwwWWWWWWWwwWWWWwwWWWWwWWWWwwWWWWwwWWWwwWWWWwwWWWwwWWWWWWWW?????",
]

# Third floor
third_floor: List[str] = [
    "WWWWWWWWWWWWWwwWWWWwwwWWwwwWWwwwWWwwwWWwwwWWwwwWWwwwWWWWWWwwwWWWWWWWWWWWWWWWWWWWWWWW",
    "W2222222222Wˇ............Y........&&&&&............&&&WB.......BW..................W",
    "W2222222222Wˇ............y............................WB.......BW..................W",
    "W2222222222Wˇ.....................p.......p...........WB.......BW..................W",
    "W2222222222Wˇ............p............................WB.......BWWWWWWW............W",
    "W2222222222W.........ŽŽŽŽŽŽŽŽŽŽŽŽŽŽŽŽŽŽŽŽŽŽŽŽŽŽŽŽŽ....D........BW.....W............W",
    "W2222222222WWWWWDDWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW......W.....D............W",
    "W.............p.......................................W..D......W.....WWWWWWWWWWWWWW",
    "W........p...............p...........p................WŤ.W.....D........sssssssssssW",
    "W.............p.................p.....................WWWWWWWWW.........sssssssssssW",
    "W..p..................p................p..............W................PsssssssssssW",
    "W..........p.....p..........p....p..........p.........D.................sssssssssssW",
    "W.................p...................p...............D.................RRRRRRRRRRRW",
    "W......p...............p..........p...................W.................SSSSSSSSSSSw",
    "W..........................................p..........W.................SSSSSSSSSSSW",
    "W......p..p............p.......p......................W.................SSSSSSSSSSSw",
    "W................p................p...p...............W.................SSSSSSSSSSSW",
    "Wô..........................p............p...........0W.................WWWWWWWWWWWW",
    "W.......p.....p....p..................................WWWWWWWWWWWWWDWWWWW2222222222W",
    "W............................p........................WB...............BW..........W",
    "W......p.........p.............p......p...............WB...............BW..........W",
    "W...........p.........p.............p.................WB......34.......BW..........W",
    "W.....................................................WB......56.......BW..........W",
    "W........p........p...p.....p........p................WB......78.......BW..........W",
    "W.........p....................p......................WB...............BW..........W",
    "W.............p........p..............................D.................D..........W",
    "W.....p...........................p...................W.................W..........W",
    "WWWwwwWWwwwWWwwwWWWwwwWWwwwWWwwwWWwwwWWwwwWWwwwWWwwwWWWWWwwWwwWWWwwWwwWWWWWWWWWWWWWW"
]

# Fourth floor
fourth_floor: List[str] = [
    "?????????WWWWWWWWWWWWWwwWWWWwwwwWWwwwWWwwwWWwwwWWwwwWWWWWWwwwWWWWWWWWWWWWWWWWWWWWWWW",
    "?????????W..........WE!m!..N..qmqmqmqmqmqmqmqmqmq.k...[.........W..................W",
    "?????????W..........W.k.e.........................g...[.........W..................W",
    "?????????W..........W.!n!.........p....p.....p........[.........W..................W",
    "?????????W..........D........p........................W.........W..................W",
    "?????????W..........W.........QnQnQnQnQnQnQnQnQnQ.....D.........W..................W",
    "?????????WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW--WWW.........W..................W",
    "??????????????????????????????????????????????????????Wt........WWWWDWWWWWWWWWWWWWWW",
    "??????????????????????????????????????????????????????W........D........sssssssssssW",
    "??????????????????????????????????????????????????????WWWWWWWWW.........sssssssssssW",
    "??????????????????????????????????????????????????????Whhhhhhhh........PsssssssssssW",
    "??????????????????????????????????????????????????????WB................sssssssssssW",
    "??????????????????????????????????????????????????????WB.....p..........|//////////W",
    "??????????????????????????????????????????????????????WB................ř!!!!!!!!!!w",
    "??????????????????????????????????????????????????????WB....p...p.......ř!!!!!!!!!!W",
    "??????????????????????????????????????????????????????W2...p............ř!!!!!!!!!!w",
    "??????????????????????????????????????????????????????Wt................ř!!!!!!!!!!W",
    "??????????????????????????????????????????????????????WWWWWWWWDWWWWWWWWWWWWWWWWWWWWW",
    "??????????????????????????????????????????????????????W........g22g22g22g22g22g...!W",
    "??????????????????????????????????????????????????????]........k..k..k..k..k..k...!W",
    "??????????????????????????????????????????????????????]........g..g..g..g..g..g....W",
    "??????????????????????????????????????????????????????]....e...............p.......W",
    "??????????????????????????????????????????????????????]..N.a.......p..............!W",
    "??????????????????????????????????????????????????????]....e............p.........!W",
    "??????????????????????????????????????????????????????W....e...g..g..g..g..g..g....W",
    "??????????????????????????????????????????????????????W....!...k..k..k..k..k..k....W",
    "??????????????????????????????????????????????????????W2222!...g22g22g22g22g22g....W",
    "??????????????????????????????????????????????????????WWwWWwwwWWwwwWWwwwWWwwwWWwwwWW"
]

ending_hallway: List[str] = [
    "WWWWWWWWWWWWWW",
    "WWWWWWWWWWWWWW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WWWWWDDDWWWWWW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW..........WW",
    "WW....P.....WW",
    "WWWWWWWWWWWWWW",
]