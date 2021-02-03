from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import become_vendor, vendor_admin, add_product

urlpatterns = [
    path('become-vendor/', become_vendor, name='become_vendor'),
    path('vendor-admin/', vendor_admin, name='vendor_admin'),
    path('add_product/', add_product, name='add_product'),


    path('login/', LoginView.as_view(template_name='vendors/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
