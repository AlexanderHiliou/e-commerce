from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
from django.shortcuts import render, redirect
from .models import Vendor


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
    return render(request, 'vendors/vendor_admin.html', {'vendor': vendor})