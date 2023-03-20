from model.credit_card import CreditCard
from model.user import UserDto, User


class UserRepository:
    def __init__(self, connection, cursor):
        self.cursor = cursor
        self.connection = connection

    def __build_user_from_database(self, user_data: tuple):
        if user_data is None:
            return None
        card = CreditCard()
        card.number: int = user_data[2] if user_data[2] is not None else None
        user = User()
        user.credit_card = card
        user.id: int = user_data[0] if user_data[0] is not None else None
        user.name: str = user_data[1] if user_data[1] is not None else None
        user.pin: str = user_data[3] if user_data[3] is not None else None
        user.balance: int = user_data[4] if user_data[4] is not None else None
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

    def delete_account(self, card_id: int):
        card_delete_query = 'DELETE FROM card WHERE id = ?;'
        card_find_query = 'SELECT id FROM card WHERE id = ?;'
        self.cursor.execute(card_delete_query, (card_id,))
        self.connection.commit()
        self.cursor.execute(card_find_query, (card_id,))
        find_query_result = self.cursor.fetchone()
        found_card_id = find_query_result[0] if find_query_result is not None else 0
        return True if card_id == found_card_id else False

    def find_account_by_card_number(self, card_number_to_transfer):
        query = 'SELECT id FROM card WHERE number = ?;'
        self.cursor.execute(query, (card_number_to_transfer,))
        query_result = self.cursor.fetchone()
        if query_result is None:
            return None
        return query_result[0]

    def find_user_by_credentials(self, credit_card_number: int, user_pin: int):
        query = 'SELECT u.id, name, number, pin, balance FROM user as u ' \
                'INNER JOIN card as c ON u.card_id = c.id ' \
                'WHERE number = ? AND pin = ?;'

        # "SELECT * FROM card WHERE number = ? AND pin = ?;"
        self.cursor.execute(query, (credit_card_number, user_pin))
        fetched_user = self.cursor.fetchone()
        print(fetched_user)
        user = self.__build_user_from_database(fetched_user)
        # user = self.users.get(credit_card_number)
        # if user is not None:
        #     if user.pin != user_pin:
        #         user = None
        return user

    def find_user_by_id(self, user_id: int):
        query = 'SELECT u.id, name, number, pin, balance FROM user as u ' \
                'INNER JOIN card as c ON u.card_id = c.id ' \
                'WHERE u.id = ? ;'
        self.cursor.execute(query, (user_id,))
        query_result = self.cursor.fetchone()
        if query_result is None:
            return None
        return self.__build_user_from_database(query_result)

    def update_balance(self, card_id: int, new_balance: int):
        query = 'UPDATE card ' \
                'SET balance = balance + ? ' \
                'WHERE id = ?;'
        self.cursor.execute(query, (new_balance, card_id))
        self.connection.commit()

    def find_account_by_user_id(self, user_id):
        query = 'SELECT card_id FROM user WHERE id = ?;'
        self.cursor.execute(query, (user_id,))
        query_result = self.cursor.fetchone()
        if query_result is None:
            return None
        return int(query_result[0])
