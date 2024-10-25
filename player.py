
class Player:
    """Creates a player with a name and a hand of 7 cards."""
    def __init__(self, user_name:str, game):
        self.name:str = user_name
        self.hand = []
        for i in range(7):
            self.draw(game.deck)
    
    def draw(self, deck, cards:int = 1):
        """Draws a number card from a deck and add it to the players hand"""
        for i in range(cards):
            card = deck.draw()
            self.hand.append(card)
            return card

    def __repr__(self) -> str:
        return f"{self.name}: {self.hand}"
    

