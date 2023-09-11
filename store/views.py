from django.shortcuts import render
from .models import Product, Order, OrderItem, ShippingAddress

from django.http import JsonResponse
import json
import datetime

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

        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}

        for id in cart:
            quantity = cart[id]['quantity']
            order['items_count'] += quantity
            items_count += quantity

            product = Product.objects.get(id=id)
            order['get_total'] += (product.price * quantity)

            item = {
                'product': product,
                'quantity': quantity,
                'get_total': product.price * quantity
            }

            items.append(item)
        
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


def create_order(request):
    transition = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    total = float(data['user_data']['total'])

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order.transition = transition

        if order.shipping:
            shipping = ShippingAddress.objects.create(
                customer= customer,
                order= order,
                address= data['shipping_data']['address'],
                city= data['shipping_data']['city'],
                state= data['shipping_data']['state'],
                zipcode= data['shipping_data']['zipcode'],

            )

            shipping.save()
        
        if order.get_total == total:
            order.complete = True
        order.save()

    return JsonResponse('Ordered successfully', safe=False)