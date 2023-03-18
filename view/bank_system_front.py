from controller.user_controller import UserController, UserRepository
from model.user import User


class Menu:
    def __init__(self, controller=None, menu_options=None, user_options=None):
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
                2: 'Logout',
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
        if id_option == 0:
            return False

    def main_menu(self):
        self.__print_menu(self.menu_options)
        return self.select_main_menu(self.get_user_input())

    def user_menu(self, user: User):
        self.__print_menu(self.user_options)
        return self.select_user_menu(user, self.get_user_input())

    def select_main_menu(self, id_option: int):
        Menu.__validate_selected_option(id_option, self.menu_options)
        print()
        if id_option == 1:
            user: User = self.controller.get_option(id_option)
            card_number = user.credit_card.number
            print(f"Your card has been created \n"
                  f"Your card number: \n"
                  f"{card_number} \n"
                  f"Your card PIN: \n"
                  f"{user.pin}")
            print()
            return True

        if id_option == 2:
            card_number, pin = self.get_user_credentials()
            user: User = self.controller.get_option(id_option, card_number=card_number, user_pin=pin)
            if user is None:
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
                    user_is_logged, user_run_app = self.user_menu(user)

                if user_run_app is False:
                    return False
                else:
                    return True

    def select_user_menu(self, user: User, id_option: int):
        Menu.__validate_selected_option(id_option, self.user_options)
        print()
        if id_option == 0:
            return False, False
        if id_option == 1:
            print(f'Balance: {user.balance}')
            return True, True
        if id_option == 2:
            print(f'You have successfully logged out!\n')
            return False, True

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
            user_pin = input('Enter your PIN code: \n')
            if len(user_pin) != 4:
                raise Exception()
        except ValueError or Exception:
            print("Please enter a valid pin number...")
            self.get_user_credentials()

        return int(credit_card), int(user_pin)

# menu = Menu()
# menu.main_menu()
