from celery import shared_task

import stripe

from django.conf import settings

from apps.order.utilities import notify_customer, notify_vendor
from apps.order.models import Order

@shared_task
def stripe_charge(total_amount, token):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    charge = stripe.Charge.create(
        amount=total_amount,
        currency='EUR',
        description='Charge for Iteriorshop',
        source=token
    )

@shared_task
def notify_vendor_and_customer(id):
    order = Order.objects.get(pk=id)
    notify_customer(order)
    notify_vendor(order)