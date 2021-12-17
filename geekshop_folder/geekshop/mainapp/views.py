from django.shortcuts import render
from .models import ProductCategory, Product

# Create your views here.
menu_links = [
    {'view_name': 'index', 'name': 'главная'},
    {'view_name': 'products', 'name': 'продукты'},
    {'view_name': 'contact', 'name': 'контакты'},
]

def main(request):
    title = 'главная'

    products = Product.objects.all()[:4]

    return render(request, 'mainapp/index.html', context = {
        "menu_links": menu_links,
        "product_count": "9000",
        "shop_slogan": "лучшее для вас!",
        'title': title,
        'products': products,
    })

def products(request):
    return render(request, 'mainapp/products.html', context={"menu_links": menu_links})

def contact(request):
    return render(request, 'mainapp/contact.html', context={"menu_links": menu_links})