class GetMethods:

    @staticmethod
    def parse_input_data(data: str):
        result = {}
        if data:
            # делим параметры через &
            params = data.split('&')
            for item in params:
                # делим ключ и значение через =
                key, val = item.split('=')
                result[key] = val
        return result


# get requests
class GetRequests(GetMethods):

    @staticmethod
    def get_request_params(environ):
        # получаем параметры запроса
        query_string = environ['QUERY_STRING']
        # превращаем параметры в словарь
        request_params = GetRequests.parse_input_data(query_string)
        return request_params


# post requests
class PostRequests(GetMethods):

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        # получаем длину тела
        content_length_data = env.get('CONTENT_LENGTH')
        # приводим к int
        content_length = int(content_length_data) if content_length_data else 0
        # считываем данные, если они есть
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            # декодируем данные
            data_str = data.decode(encoding='utf-8')
            # собираем их в словарь
            result = self.parse_input_data(data_str)
        return result

    def get_request_params(self, environ):
        # получаем данные
        data = self.get_wsgi_input_data(environ)
        # превращаем данные в словарь
        data = self.parse_wsgi_input_data(data)
        return data

# {'method': 'POST', 'data':
# {'name': '%D0%95%D0%B3%D0%BE%D1%80',
# 'email': 'egor%40yandex.ru',
# 'member': 'yes',
# 'suggestion': '%D0%92%D1%81%D0%B5+%D1%85%D0%BE%D1%80%D0%BE%D1%88%D0%BE%21'}}
