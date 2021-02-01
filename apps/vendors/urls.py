from django.urls import path
from .views import become_vendor

urlpatterns = [
    path('become-vendor/', become_vendor, name='become_vendor'),
]
