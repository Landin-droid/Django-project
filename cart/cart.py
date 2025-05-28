from decimal import Decimal
from django.conf import settings
from LabStartApp.models import Product


class Cart(object):

    def __init__(self, request):
        self.session = request.session  # сохранение текущей сессии в переменную
        cart = self.session.get(settings.CART_SESSION_ID)  # проверка - есть ли уже корзина
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}  # если нет - инициализация пустой корзины
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):  # добавление товара
        product_id = str(product.product_id)  # ключ для словаря, который будет сохранять товарную позицию
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}  # по ключу определяем цену и кол-во
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.product_id)
        if product_id in self.cart:
            del self.cart[product_id]  # поиск продукта по его ID
            self.save()

    def __iter__(self):  # итератор для отображения полного наименования товара
        product_ids = self.cart.keys()
        products = Product.objects.filter(
            product_id__in=product_ids) # запрос к БД для получения queryset со всеми продуктами в корзине

        cart = self.cart.copy()
        for product in products:
            cart[str(product.product_id)]['product'] = product  # создание словаря со списком продуктов

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']  # расчет общей стоимости одной товарной позиции
            yield item

    def __len__(self):  # кол-во товаров в корзине
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):  # общая стоимость всех товаров в корзине
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):  # сброс сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
        self.save()