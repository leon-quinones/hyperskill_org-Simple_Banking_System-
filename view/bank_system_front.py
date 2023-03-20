from sqlite3 import OperationalError
from collections import namedtuple
from controller.user_controller import UserController, UserRepository
from model.user import User


class Menu:
    def __init__(self, controller=None, menu_options=None, user_options=None):
        self.user = None
        if menu_options is None:
            menu_options = {
                1: 'Create an account',
                2: 'Log into account',
                0: 'Exit'
            }

        if controller is None:
            __user_repository: UserRepository = UserRepository()
            controller = UserController(__user_repository)

        if user_options is None:
            user_options = {
                1: 'Balance',
                2: 'Add income',
                3: 'Do transfer',
                4: 'Close account',
                5: 'Log out',
                0: 'Exit'
            }

        self.controller = controller
        self.menu_options = menu_options
        self.user_options = user_options

    @staticmethod
    def __print_menu(menu: dict):
        for i, key in enumerate(menu.keys()):
            print(f'{key}. {menu.get(key)}')

    @staticmethod
    def __validate_selected_option(id_option: int, menu_options: dict):
        if 0 > id_option or id_option > len(menu_options):
            raise Exception("Option not supported")

    def main_menu(self):
        self.__print_menu(self.menu_options)
        return self.select_main_menu(self.get_user_option_input())

    def user_menu(self):
        self.__print_menu(self.user_options)
        return self.select_user_menu(self.get_user_option_input())

    def select_main_menu(self, id_option: int):
        Menu.__validate_selected_option(id_option, self.menu_options)
        print()
        if id_option == 1:
            self.user: User = self.controller.get_option(id_option)
            card_number = self.user.credit_card.number
            print(f"Your card has been created \n"
                  f"Your card number: \n"
                  f"{card_number} \n"
                  f"Your card PIN: \n"
                  f"{self.user.pin}")
            print()
            return True

        if id_option == 2:
            card_number, pin = self.get_user_credentials()
            self.user: User = self.controller.get_option(id_option, card_number=card_number, user_pin=pin)
            if self.user is None:
                print()
                print('Wrong card number or PIN!')
                print()
                return True
            else:
                user_is_logged = True
                user_run_app = True
                print()
                print('You have successfully logged in!')
                while user_is_logged and user_run_app:
                    print()
                    user_is_logged, user_run_app = self.user_menu()

                if user_run_app is False:
                    return False
                else:
                    return True

    def select_user_menu(self, id_option: int):
        Menu.__validate_selected_option(id_option, self.user_options)
        print()
        if id_option == 0:
            return False, False
        if id_option == 1:
            # user_balance = self.controller.get_user_balance(self.user.id)
            # if user_balance is None:
            #     raise OperationalError
            #
            # print(f'Balance: {user_balance}')
            print(f'Balance: {self.user.balance}')
            return True, True
        if id_option == 5:
            print(f'You have successfully logged out!\n')
            return False, True
        if id_option == 2:
            print(f'Enter income: ')
            income = self.get_user_income()
            account_id = self.controller.get_card_id(self.user.id)
            if account_id is None:
                raise OperationalError(f'card associated to user: {self.user.id} was not found')
            transaction_result = self.controller.change_balance(account_id, income)
            if transaction_result is False:
                raise OperationalError
            print('Income was added!')
            self.user.balance += income
            return True, True
        if id_option == 3:
            card_number = self.get_credit_card_number('Enter card number:')
            is_card_valid = self.luhn_check(card_number)
            if is_card_valid is False:
                print('Probably you made a mistake in the card number. Please try again!')
                return True, True
            print(f'Enter how much money you want to transfer:')
            transaction_amount = self.get_user_income()
            user_card_id = self.controller.get_card_id(self.user.id)
            TransactionData = namedtuple('TransactionData', ['user_id', 'user_card_id', 'card_number_to_transfer', 'new_balance'])
            # user_card_id: int, card_number_to_transfer: int, new_balance: int
            transaction_data = TransactionData(self.user.id, user_card_id, card_number, transaction_amount)
            transaction_result = self.controller.make_transaction(transaction_data)
            if transaction_result is False:
                raise OperationalError('Algo paso! en la database')
            print('Success!')
            self.user.balance -= transaction_amount
            return True, True
        if id_option == 4:
            account_was_closed = self.controller.delete_account(self.user.id)
            if account_was_closed is False:
                raise OperationalError('Lol algo paso')
            print('The account has been closed!')
            return False, True

    def get_user_income(self):
        try:
            income = int(input())
            if income <= 0:
                raise ValueError
        except ValueError:
            print("Please enter a valid income amount...")
            self.print_menu()
        return income


    def get_user_option_input(self):
        try:
            option = int(input())
        except ValueError:
            print("Please enter a valid option number...")
            self.print_menu()
        return int(option)

    def get_credit_card_number(self, message: str):
        try:
            print(message)
            credit_card = input()
            if len(credit_card) != 16:
                print("card number must have 16 digits.")
                raise Exception()
            return credit_card
        except ValueError or Exception():
            print("Please enter a valid 16-digit credit card number...")
            self.get_credit_card_number()

    def get_user_credentials(self):
        credit_card = None
        user_pin = None
        credit_card = self.get_credit_card_number('Enter your card number:')
        # try:
        #     print('Enter your card number:')
        #     credit_card = input()
        #     if len(credit_card) != 16:
        #         print("card number must have 16 digits.")
        #         raise Exception()
        # except ValueError or Exception():
        #     print("Please enter a valid 16-digit credit card number...")
        #     self.get_user_credentials()
        try:
            user_pin = input('Enter your PIN code: \n')
            if len(user_pin) != 4:
                raise Exception()
        except ValueError or Exception:
            print("Please enter a valid pin number...")
            self.get_user_credentials()

        return int(credit_card), int(user_pin)

    def luhn_check(self, credit_card_number: str):
        card_number = list(map(int, credit_card_number))
        return True if sum(card_number) % 10 else False
# menu = Menu()
# menu.main_menu()
