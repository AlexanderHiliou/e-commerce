from apps.cart.cart import Cart

from .models import Order, OrderItem


def checkout(request, first_name, last_name, email, adress, zipcode, place, phone, amount):
    
    order = Order.objects.create(frist_name=first_name, last_name=last_name, email=email, adress=adress, zip_code=zipcode, place=place, phone=phone, paid_amount=amount)

    for item in Cart(request):
        OrderItem.objects.create(order=order, product=item['product'], vendor=item['product'].vendor, price=item['product'].price, quantity=item['quantity'])

        order.vendors.add(item['product'].vendor)
        
    return order