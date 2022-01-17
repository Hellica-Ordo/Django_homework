from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product
from basketapp.models import Basket

# Create your views here.
menu_links = [
    {"href": "index", "active_if": ["index"], "name": "Главная"},
    {
        "href": "products:index",
        "active_if": ["products:index", "products:category"],
        "name": "Продукты",
    },
    {"href": "contact", "active_if": ["contact"], "name": "Контакты"},
]


def main(request):
    title = 'Главная'
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    products = Product.objects.all()[:4]

    return render(request, 'mainapp/index.html', context={
        'menu_links': menu_links,
        "product_count": "9000",
        "shop_slogan": "лучшее для вас!",
        'title': title,
        'products': products,
        'basket': basket})


def products(request, pk=None):
    print(pk)

    title = 'Продукты'
    products_menu = ProductCategory.objects.all()
    related_products = Product.objects.all()[:2] if not pk else Product.objects.filter(
        category__id=pk)

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

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
                                                                      'basket': basket})

    else:
        same_products = Product.objects.all()[:3]

        return render(request, 'mainapp/products.html', context={'title': title,
                                                                 'menu_links': menu_links,
                                                                 'products_menu': products_menu,
                                                                 'same_products': same_products,
                                                                 'basket': basket})


def contact(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    return render(request, 'mainapp/contact.html', context={"menu_links": menu_links,
                                                            'basket': basket})
