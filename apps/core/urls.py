from django.urls import path
from .views import frontpage, contact


urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('contact/', contact, name='contact'),
]
