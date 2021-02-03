from django.shortcuts import render
from apps.product.models import Product


def frontpage(request):
    latest_products = Product.objects.all()[:8]
    return render(request, 'core/frontpage.html', {'latest_products': latest_products})


def contact(request):
    return render(request, 'core/contact.html')
