from datetime import date
from views import Index, Contacts, Products, Suggestions


# front controller
def date_front(request):
    request['data'] = date.today()


def style(request):
    """css"""
    with open('templates/style.css') as file:
        css_file = file.read()
        request['style'] = css_file


fronts = [date_front, style]

routes = {
    '/': Index(),
    '/contacts/': Contacts(),
    '/products/': Products(),
    '/suggestions/': Suggestions(),
}
