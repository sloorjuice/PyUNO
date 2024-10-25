from player import Player
from deck import Deck
from deck import Pile
from card import Card
import tkinter as tk
import random

import sys
class Main:
    def __init__(self) -> None:
        """Creating the window"""
        # Creating the window
        self.window = tk.Tk()
        # Creating the icon and title
        icon = tk.PhotoImage(file = 'images/draw4_draw4.png')
        self.window.wm_iconphoto(False, icon)
        self.windowTitle = self.window.title("Uno")
        self.debugMenu = False
        
        """Setting up the game"""
        # Creating/Shuffling a Deck/pile
        self.deck, self.pile = Deck(), Pile()
        self.deck.shuffle_deck()
        if self.deck.deck[0].color == "wild": # Reshuffle if first card is a wild
            print("SAVED THE DAY")
            self.deck.shuffle_deck()
        # Creating Players one and two
        self.playerOne, self.playerTwo = Player("Player One", self), Player("Player Two", self)
        self.currentIndex = 8 # Keeps track of how many cards the player has had total
        self.currentTurn = "Player One" # Setting current turn to player one
        self.totalTurns = 1 # Keeps track of the total # of turns
        
        self.wildMenuVar = tk.StringVar(self.window) # Keep track of what color the player choses when using a wild
        self.isSkip = False # Keeps track if a card is a skip or not
        self.isPlusTwo = False # Keeps track if a card is a plus two or not
        
        # Creating an image for the back of the card and making it a draw card button
        backImgPath = "images\\back.png"
        backCardImage = tk.PhotoImage(file=backImgPath)
        self.drawButton = tk.Button(self.window, command = lambda:self.draw_button(), image=backCardImage).grid(column=0,row=4)
        
        # Set the first card
        self.pile.pile.append(self.deck.deck.pop(0)) # Puts the first card in the deck into the pile
        self.currentCard = self.pile.pile[0] # Keeps track of the currentCard
        self.currentCardLabel = tk.Label(self.window, image=self.currentCard.image).grid(column=1,row=4) # Displays current 
        
        # Displays how many cards player two has
        self.playerTwoHandLabel = tk.Label(self.window, text=f"Player 2 has {len(self.playerTwo.hand)} cards").grid(column=0,row=0)
        # Displays how many cards in Deck/Pile
        self.cardsInDeckLabel = tk.Label(self.window, text=f"Cards left in deck: {len(self.deck.deck)}").grid(column=0,row=1)
        self.cardsInPileLabel = tk.Label(self.window, text=f"Cards in pile: {len(self.pile.pile)}").grid(column=0,row=2)
        # Displays the current color of the current card
        self.currentColorLabel = tk.Label(self.window, text=f"Current Color: {self.currentCard.color}")
        self.currentColorLabel.grid(column=0,row=3)
        
        # Displaying the players hand
        self.cardButtons = [] # Creating a list for all the buttons that will represent the cards in the hand
        for i, card in enumerate(self.playerOne.hand): # Looping through the cards in the players hand
            button = tk.Button(self.window, command = lambda card=card:self.play_card(card), image=card.image)
            button.grid(column=i,row=5) # Creating buttons for the cards
            self.cardButtons.append(button) # Adding the cards to the list of cards
            
        # Creating other buttons
        self.quitButton = tk.Button(self.window, text='Quit', width=10, command=(quit)).grid(row=6, column=2)
        self.refillButton = tk.Button(self.window, text='Refill', width=10, command=self.use_refill_button).grid(row=6, column=1)
        if self.debugMenu:
            self.updateButton = tk.Button(self.window, text='Update', width=10, command=self.update).grid(row=6, column=0)

        tk.mainloop()
        
        
    """Methods for buttons"""
    def draw_button(self, cards:int = 1):
            """Code for the draw draw button, Draws a card, adds it to the hand and creates a button"""
            if len(self.deck.deck) > 0 and self.currentTurn == "Player One":
                for i in range(cards):
                    card = self.playerOne.draw(self.deck)
                    button = tk.Button(self.window, command = lambda card=card:self.play_card(card), image=card.image)
                    button.grid(column=self.currentIndex,row=5)
                    self.cardButtons.append(button)
                    self.currentIndex = self.currentIndex + 1
                    self.update()
                    self.currentTurn = "Player Two"
                    self.totalTurns += 1

                    self.player_two_ai()
            else:
                pass
            
    def play_card(self, card):
        """Code for the draw card button, 
        Removing the button, Creating a new button, moving the card from the hand to the pile and displaying it"""
        cardIndex = self.playerOne.hand.index(card)
        if card.compare(self.currentCard) and card.color != "wild" and self.currentTurn == "Player One":
            if card.value == "plustwo":
                for i in range(2):
                    self.playerTwo.draw(self.deck)
            elif card.value == "skip" or card.value == "reverse":
                self.isSkip = True
            self.cardButtons[cardIndex].destroy()
            x = self.playerOne.hand.pop(cardIndex)
            self.cardButtons.pop(cardIndex)
            self.currentCard = x
            self.pile.pile.append(x)
            self.update()
            if self.isSkip:
                self.isSkip = False
                return
            self.currentTurn = "Player Two"
            self.totalTurns += 1
            self.player_two_ai() 
        elif card.color == "wild":
            self.cardButtons[cardIndex].destroy()
            x = self.playerOne.hand.pop(cardIndex)
            self.cardButtons.pop(cardIndex)
            self.pile.pile.append(cardIndex)
            self.currentCard = card
            self.update()
            if card.value == "draw4":
                for i in range(4):
                    self.playerTwo.draw(self.deck)
            self.wildMenuVar.set("wild")  # Default value
            self.dropdown = tk.OptionMenu(
                self.window,
                self.wildMenuVar,
                "red",
                "green",
                "blue",
                "yellow",
                command=self.wild_card_dropdown # Directly use the method
            )
            self.dropdown.grid(column=2, row=4) 

    def use_refill_button(self):
        """Code for the refill button"""
        self.deck.refill_deck(self.pile.pile)
       
        self.update()

    def wild_card_dropdown(self, selectedColor):
        """Code for the wild dropdown"""
        # Set the current card's color to the selected color
        self.currentCard.color = selectedColor
        self.currentCard.value = "none"
        self.imagePath = f"images\\{self.currentCard.color}_wild.png"
        self.currentCard.image = tk.PhotoImage(file=self.imagePath)
        self.dropdown.destroy()  # Remove the dropdown
        self.currentTurn = "Player Two"
        self.totalTurns += 1
        self.update()
        self.player_two_ai()


    """Update Methods"""
    def update(self):
        self.update_current_card()
        self.update_deck_info()
        self.update_player_two_hand()
        self.update_current_color()
        if self.debugMenu:
            #Debug Menu
            print('Debug Menu:')
            print(f'Current Card: {self.currentCard}')
            print(f'Current Turn({self.totalTurns}): {self.currentTurn}')
            print(f'Player One Hand({len(self.playerOne.hand)}): {self.playerOne.hand}')
            print(f'Player Two Hand({len(self.playerTwo.hand)}): {self.playerTwo.hand}')
            print(f'Current Index(total # of cards player one has had): {self.currentIndex}')
        if len(self.playerOne.hand) <= 0:
            
            sys.exit()
    
    def update_current_color(self):
        self.currentColorLabel.destroy()
        self.currentColorLabel = tk.Label(self.window, text=f"Current Color: {self.currentCard.color}")
        self.currentColorLabel.grid(column=0,row=3)  
    
    def update_current_card(self):
        """Updates the current card image"""
        self.currentCardLabel = tk.Label(self.window, image=self.currentCard.image).grid(column=1,row=4)

    def update_deck_info(self):
        """Updates the # of cards in deck and pile"""
        self.cardsInDeckLabel = tk.Label(self.window, text=f"Cards left in deck: {len(self.deck.deck)}").grid(column=0,row=1)
        self.cardsInPileLabel = tk.Label(self.window, text=f"Cards in pile: {len(self.pile.pile)}").grid(column=0,row=2)
    
    def update_player_two_hand(self):
        """Updates the # of cards in player two's hand"""
        self.playerTwoHandLabel = tk.Label(self.window, text=f"Player 2 has {len(self.playerTwo.hand)} cards").grid(column=0,row=0)
                    
    
    """A.I. Methods"""
    def player_two_ai(self):
        """Controls player two's turn"""
        if len(self.playerTwo.hand) <= 0:
            # Checking if the 2nd players hand is empty
            sys.exit()
        while self.currentTurn == "Player Two":
            for card in self.playerTwo.hand:
                # Looping through the 2nd players hand
                # and playing the first playable one
                if card.compare(self.currentCard):
                    if card.value == "skip" or card.value == "reverse":
                        self.isSkip = True
                    elif card.value == "plustwo":
                        self.isPlusTwo = True
                    cardIndex = self.playerTwo.hand.index(card)
                    x = self.playerTwo.hand.pop(cardIndex)
                    self.currentCard = x
                    self.pile.pile.append(x)
                    if self.isPlusTwo:
                        for i in range(2):
                            card = self.playerOne.draw(self.deck)
                            button = tk.Button(self.window, command = lambda newCard=card:self.play_card(newCard), image=card.image)
                            button.grid(column=self.currentIndex,row=5)
                            self.cardButtons.append(button)
                            self.currentIndex = self.currentIndex + 1
                            
                            self.isSkip = True
                            self.isPlusTwo = False
                    if self.isSkip:
                        self.update()
                        self.player_two_ai()
                        self.isSkip = False
                        return
                    self.update()
                    self.currentTurn = "Player One"
                    self.totalTurns += 1
                    return
                
                elif card.color == "wild":
                    cardIndex = self.playerTwo.hand.index(card)
                    x = self.playerTwo.hand.pop(cardIndex)
                    self.currentCard = x
                    self.pile.pile.append(x)
                    if card.value == "draw4":
                        for i in range(4):
                            card = self.playerOne.draw(self.deck)
                            button = tk.Button(self.window, command = lambda newCard=card:self.play_card(newCard), image=card.image)
                            button.grid(column=self.currentIndex,row=5)
                            self.cardButtons.append(button)
                            self.currentIndex = self.currentIndex + 1
                    self.currentCard.color = random.choice(["red", "green", "blue", "yellow"])
                    if card.value == "draw4":
                        self.currentCard.value = "draw"
                    if card.value == "wild":
                        self.currentCard.value = "none"
                    self.imagePath = f"images\\{self.currentCard.color}_wild.png"
                    self.currentCard.image = tk.PhotoImage(file=self.imagePath)
                    self.update()
                    self.totalTurns += 1
                    self.currentTurn = "Player One"
                    return
                        
            # Otherwise player two will draw a card and their turn will end
            self.playerTwo.draw(self.deck)
            self.update()
            self.totalTurns += 1
            self.currentTurn = "Player One" 


game = Main()