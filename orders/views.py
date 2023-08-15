from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from django.db import transaction

from .serializers import OrderSerializer
from cart.cart import Cart
from social.models import Address, Product, OrderItems, Order
from .tasks import order_confirmation_mail

import random
# Create your views here.

@api_view(['POST'])
@login_required
def order_create(request):
    cart=Cart(request)
    user=request.user
    order_id=str(random.randrange(1000))
    
    address=Address.objects.filter(user=user)[0]
    data={"order_id":order_id, "address":address.id, "buyer":user.id, "price":1}
    order_srz=OrderSerializer(data=data)
    with transaction.atomic():
        order_srz.is_valid(raise_exception=True)
        order=order_srz.save()
        for item in cart:
            OrderItems.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
        order.price=order.get_total_cost()
        order.save()
        order_confirmation_mail.delay(order.id)
        cart.clear()
    return render(request, 'orders/order_placed.html', {'order': order})


@login_required
def checkout_page(request):
    cart=Cart(request)
    addresses=Address.objects.filter(user=request.user)
    return render(request,'orders/checkout_page.html',{'cart': cart, 'addresses': addresses})
        
    