import view.bank_system_front as view
import model.credit_card as model


class AppMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class BankApp(metaclass=AppMeta):
    def __init__(self):
        self.__is_running = None

    def run(self):
        while self.__is_running:
            menu = view.Menu()
            self.__is_running = menu.main_menu()
        print('Bye!')

    def stop_app(self):
        self.__is_running = False


app = BankApp()
app.run()
