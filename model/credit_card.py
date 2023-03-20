import random


class CreditCard:
    __inn = '400000'

    def __init__(self, initial_customer_number: int = 150000000):
        self.__digits = []
        self.__customer_number = 0
        self.number = 0

        self.build_customer_number(initial_customer_number)
        self.build_card_number()

    def build_checksum(self):
        aux = self.__digits.copy()
        for i in range(0, len(self.__digits), 2):
            c = self.__digits[i] * 2  # calculate value
            aux[i] = c - 9 if c > 9 else c
        checknum = 10 - (sum(aux) % 10)
        return 0 if checknum > 9 else checknum

    def build_customer_number(self, initial_customer_number: int):
        if initial_customer_number // 100000000 < 1 or initial_customer_number // 100000000 > 9:
            raise Exception("base user number must have 9 digits")
        self.__customer_number = random.randint(initial_customer_number, 999999999)

    def build_card_number(self):
        self.__digits = list(map(int, CreditCard.__inn))
        self.__digits += list(map(int, str(self.__customer_number)))
        self.__digits += [self.build_checksum()]
        self.number = int(''.join(map(str, self.__digits)))

