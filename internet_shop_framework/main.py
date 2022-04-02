import quopri

from internet_shop_framework.requests import GetRequests, PostRequests


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class ISFramework:
    """Класс ISFramework - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.urls_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        url = environ['PATH_INFO']

        # добавление закрывающего слеша
        if not url.endswith('/'):
            url = f'{url}/'

        request = {}
        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = data
            print(f'Нам пришёл post-запрос: {ISFramework.decode_value(data)}')
        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = request_params
            print(f'Нам пришли GET-параметры: {request_params}')
        print(request)  # {'method': 'GET', 'request_params': {'id': '1', 'category': '10'}}

        # находим нужный контроллер
        # отработка паттерна page controller
        if url in self.urls_lst:
            view = self.urls_lst[url]
        else:
            view = PageNotFound404()
        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        for front in self.fronts_lst:  # можно сделать активного юзера, передавать между страницами
            front(request)
        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
