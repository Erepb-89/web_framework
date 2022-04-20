import copy
import quopri


# абстрактный пользователь
class User:
    pass


# админ
class Admin(User):
    pass


# покупатель
class Buyer(User):
    pass


# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {
        'admin': Admin,
        'buyer': Buyer
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


# порождающий паттерн Прототип - Продукт
class ProductPrototype:
    # прототип товара

    def clone(self):
        return copy.deepcopy(self)


class Product(ProductPrototype):

    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.category.products.append(self)
        self.price = price


# Диван
class Sofa(Product):
    pass


# Кресло
class Armchair(Product):
    pass


# Стул
class Chair(Product):
    pass


# Стол
class Table(Product):
    pass


# Категория
class Category:
    # реестр?
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.products = []

    def products_count(self):
        result = len(self.products)
        # if self.category:
        #     result += self.category.products_count()
        return result


# порождающий паттерн Абстрактная фабрика - фабрика продуктов
class ProductFactory:
    types = {
        'sofa': Sofa,
        'armchair': Armchair,
        'chair': Chair,
        'table': Table
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category, price):
        return cls.types[type_](name, category, price)


# Основной интерфейс проекта
class Engine:
    def __init__(self):
        self.admins = []
        self.buyers = []
        self.products = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            # print(item.name, item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_product(type_, name, category, price):
        return ProductFactory.create(type_, name, category, price)

    def get_product(self, name):
        for item in self.products:
            if item.name == name:
                return item
        # return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        # print('log--->', text)
        with open('log.txt', 'a', encoding="UTF-8") as file:
            file.write(f"{text}\n")
