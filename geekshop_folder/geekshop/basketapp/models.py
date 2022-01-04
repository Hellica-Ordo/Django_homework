from django.db import models
from django.conf import settings
from mainapp.models import Product

# related_name позволяет обращаться ко всем записям в бд в коризне для пользователя через user.basket
class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='дата добавления', auto_now_add=True)

    # оно вроде как работает, но общую стоимость считает неправильно
    # количество товаров в корзине
    @property
    def item_count(self):
        items_in_basket = Basket.objects.filter(user=self.user)
        all_items_count = sum(list(map(lambda n: n.quantity, items_in_basket)))
        return all_items_count

    # стоимость товаров одного типа
    @property
    def product_cost(self):
        return self.product.quantity * self.product.price

    # стоимость всех товаров в корзине
    @property
    def all_products_cost(self):
        items_in_basket = Basket.objects.filter(user=self.user)
        basket_cost = sum(list(map(lambda n: n.product_cost, items_in_basket)))
        return basket_cost