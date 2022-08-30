import pygame
from .models import *
from .engine import *

pygame.init()
bounds = (1024, 768)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("SPŠE ADVENTURE - REVENGEANCE")
icon = pygame.image.load('img/spselogo2.png')
pygame.display.set_icon(icon)
gameEngine = SnapEngine()

cardBack = pygame.image.load('card_images/BACK.png')
cardBack = pygame.transform.scale(cardBack, (int(238*0.8), int(332*0.8)))

def renderGame(window):
    window.fill((15,0,169))
    font = pygame.font.SysFont('comicsans',60, True)

    window.blit(cardBack, (100, 200))
    window.blit(cardBack, (700, 200))

    text = font.render(str(len(gameEngine.player1.hand)) + " cards", True, (255,255,255))
    window.blit(text, (100, 500))

    text = font.render(str(len(gameEngine.player2.hand)) + " cards", True, (255,255,255))
    window.blit(text, (700, 500))

    topCard = gameEngine.pile.peek()
    if (topCard != None):
        window.blit(topCard.image, (400, 200))
        
    if gameEngine.state == GameState.PLAYING:
        text = font.render(gameEngine.currentPlayer.name + " to flip", True, (255,255,255))
        window.blit(text, (20,50))

    if gameEngine.state == GameState.SNAPPING:
        result = gameEngine.result
        if result["isSnap"]:
            message = "Winning Snap! by " + result["winner"].name
        else:
            message = "False Snap! by " + result["snapCaller"].name + ". " + result["winner"].name + " wins!"
            text = font.render(message, True, (255,255,255))
            window.blit(text, (20,50))

    if gameEngine.state == GameState.ENDED:
        result = gameEngine.result
        message = "Game Over! " + result["winner"].name + " wins!"
        text = font.render(message, True, (255,255,255))
        window.blit(text, (20,50))
        return False
    
    return True
        
        
def start():
    run = True
    while run:
        key = None; 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return
            if event.type == pygame.KEYDOWN:
                key = event.key
            if gameEngine.currentPlayer == gameEngine.player2:
                pygame.time.delay(800)
                try:
                    if gameEngine.pile.cards[-1].value == gameEngine.pile.cards[-2].value:
                        key = gameEngine.player2.snapKey
                    else: 
                        key = gameEngine.player2.flipKey
                except IndexError:
                    key = gameEngine.player2.flipKey
        
        gameEngine.play(key)
        run: bool = renderGame(window)
        pygame.display.update()

        if gameEngine.state == GameState.SNAPPING:
            pygame.time.delay(2500)
            gameEngine.state = GameState.PLAYING
    
    return False