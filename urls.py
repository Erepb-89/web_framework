from datetime import date
from views import Index, Contacts, Products, ProductsList, \
    Suggestions, Categories, CreateProduct, CopyProduct, \
    CreateCategory


# front controller
def date_front(request):
    request['today'] = date.today()


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
    '/products-list/': ProductsList(),
    '/categories/': Categories(),
    '/suggestions/': Suggestions(),
    '/create-product/': CreateProduct(),
    '/create-category/': CreateCategory(),
    '/copy-product/': CopyProduct()
}
