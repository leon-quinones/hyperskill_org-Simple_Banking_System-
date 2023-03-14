class MenuController:
    pass


class Menu:
    def __init__(self, controller=None, menu_options=None):
        if menu_options is None:
            menu_options = ['Exit',
                            'Create an account',
                            'Log into account'
                           ]
        if controller is None:
            self.controller = MenuController()

        self.menu_options = menu_options

    def print_menu(self):
        for i, option in enumerate(self.menu_options):
            print(f'{i + 1}. {option}')

    def choose_options(self, id_option: int):
        if 0 >= id_option or  id_option > len(self.menu_options):
            Exception("Option not supported")
        self.controller.getView(id_option)

    def get_user_input(self):
        return input()

menu = Menu()
menu.print_menu()