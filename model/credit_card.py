import random


class CreditCard:
    __inn: int = 400000
    __inn_factor = 10 ** 10
    __customer_number_factor = 10

    def __init__(self, initial_customer_number: int):
        self.__checknumber = 0
        self.__customer_number = 0
        self.number = 0

        self.build_checksum()
        self.build_customer_number(initial_customer_number)
        self.build_card_number()

    def build_checksum(self):
        self.__checknumber = random.randint(0, 9)

    def build_customer_number(self, initial_customer_number: int):
        if initial_customer_number // 100000000 < 1 or initial_customer_number // 100000000 > 9:
            raise Exception("base user number must have 9 digits")
        self.__customer_number = random.randint(initial_customer_number, 999999999)

    def build_card_number(self):
        print(CreditCard.__inn)
        print(self.__customer_number)
        print(self.__checknumber)
        self.number = CreditCard.__inn * CreditCard.__inn_factor
        print(self.number)
        self.number += self.__customer_number * CreditCard.__customer_number_factor
        print(self.number)
        self.number += self.__checknumber
        print(self.number)


# card = CreditCard(250000000)
# print(card.number)
