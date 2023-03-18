import view.bank_system_front as view
from controller.user_controller import UserController, UserRepository


class AppMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class BankApp(metaclass=AppMeta):
    def __init__(self):
        self.__is_running = True

    def run(self):
        __user_repository: UserRepository = UserRepository()
        controller = UserController(__user_repository)
        menu = view.Menu(controller=controller)
        while self.__is_running:
            self.__is_running = menu.main_menu()
            print(f'This is app_running: {self.__is_running}')
        print('Bye!')

    def stop_app(self):
        self.__is_running = False


app = BankApp()
app.run()
