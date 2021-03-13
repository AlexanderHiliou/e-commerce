from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from apps.product.models import Product
from .forms import ContactForm


def frontpage(request):
    latest_products = Product.objects.all()
    paginator = Paginator(latest_products, 8)
    page = request.GET.get('page')
    latest_products = paginator.get_page(page)
    return render(request, 'core/frontpage.html', {'latest_products': latest_products})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('frontpage')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})
