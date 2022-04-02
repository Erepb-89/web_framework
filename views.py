from internet_shop_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render(
            'index.html',
            data=request.get('data', None),
            style=request.get('style', None))


class Contacts:
    def __call__(self, request):
        return '200 OK', render(
            'contact.html',
            data=request.get('data', None),
            style=request.get('style', None))


class Products:
    def __call__(self, request):
        return '200 OK', render(
            'products.html',
            data=request.get('data', None),
            style=request.get('style', None))


class Suggestions:
    def __call__(self, request):
        return '200 OK', render(
            'suggestions.html',
            data=request.get('data', None),
            style=request.get('style', None))


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'
