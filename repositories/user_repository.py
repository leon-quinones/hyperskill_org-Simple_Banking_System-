from model.credit_card import CreditCard
from model.user import UserDto, User


class UserRepository:
    def __init__(self, connection, cursor):
        self.cursor = cursor
        self.connection = connection

    def find_user_by_credentials(self, credit_card_number: int, user_pin: int):
        query = 'SELECT u.id, name, number, pin, balance FROM user as u ' \
                'INNER JOIN card as c ON u.card_id = c.id ' \
                'WHERE number = ? AND pin = ?;'

        # "SELECT * FROM card WHERE number = ? AND pin = ?;"
        self.cursor.execute(query, (credit_card_number, user_pin))
        user = self.__build_user_from_database(self.cursor.fetchone())
        # user = self.users.get(credit_card_number)
        # if user is not None:
        #     if user.pin != user_pin:
        #         user = None
        print(user)
        return user

    def create_user(self, userdto: UserDto):
        card_query = 'INSERT INTO card (number, pin, balance) VALUES (?, ?, ?);'
        find_card_query = 'SELECT id FROM card WHERE number = ?;'
        user_query = 'INSERT INTO user (name, card_id) VALUES (?, ?);'
        database_card_data = (userdto.credit_card.number, userdto.pin, userdto.balance)
        self.cursor.execute(card_query, database_card_data)
        self.connection.commit()
        # self.cursor.execute('select * from card')
        # print(self.cursor.fetchall())
        self.cursor.execute(find_card_query, (userdto.credit_card.number,))
        id_card: int = self.cursor.fetchone()
        self.cursor.execute(user_query, (userdto.name, id_card[0]))
        self.connection.commit()

        # self.users[userdto.credit_card.number] = userdto

    def __build_user_from_database(self, user_data: tuple):
        if user_data is None:
            return None
        card = CreditCard()
        card.number: int = user_data[2]
        user = User()
        user.credit_card = card
        user.id: int = user_data[0]
        user.name: str = user_data[1]
        user.pin: str = user_data[3]
        user.balance: int = user_data[4]
        return user
