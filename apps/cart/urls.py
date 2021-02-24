from django.urls import path
from .views import cart_detail, success

urlpatterns = [
    path('', cart_detail, name='cart'),
    path('success', success, name='success'),
]
