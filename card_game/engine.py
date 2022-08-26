from enum import Enum
import pygame
from .models import *

class GameState(Enum):
    PLAYING = 0
    SNAPPING = 1
    ENDED = 2
    

class SnapEngine:
    deck = None
    player1 = None
    player2 = None
    pile = None
    state = None
    currentPlayer = None
    result = None
    
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player1 = Player("Player 1", pygame.K_q, pygame.K_w)
        self.player2 = Player("Player 2", pygame.K_o,pygame.K_p)
        self.pile = Pile()
        self.deal()
        self.currentPlayer = self.player1
        self.state = GameState.PLAYING
        
    def deal(self):
        half = self.deck.length() // 2
        for _ in range(0, half):
            self.player1.draw(self.deck)
            self.player2.draw(self.deck)
            
    def switchPlayer(self):
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1
            
    def winRound(self, player):
        self.state = GameState.SNAPPING
        player.hand.extend(self.pile.popAll())
        self.pile.clear()
        
    def play(self, key):
        if key is None: 
            return
        
        if self.state == GameState.ENDED:
            return
        
        if key == self.currentPlayer.flipKey:
            self.pile.add(self.currentPlayer.play())
            self.switchPlayer()
            
        snapCaller = None
        nonSnapCaller = None
        isSnap = self.pile.isSnap()

        if (key == self.player1.snapKey):
            snapCaller = self.player1
            nonSnapCaller = self.player2
        elif (key == self.player2.snapKey):
            snapCaller = self.player2
            nonSnapCaller = self.player1
            
        if isSnap and snapCaller:
            self.winRound(snapCaller)
            self.result = {
                "winner": snapCaller,
                "isSnap": True,
                "snapCaller": snapCaller 
            }
            self.winRound(snapCaller)
        elif not isSnap and snapCaller:
            self.result = {
                "winner": nonSnapCaller,
                "isSnap": False,
                "snapCaller": snapCaller 
            }
            self.winRound(nonSnapCaller)
    
        if len(self.player1.hand) == 0:
            self.result = {
                "winner": self.player2,
            }
            self.state = GameState.ENDED
        elif len(self.player2.hand) == 0:
            self.result = {
                "winner": self.player1,
            }
            self.state = GameState.ENDED
        
        