import random

from model.credit_card import CreditCard


class User:
    def __init__(self):
        self.credit_card: CreditCard = None
        self.pin: int = None
        self.balance: float = None


    def create_pin(self):
        self.pin = random.randint(1000, 9999)

    def assign_credit_card(self, credit_card: CreditCard):
        self.credit_card = credit_card

    def assign_balance(self, balance: float):
        self.balance = balance


class UserDto:
    def __init__(self, credit_card_number: int, user_pin: int, balance: float, name: str):
        self.credit_card: CreditCard = credit_card_number
        self.pin: int = user_pin
        self.balance = balance
        self.name = name
