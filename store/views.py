from django.shortcuts import render
from .models import Product, Order, OrderItem

from django.http import JsonResponse
import json

def store(request):
    products = Product.objects.all()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items_count = order.items_count
    else:
        items_count = 0

    context = {'products': products, 'items_count': items_count}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        items_count = order.items_count
    else:
        items = []
        order = {'items_count': 0, 'get_total': 0}
        items_count = 0
        
    context = {'items': items, 'order': order, 'items_count': items_count}
    return render(request, 'store/cart.html', context)

def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        items_count = order.items_count
        # shipping = order.shipping
    else:
        items = []
        order = {'items_count': 0, 'get_total': 0}
        items_count = 0
        # shipping = False

    context = {'items': items, 'order': order, 'items_count': items_count,}  
    return render(request, 'store/checkout.html', context)

def update_item(request):

    data = json.loads(request.body)

    product_id = data.get('product')
    action = data.get('action')

    product = Product.objects.get(id=product_id)
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)