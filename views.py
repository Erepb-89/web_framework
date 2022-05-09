from architectural_system_pattern_unit_of_work import UnitOfWork
from internet_shop_framework.templator import render
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, ListView, CreateView, BaseSerializer
from patterns.сreational_patterns import Engine, Logger, MapperRegistry
from patterns.structural_patterns import AppRoute, Debug
from datetime import datetime

site = Engine()

logger = Logger('main')

routes = {}
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


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
            category_products = site.get_products_by_category(category.id)
            return '200 OK', render(
                'products_list.html',
                objects_list=category_products,
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

            new_category = site.create_category(name)
            site.categories.append(new_category)

            # добавление в бд
            new_category.mark_new()
            UnitOfWork.get_current().commit()

            return '200 OK', render(
                'categories.html',
                objects_list=site.categories,
                products_count_by_category=site.products_count_by_category
            )
        else:
            return '200 OK', render(
                'create_category.html',
                categories=site.categories
            )


# контроллер - список категорий Админка
@AppRoute(routes=routes, url='/categories/')
class Categories:
    @Debug(name='Categories')
    def __call__(self, request):
        logger.log(f'Список категорий --> {datetime.now()}')
        return '200 OK', render(
            'categories.html',
            objects_list=site.categories,
            products_count_by_category=site.products_count_by_category
        )


# контроллер - удалить категорию
@AppRoute(routes=routes, url='/delete-category/')
class DeleteCategory:
    def __call__(self, request):
        # request_params = request['request_params']

        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            site.categories.remove(category)
            # удаление из бд
            category.mark_removed()
            UnitOfWork.get_current().commit()

            return '200 OK', render(
                'categories.html',
                objects_list=site.categories,
                products_count_by_category=site.products_count_by_category
            )
        except KeyError:
            return '200 OK', 'No category with such id is added yet'


# контроллер - создать продукт
@AppRoute(routes=routes, url='/create-product/')
class CreateProduct:

    @Debug(name='CreateProduct')
    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            price = data['price']
            price = site.decode_value(price)

            category = site.find_category_by_id(int(self.category_id))

            product = site.create_product(category.name, name, category.id, price=price)
            # Добавляем наблюдателей на продукт
            product.observers.append(email_notifier)
            product.observers.append(sms_notifier)

            site.products.append(product)
            product.mark_new()
            UnitOfWork.get_current().commit()

            category_products = site.get_products_by_category(category.id)

            return '200 OK', render('products_list.html',
                                    objects_list=category_products,
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

                new_product.mark_new()
                UnitOfWork.get_current().commit()

            # category = site.find_category_by_id(int(request['request_params']['id']))
            # category_products = site.get_products_by_category(category.id)

            return '200 OK', render(
                'products_list.html',
                objects_list=site.products,
                # name=category.name,
                # id=category.id
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
            product = site.get_product(name)
            site.products.remove(product)
            # удаление из бд
            product.mark_removed()
            UnitOfWork.get_current().commit()

            return '200 OK', render(
                'products_list.html',
                objects_list=site.products
            )
        except KeyError:
            return '200 OK', 'No product with such a name is added yet'


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

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('buyer')
        return mapper.all()


@AppRoute(routes=routes, url='/create-buyer/')
class BuyerCreateView(CreateView):
    template_name = 'create_buyer.html'

    def create_obj(self, data: dict):
        username = data['name']
        username = site.decode_value(username)
        new_obj = site.create_user('buyer', username)
        site.buyers.append(new_obj)
        # добавление в бд
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


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
