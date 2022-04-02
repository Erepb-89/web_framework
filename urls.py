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


# def fonts(request):
#     """fonts"""
#     with open('templates/fonts/font-awesome/css/font-awesome.css') as file:
#         font_file = file.read()
#         request['fonts'] = font_file


fronts = [date_front, style]

routes = {
    '/': Index(),
    '/contacts/': Contacts(),
    '/products/': Products(),
    '/suggestions/': Suggestions(),
}
