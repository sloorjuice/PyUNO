import tkinter as tk
from tkinter import PhotoImage

class Card:
    """Creates a card"""
    def __init__(self, color:str, value:str) -> None:
        # Creating card stats and attaching the picture
        self.color = color
        self.value = str(value)
        self.imagePath = f"images\\{color}_{value}.png"
        self.image = PhotoImage(file=self.imagePath)

    def compare(self, card):
        """Compares a card to another card based on either value or color"""
        if self.color == card.color or self.value == card.value:
            return True
        else:
            return False
        
    def __repr__(self) -> str:
        """Controls how the card is displayed in a Print()"""
        return f"{self.color} {self.value}"