from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product
from basketapp.models import Basket
from random import sample

#ссылки для главного меню сайта
menu_links = [
    {"href": "index", "active_if": ["index"], "name": "Главная"},
    {
        "href": "products:index",
        "active_if": ["products:index", "products:category"],
        "name": "Продукты",
    },
    {"href": "contact", "active_if": ["contact"], "name": "Контакты"},
]

#функция для вывода корзины, чтобы не писать в каждом контроллере одно и то же
def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []

#вывод "горящего предложения" (с) перевод алиэкспресса
def get_hot_product():
    products = Product.objects.all()

    return sample(list(products), 1)[0]

#вывод похожих продуктов для горячего предложения
def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category). \
                        exclude(pk=hot_product.pk)[:3]

    return same_products


#контроллер главной страницы
def main(request):
    title = 'Главная'
    basket = get_basket(request.user)

    products = Product.objects.all()[:4]

    return render(request, 'mainapp/index.html', context={
        'menu_links': menu_links,
        "product_count": "9000",
        "shop_slogan": "лучшее для вас!",
        'title': title,
        'products': products,
        'basket': basket})


#контроллер каталога продуктов
def products(request, pk=None):
    print(pk)

    title = 'Продукты'
    products_menu = ProductCategory.objects.all()
    related_products = Product.objects.all()[:2] if not pk else Product.objects.filter(category__id=pk)
    basket = get_basket(request.user)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'Все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        return render(request, 'mainapp/products_list.html', context={'title': title,
                                                                      'menu_links': menu_links,
                                                                      'products_menu': products_menu,
                                                                      'category': category,
                                                                      'products': products,
                                                                      'related_products': related_products,
                                                                      'same_products': same_products,
                                                                      'basket': basket})

    else:
        same_products = Product.objects.all()[:3]

        return render(request, 'mainapp/products.html', context={'title': title,
                                                                 'menu_links': menu_links,
                                                                 'products_menu': products_menu,
                                                                 'same_products': same_products,
                                                                 'basket': basket,
                                                                 'hot_product': hot_product})


#контроллер страницы конкретного товара
def product(request, pk):
    title = 'продукты'

    content = {
        'title': title,
        'products_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
        "menu_links": menu_links,
    }

    return render(request, 'mainapp/product.html', content)


#контроллер страницы контактов
def contact(request):
    basket = get_basket(request.user)

    return render(request, 'mainapp/contact.html', context={"menu_links": menu_links,
                                                            'basket': basket})
