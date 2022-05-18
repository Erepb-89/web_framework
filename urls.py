"""Urls"""

from datetime import date

# front controller
with open('templates/style.css', encoding='utf-8') as file:
    css_file = file.read()


def date_front(request):
    request['today'] = date.today()


def style(request):
    """css"""
    request['style'] = css_file


fronts = [date_front, style]

STYLE = css_file
DATE = date.today()

# routes = {
#     '/': Index(),
#     '/contacts/': Contacts(),
#     '/products/': Products(),
#     '/products-list/': ProductsList(),
#     '/categories/': Categories(),
#     '/suggestions/': Suggestions(),
#     '/create-product/': CreateProduct(),
#     '/create-category/': CreateCategory(),
#     '/copy-product/': CopyProduct()
# }
