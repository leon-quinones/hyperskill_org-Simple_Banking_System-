import view.bank_system_front


class AppMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class BankApp(metaclass=AppMeta):
    def some_business_logic(self):
        pass