from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
from django.shortcuts import render, redirect
from django.utils.text import slugify

from .models import Vendor
from .forms import ProductForm
from apps.product.models import Product, Category



def become_vendor(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request , user)

            vendor = Vendor.objects.create(name=user.username, created_by=user)

            return redirect('frontpage')

    else:
        form = UserCreationForm()
    return render(request, 'vendors/become_vendor.html', {'form': form})


@login_required
def vendor_admin(request):
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orders.all()

    remove_product = request.GET.get('remove_product', '')
    if remove_product:
        product = Product.objects.get(id=remove_product)
        product.delete()
        return redirect('vendor_admin')

    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.vendor_fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.vendor_fully_paid = False


    return render(request, 'vendors/vendor_admin.html', {'vendor': vendor, 'products': products, 'orders': orders })

@login_required
def edit_vendor(request):
    vendor = request.user.vendor
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        if name:
            vendor.name = name
            vendor.save()
            vendor.created_by.email = email
            vendor.created_by.save()

            return redirect('vendor_admin')
    return render(request, 'vendors/edit_vendor.html', {'vendor': vendor})


@login_required
def add_product(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save()

            return redirect('vendor_admin')
    else:
        form = ProductForm()

    return render(request, 'vendors/add_product.html', {'form': form, 'categories': categories})