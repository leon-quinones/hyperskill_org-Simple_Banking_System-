from collections import namedtuple
from sqlite3 import OperationalError

from model.credit_card import CreditCard
from model.user import User, UserDto
from repositories.user_repository import UserRepository


class UserController:

    def __init__(self, __user_repository: UserRepository):
        # self.is_app_running = True
        self.user_repository = __user_repository

    # def continue_app(self):
    #     self.is_app_running = False

    def login(self, credit_card_number: int, user_pin: int):
        try:
            user: User = self.user_repository.find_user_by_credentials(credit_card_number, user_pin)
        except ValueError:
            raise Exception("User not found")
            user = None
        return user

    def create_account(self, user_base_number=250000000, name="John Smith"):
        user = User()
        user.create_pin()
        user.name = name
        user.assign_credit_card(CreditCard(user_base_number))
        user.assign_balance(0)
        self.user_repository.create_user(user)
        return user

    def delete_account(self, user_id: int):
        # try:
        account_id = self.user_repository.find_account_by_user_id(user_id)
        self.user_repository.delete_account(account_id)
        return True
        # except OperationalError:
        #     return False

    def change_balance(self, user_id: int, new_balance: int):
        # try:
        self.user_repository.update_balance(user_id, new_balance)
        return True
        # except OperationalError:
        #     return False

    def get_user_balance(self, user_id: int):
        user = self.user_repository.find_user_by_id(user_id)
        return user.balance

    def get_card_id(self, user_id: int):
        return self.user_repository.find_account_by_user_id(user_id);

    def make_transaction(self, transaction_data: namedtuple):
        account_id = self.user_repository.find_account_by_card_number(
            transaction_data.card_number_to_transfer)
        if account_id is None:
            print('Such a card does not exist.')
            return True
        user = self.user_repository.find_user_by_id(transaction_data.user_id)
        if transaction_data.new_balance > user.balance:
            print('Not enough money!')
            return True
        #            user_card_id: int, card_number_to_transfer: int, new_balance: int
        self.user_repository.update_balance(transaction_data.user_card_id, -1 * transaction_data.new_balance)
        self.user_repository.update_balance(account_id, transaction_data.new_balance)
        return True

    def get_option(self, option: int, **kwargs):
        if option == 1:
            return self.create_account()

        if option == 2:
            card_number = kwargs.get("card_number", None)
            user_pin = kwargs.get("user_pin", None)
            if card_number is None or user_pin is None:
                raise Exception("Please insert a valid card number and PIN")
            return self.login(card_number, user_pin)
