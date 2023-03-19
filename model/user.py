import random

from model.credit_card import CreditCard


class User:
    def __init__(self):
        self.id = 0
        self.name = ''
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
    def __init__(self, credit_card: CreditCard, user_pin: int, balance: int, name: str):
        self.credit_card: CreditCard = credit_card
        self.pin: int = user_pin
        self.balance: int = balance
        self.name: str = name
