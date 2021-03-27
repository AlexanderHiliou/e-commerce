import stripe

from django.conf import settings

from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import CheckoutForm
from apps.order.utilities import checkout
from .cart import Cart
from .tasks import stripe_charge, notify_vendor_and_customer



def cart_detail(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            stripe_token = form.cleaned_data['stripe_token']

            try:
                stripe_charge.delay(int(cart.get_total_cost() * 100), stripe_token)

                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                address = form.cleaned_data['address']
                zipcode = form.cleaned_data['zipcode']
                place = form.cleaned_data['place']

                order = checkout(request, first_name, last_name, email, address, zipcode, place, phone, cart.get_total_cost())

                cart.clear()

                notify_vendor_and_customer.delay(order.id)

            except Exception:
                messages.error(request, 'There was something wrong with payment')

                return redirect('success')
    else:
        form = CheckoutForm()


    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', '')

    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('cart')

    if change_quantity:
        cart.add(change_quantity, quantity, True)
        return redirect('cart')

    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('cart')
    return render(request, 'cart/cart.html', {'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY})


def success(request):
    return render(request, 'cart/success.html')
