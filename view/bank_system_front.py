from controller.user_controller import UserController
from model.user import User


class Menu:
    def __init__(self, controller=None, menu_options=None, user_options = None):
        if menu_options is None:
            menu_options = {
                1: 'Create an account',
                2: 'Log into account',
                0: 'Exit'
            }

        if controller is None:
            controller = UserController()

        if user_options is None:
            user_options = {
                1: 'Balance',
                2: 'Logout',
                0: 'Exit'
            }

        self.controller = controller
        self.menu_options = menu_options
        self.user_options = user_options

    def __print_menu(self, menu: dict):
        for i, key in enumerate(menu.keys()):
            print(f'{key}. {menu.get(key)}')

    def main_menu(self):
        self.__print_menu(self.menu_options)
        return self.select_main_menu(self.get_user_input())

    def user_menu(self):
        self.__print_menu(self.user_options)
        return self.user_menu()

    def select_main_menu(self, id_option: int):
        if 0 >= id_option or id_option > len(self.menu_options):
            raise Exception("Option not supported")
        if id_option == 0:
            return False

        if id_option == 1:
            user: User = self.controller.get_option(id_option)
            card_number = user.credit_card.number
            print(f"Your card has been created \n"
              f"Your card number: \n"
              f"{card_number} \n"
              f"Your card PIN: \n"
              f"{user.pin}")
            return True

        if id_option == 2:
            self.get_user_credentials()
            user: User = self.controller.get_option(id_option)
            if user is None:
                print('Wrong card number or PIN!')

    def select_user_menu(self, user_option: int):
        pass

    def get_user_input(self):
        try:
            option = int(input())
        except ValueError:
            print("Please enter a valid option number...")
            self.print_menu()
        return int(option)

    def get_user_credentials(self):
        credit_card = None
        user_pin = None
        try:
            print('Enter your card number:')
            credit_card = input()
            if len(credit_card) != 16:
                print("card number must have 16 digits.")
                raise Exception()
        except ValueError or Exception():
            print("Please enter a valid 16-digit credit card number...")
            self.get_user_credentials()
        try:
            user_pin = input('Enter your card number: \n')
            if len(user_pin) != 4:
                raise Exception()
        except ValueError or Exception:
            print("Please enter a valid pin number...")
            self.get_user_credentials()

        return credit_card, user_pin


# menu = Menu()
# menu.print_menu()
