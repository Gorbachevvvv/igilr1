from .models import Seller, Customer


def is_seller(request):
    if request.user.is_authenticated:
        is_seller = Seller.objects.filter(user=request.user).exists()
    else:
        is_seller = False
    return {'is_seller': is_seller}

def is_customer(request):
    if request.user.is_authenticated:
        is_customer = Customer.objects.filter(user=request.user).exists()
    else:
        is_customer = False
    return {'is_customer': is_customer}

def is_admin(request):
    if request.user.is_authenticated:
        is_admin=request.user.is_superuser
    else:
        is_admin = False
    return {'is_admin': is_admin}