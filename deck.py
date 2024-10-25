from card import Card
import random

class Pile():
    """Creating a pile of cards"""
    def __init__(self):
        self.pile = []

class Deck(Card):
    """Creating a deck full of 12 cards of each color including action cards and wilds."""
    def __init__(self):
        self.deck = []
        for i in range(2):
            for c in ["blue", "green", "red", "yellow"]:
                for i in range(1,13):
                    if i == 12: 
                        card = Card(c, "plustwo")
                    elif i == 11:
                        card = Card(c, "reverse")
                    elif i == 10:
                        card = Card(c, "skip")
                    else:
                        card = Card(c, str(i))
                    self.deck.append(card)
                
        #Creating wild and draw 4 cards        
        for i in range(4):
            card = Card("wild", "wild")
            self.deck.append(card)
            card = Card("wild", "draw4")
            self.deck.append(card)

    def shuffle_deck(self):
        """Shuffles a deck"""
        random.shuffle(self.deck)

    def refill_deck(self, pile):
        """Refills the deck with all the cards in the pile except for the current card"""
        top_card = pile.pop(-1)
        while len(pile) > 0:
            card = pile.pop()
            
            self.deck.append(card)
        pile.append(top_card)
        self.shuffle_deck()

    
    
    def draw(self):
        """Draws a card from the deck"""
        card = self.deck.pop()
        return card
                    