from enum import Enum
import pygame
import random

class Suits(Enum):
    CLUB = 0
    SPADE = 1
    HEART = 2
    DIAMOND = 3
  
class Card:
    suit = None
    value = None
    image = None
    
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.image = pygame.image.load('card_images/' + self.suit.name + '-' + str(self.value) + '.svg')

class Deck:
    cards = None
    
    def __init__(self):
        self.cards = []
        for suit in Suits:
            for value in range(1,14):
                self.cards.append(Card(suit, value))
            
    def shuffle(self):
        random.shuffle(self.cards)
        
    def deal(self):
        return self.cards.pop()

    def length(self):
        return len(self.cards)

class Pile:
    cards = None
    
    def __init__(self):
        self.cards = []
        
    def add(self, card):
        self.cards.append(card)
        
    def peek(self):
        if (len(self.cards) > 0):
            return self.cards[-1]
        else:
            return None
        
    def popAll(self):
        return self.cards
        
    def clear(self):
        self.cards = []
        
    def isSnap(self):
        if (len(self.cards) > 1):
            return (self.cards[-1].value == self.cards[-2].value)
        return False
    
class Player:
    hand = None
    flipKey = None
    snapKey = None
    name = None

    def __init__(self, name, flipKey, snapKey):
        self.hand = []
        self.flipKey = flipKey
        self.snapKey = snapKey
        self.name = name
        
    def draw(self, deck):
        self.hand.append(deck.deal())
        
    def play(self):
        return self.hand.pop(0)