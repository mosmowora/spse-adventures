# Import
from typing import List

win_width: int = 640
win_height: int = 480
tilesize: int = 32
fps: int = 60

player_layer: int = 4
object_layer: int = 3
block_layer: int = 2
ground_layer: int = 1

player_speed: int = 2

red: tuple = (255, 0, 0)
black: tuple = (0, 0, 0)
blue: tuple = (0, 0, 255)

tilemap: List[str] = [
    "WWOOOWW",
    "S.....S",
    "S..L..S",
    "S..L..S",
    "S..L..S",
    "S..L..S",
    "S..P..S",
    "S.....S",
    "W..L..S",
    "W..L..S",
    "W..L..S",
    "W..L..S",
    "W.....S",
    "W.....S",
    "WWDWWWW"
]