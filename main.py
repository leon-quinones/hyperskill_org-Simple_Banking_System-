import view.bank_system_front as view
from controller.user_controller import UserController, UserRepository
import sqlite3


class AppMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class BankApp(metaclass=AppMeta):
    def __init__(self):
        self.database_cursor = None
        self.__is_running = True
        self.connect_database()

    def connect_database(self):
        self.conn = sqlite3.connect('card.s3db', timeout=1000)
        self.database_cursor = self.conn.cursor()
        self.database_cursor.execute(
            'CREATE TABLE IF NOT EXISTS card ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,' 
            'number TEXT UNIQUE,'
            'pin TEXT,'
            'balance INTEGER DEFAULT 0'
            ');')
        self.conn.commit()
        self.database_cursor.execute(
            'CREATE TABLE IF NOT EXISTS user ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'name TEXT, '
            'card_id INTEGER NOT NULL,'
            'CONSTRAINT fk_card_user FOREIGN KEY (card_id)'
            'REFERENCES card (id)'
            ');')
        self.conn.commit()

    def run(self):
        __user_repository: UserRepository = UserRepository(self.conn, self.database_cursor)
        controller = UserController(__user_repository)
        menu = view.Menu(controller=controller)
        while self.__is_running:
            self.__is_running = menu.main_menu()
        print('Bye!')

    def stop_app(self):
        self.__is_running = False


app = BankApp()
app.run()
