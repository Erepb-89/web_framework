from internet_shop_framework.templator import render
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, ListView, CreateView, BaseSerializer
from patterns.сreational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug
from datetime import datetime

site = Engine()
# site.create_user('admin', 'Erepb')
# site.create_user('admin', 'Nik')
buyer1 = site.create_user('buyer', 'Andrey')
buyer2 = site.create_user('buyer', 'Ilya')
buyer3 = site.create_user('buyer', 'Evgeniy')
buyer4 = site.create_user('buyer', 'Petr')
site.buyers.append(buyer1)
site.buyers.append(buyer2)
site.buyers.append(buyer3)
site.buyers.append(buyer4)

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

routes = {}
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


# контроллер - главная
@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render(
            'index.html')


# контроллер - контакты
@AppRoute(routes=routes, url='/contacts/')
class Contacts:
    @Debug(name='Contacts')
    def __call__(self, request):
        return '200 OK', render(
            'contact.html')


# контроллер - список продуктов
@AppRoute(routes=routes, url='/products/')
class Products:
    @Debug(name='Products')
    def __call__(self, request):
        print(request['request_params'])
        return '200 OK', render(
            'products.html')


# контроллер - список продуктов Админка
@AppRoute(routes=routes, url='/products-list/')
class ProductsList:
    @Debug(name='ProductsList')
    def __call__(self, request):
        logger.log(f'Список продуктов --> {datetime.now()}')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render(
                'products_list.html',
                objects_list=category.products,
                name=category.name,
                id=category.id
            )
        except KeyError:
            return '200 OK', 'No products have been added yet'


# контроллер - пожелания
@AppRoute(routes=routes, url='/suggestions/')
class Suggestions:
    @Debug(name='Suggestions')
    def __call__(self, request):
        return '200 OK', render(
            'suggestions.html')


# контроллер 404
class NotFound404:
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# контроллер - создать категорию
@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    @Debug(name='CreateCategory')
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост
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
                objects_list=site.categories
            )
        else:
            categories = site.categories
            return '200 OK', render(
                'create_category.html',
                categories=categories
            )


# контроллер - список категорий Админка
@AppRoute(routes=routes, url='/categories/')
class Categories:
    @Debug(name='Categories')
    def __call__(self, request):
        logger.log(f'Список категорий --> {datetime.now()}')
        return '200 OK', render(
            'categories.html',
            objects_list=site.categories
        )


# контроллер - создать продукт
@AppRoute(routes=routes, url='/create-product/')
class CreateProduct:
    category_id = -1

    @Debug(name='CreateProduct')
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
                # Добавляем наблюдателей на продукт
                product.observers.append(email_notifier)
                product.observers.append(sms_notifier)

                site.products.append(product)

            return '200 OK', render('products_list.html',
                                    objects_list=category.products,
                                    name=category.name,
                                    id=category.id
                                    )

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render(
                    'create_product.html',
                    name=category.name,
                    id=category.id
                )
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# контроллер - копировать продукт
@AppRoute(routes=routes, url='/copy-product/')
class CopyProduct:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            name = site.decode_value(name)
            old_product = site.get_product(name)
            if old_product:
                new_name = f'{name}_1'
                new_product = old_product.clone()
                new_product.name = new_name
                site.products.append(new_product)

            return '200 OK', render(
                'products_list.html',
                objects_list=site.products
            )
        except KeyError:
            return '200 OK', 'No products have been added yet'


# контроллер - удалить продукт
@AppRoute(routes=routes, url='/delete-product/')
class DeleteProduct:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            name = site.decode_value(name)
            site.products.remove(site.get_product(name))

            return '200 OK', render(
                'products_list.html',
                objects_list=site.products
            )
        except KeyError:
            return '200 OK', 'No product with such a name yet'


@AppRoute(routes=routes, url='/admins-options/')
class AdminView(ListView):
    template_name = 'admins_options.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['categories_count'] = site.categories_count()
        context['buyers_count'] = site.buyers_count()
        return context

@AppRoute(routes=routes, url='/buyers/')
class BuyerListView(ListView):
    queryset = site.buyers
    template_name = 'buyers.html'


@AppRoute(routes=routes, url='/create-buyer/')
class BuyerCreateView(CreateView):
    template_name = 'create_buyer.html'

    def create_obj(self, data: dict):
        username = data['name']
        username = site.decode_value(username)
        new_obj = site.create_user('buyer', username)
        site.buyers.append(new_obj)


@AppRoute(routes=routes, url='/subscribe/')
class SubscribeCreateView(CreateView):
    """Подписка покупателя на товар"""
    template_name = 'subscribe_buyer.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['products'] = site.products
        context['buyers'] = site.buyers
        return context

    def create_obj(self, data: dict):
        product_name = data['product_name']
        product_name = site.decode_value(product_name)
        product = site.get_product(product_name)
        buyer_name = data['buyer_name']
        buyer_name = site.decode_value(buyer_name)
        buyer = site.get_buyer(buyer_name)
        product.subscribe(buyer)


@AppRoute(routes=routes, url='/api/')
class ProductApi:
    @Debug(name='ProductApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.products).save()
