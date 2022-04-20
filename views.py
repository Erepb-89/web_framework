from internet_shop_framework.templator import render
from patterns.сreational_patterns import Engine, Logger

site = Engine()
site.admins = ['Erepb', 'Nik']
site.buyers = ['Andrey', 'Ilya']

new_category1 = site.create_category('стулья', 0)
new_category2 = site.create_category('столы', 1)
new_category3 = site.create_category('кресла', 2)
new_category4 = site.create_category('диваны', 3)
site.categories.append(new_category1)
site.categories.append(new_category2)
site.categories.append(new_category3)
site.categories.append(new_category4)

product1 = site.create_product('sofa', 'красивый диван', category=site.find_category_by_id(3), price=50000)
product2 = site.create_product('sofa', 'обычный диван', category=site.find_category_by_id(3), price=25000)
product3 = site.create_product('chair', 'красивый стул1', category=site.find_category_by_id(0), price=6000)
product4 = site.create_product('chair', 'красивый стул2', category=site.find_category_by_id(0), price=7000)
product5 = site.create_product('chair', 'обычный стул', category=site.find_category_by_id(0), price=4000)
product6 = site.create_product('armchair', 'красивое кресло', category=site.find_category_by_id(2), price=15000)
product7 = site.create_product('armchair', 'обычное кресло', category=site.find_category_by_id(2), price=10000)
product8 = site.create_product('table', 'красивый стол', category=site.find_category_by_id(1), price=30000)
product9 = site.create_product('table', 'обычный стол', category=site.find_category_by_id(1), price=15000)
site.products.append(product1)
site.products.append(product2)
site.products.append(product3)
site.products.append(product4)
site.products.append(product5)
site.products.append(product6)
site.products.append(product7)
site.products.append(product8)
site.products.append(product9)

logger = Logger('main')


class Index:
    def __call__(self, request):
        return '200 OK', render(
            'index.html',
            today=request.get('today', None),
            style=request.get('style', None))


class Contacts:
    def __call__(self, request):
        return '200 OK', render(
            'contact.html',
            today=request.get('today', None),
            style=request.get('style', None))


# контроллер - список продуктов
class Products:
    def __call__(self, request):
        print(request['request_params'])
        return '200 OK', render(
            'products.html',
            today=request.get('today', None),
            style=request.get('style', None))


# контроллер - список продуктов Админка
class ProductsList:
    def __call__(self, request):
        logger.log('Список продуктов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render(
                'products_list.html',
                objects_list=category.products,
                name=category.name,
                id=category.id,
                today=request.get('today', None),
                style=request.get('style', None)
            )
        except KeyError:
            return '200 OK', 'No products have been added yet'


class Suggestions:
    def __call__(self, request):
        return '200 OK', render(
            'suggestions.html',
            today=request.get('today', None),
            style=request.get('style', None))


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# контроллер - создать категорию
class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render(
                'categories.html',
                objects_list=site.categories,
                today=request.get('today', None),
                style=request.get('style', None)
            )
        else:
            categories = site.categories
            return '200 OK', render(
                'create_category.html',
                categories=categories,
                today=request.get('today', None),
                style=request.get('style', None)
            )


# контроллер - список категорий Админка
class Categories:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render(
            'categories.html',
            objects_list=site.categories,
            today=request.get('today', None),
            style=request.get('style', None)
        )


# контроллер - создать продукт
class CreateProduct:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            price = data['price']
            price = site.decode_value(price)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                product = site.create_product('sofa', name, category, price=price)
                site.products.append(product)

            return '200 OK', render('products_list.html',
                                    objects_list=category.products,
                                    name=category.name,
                                    id=category.id,
                                    today=request.get('today', None),
                                    style=request.get('style', None)
                                    )

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render(
                    'create_product.html',
                    name=category.name,
                    id=category.id,
                    today=request.get('today', None),
                    style=request.get('style', None)
                )
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# контроллер - копировать продукт
class CopyProduct:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_product = site.get_product(name)
            if old_product:
                new_name = f'copy_{name}'
                new_product = old_product.clone()
                new_product.name = new_name
                site.products.append(new_product)

            return '200 OK', render(
                'products_list.html',
                objects_list=site.products,
                today=request.get('today', None),
                style=request.get('style', None)
            )
        except KeyError:
            return '200 OK', 'No products have been added yet'
