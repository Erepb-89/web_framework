import copy
import quopri
import sqlite3

from architectural_system_pattern_unit_of_work import DomainObject
from behavioral_patterns import FileWriter, Subject, ConsoleWriter


class User:
    """Абстрактный пользователь"""

    def __init__(self, name):
        self.name = name


class Admin(User):
    """Админ"""
    pass


class Buyer(User, DomainObject):
    """Покупатель"""

    def __init__(self, name):
        self.products = []
        super().__init__(name)


class UserFactory:
    """Абстрактная фабрика пользователей"""
    types = {
        'admin': Admin,
        'buyer': Buyer
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class ProductPrototype:
    """Прототип товара"""

    def clone(self):
        return copy.deepcopy(self)


class Product(ProductPrototype, Subject, DomainObject):
    """Продукт"""

    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price
        self.buyers = []
        super().__init__()

    def __getitem__(self, item):
        return self.buyers[item]

    def subscribe(self, user: Buyer):
        self.buyers.append(user)
        user.products.append(self)
        print('user:', user.name, 'product:', user.products[0].name)
        self.notify()


class Sofa(Product):
    """Диван"""
    pass


class Armchair(Product):
    """Кресло"""
    pass


class Chair(Product):
    """Стул"""
    pass


class Table(Product):
    """Стол"""
    pass


class Category(DomainObject):
    """Категория товара"""
    auto_id = 0

    def __init__(self, name):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.products = []

    def products_count(self):
        result = len(self.products)
        return result


class ProductFactory:
    """Порождающий паттерн Абстрактная фабрика - фабрика продуктов"""
    types = {
        'диваны': Sofa,
        'стулья': Armchair,
        'кресла': Chair,
        'столы': Table
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category, price):
        return cls.types[type_](name, category, price)


class Engine:
    """Основной интерфейс проекта"""

    def __init__(self):
        buyers_mapper = MapperRegistry.get_current_mapper('buyer')
        products_mapper = MapperRegistry.get_current_mapper('product')
        categories_mapper = MapperRegistry.get_current_mapper('category')
        self.admins = []
        self.buyers = buyers_mapper.all()
        # self.buyers = []
        self.products = products_mapper.all()
        # self.products = []
        self.categories = categories_mapper.all()
        # self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name):
        return Category(name)

    def find_category_by_id(self, id):
        for item in self.categories:
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
        return None

    def get_products_by_category(self, category_id):
        result_list = [item for item in self.products if item.category == category_id]
        return result_list

    def products_count_by_category(self, category_id):
        result_list = [item for item in self.products if item.category == category_id]
        return len(result_list)

    def get_buyer(self, name) -> Buyer:
        for item in self.buyers:
            if item.name == name:
                return item

    def categories_count(self):
        result = len(self.categories)
        return result

    def buyers_count(self):
        result = len(self.buyers)
        return result

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class SingletonByName(type):
    """Порождающий паттерн Синглтон"""

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
    """Логгер"""

    def __init__(self, name, writer=FileWriter('log.txt')):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)


class BuyerMapper:
    """
    Архитектурный системный паттерн - Data Mapper
    Маппер покупателя
    """

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'buyer'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            buyer = Buyer(name)
            buyer.id = id
            result.append(buyer)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Buyer(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем объект из базы
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CategoryMapper:
    """
    Архитектурный системный паттерн - Data Mapper
    Маппер категории
    """

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'category'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            category = Category(name)
            category.id = id
            result.append(category)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Category(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем объект из базы
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class ProductMapper:
    """
    Архитектурный системный паттерн - Data Mapper
    Маппер пролукта
    """

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'product'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, category, price = item
            product = Product(name, category, price)
            product.id = id
            result.append(product)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name, category, price FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Product(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, category, price) VALUES (?, ?, ?)"
        self.cursor.execute(statement, (obj.name, obj.category, obj.price))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=?, category=?, price=? WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем объект из базы
        self.cursor.execute(statement, (obj.name, obj.category, obj.price, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = sqlite3.connect('patterns.sqlite')


class MapperRegistry:
    """Порождающий паттерн Абстрактная фабрика - фабрика мапперов"""
    mappers = {
        'buyer': BuyerMapper,
        'category': CategoryMapper,
        'product': ProductMapper
    }

    @staticmethod
    def get_mapper(obj):

        if isinstance(obj, Buyer):
            return BuyerMapper(connection)
        if isinstance(obj, Category):
            return CategoryMapper(connection)
        if isinstance(obj, Product):
            return ProductMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')
