from model.credit_card import CreditCard
from model.user import User, UserDto


class UserRepository:
    def __init__(self):
        self.users: dict = { }

    def find_user_by_credentials(self,credit_card_number: int, user_pin: int):
        user = self.users.get(credit_card_number)
        if user.pin != user_pin:
            user = None
        return user

    def create_user(self, userdto: UserDto):
        self.users[userdto.credit_card.number] = userdto


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

    def create_account(self, user_base_number=250000000):
        user = User()
        user.create_pin()
        user.assign_credit_card(CreditCard(user_base_number))
        user.assign_balance(0.0)
        self.user_repository.create_user(user)
        print(user.pin, user.credit_card)
        return user

    def get_option(self, option: int, **kwargs):
        if option == 1:
            return self.create_account()

        if option == 2:
            card_number = kwargs.get("card_number", None)
            user_pin = kwargs.get("user_pin", None)
            if card_number is None or user_pin is None:
                raise Exception("Please insert a valid card number and PIN")
            return self.login(card_number, user_pin)



