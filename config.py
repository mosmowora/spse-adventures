# Import
from typing import List

WIN_WIDTH: int = 640
WIN_HEIGHT: int = 480
TILE_SIZE: int = 32
FPS: int = 60

PLAYER_LAYER: int = 4
OBJECT_LAYER: int = 3
BLOCK_LAYER: int = 2
GROUND_LAYER: int = 1

PLAYER_SPEED: int = 2

RED: tuple = (255, 0, 0)
BLACK: tuple = (0, 0, 0)
BLUE: tuple = (0, 0, 255)

tilemap: List[str] = [
    "_______WWOOOWW______",
    "_______S.....S______",
    "_______S..L..S______",
    "_______S..L..S______",
    "_______S..L..S______",
    "_______S..L..S______",
    "_______S..P..S______",
    "_______S.....S______",
    "_______W..L..S______",
    "_______W..L..S______",
    "_______W..L..S______",
    "_______W..L..S______",
    "_______W.....S______",
    "_______WT....S______",
    "_______WWWDWWW______"
]