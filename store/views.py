from django.shortcuts import render
from .models import Product, Order, OrderItem, ShippingAddress

from django.http import JsonResponse
from .utils import cartData, guestOrder
import json
import datetime


def store(request):
    products = Product.objects.all()

    data = cartData(request)

    context = {'products': products, 'items_count': data['items_count']}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
        
    context = {'items': data['items'], 'order': data['order'], 'items_count': data['items_count']}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)

    items = data['items']
    order = data['order']

    context = {'items': items, 'order': order, 'items_count': data['items_count']}
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
        
    else:
        customer, order = guestOrder(request, data)

    if order.get_total == total:
            order.complete = True

    if order.shipping:
        shipping = ShippingAddress.objects.create(
            customer= customer,
            order= order,
            address= data['shipping_data']['address'],
            city= data['shipping_data']['city'],
            state= data['shipping_data']['state'],
            zipcode= data['shipping_data']['zipcode'],

        )
    order.transition = transition
    order.save()

    return JsonResponse('Ordered successfully', safe=False)


def order_history(request):

    if request.user.is_authenticated:
        orders = Order.objects.filter(customer=request.user.customer)
    else:
        orders = []

    data = cartData(request)
    context = {'orders': orders, 'items_count': data['items_count']}
    return render(request, 'store/order_history.html', context)


def order_detail(request, pk):

    order = Order.objects.get(id=pk)
    items = order.orderitem_set.all()
    json_items = []

    for item in items:
        order_item = {
            'name': item.product.name,
            'quantity': item.quantity,
            'price': item.product.price
        }
        json_items.append(order_item)

    return JsonResponse({'items': json_items}, safe=False)


def product_detail(request, pk):

    product = Product.objects.get(id=pk)
    data = cartData(request)

    context = {'product': product, 'items_count': data['items_count']}
    return render(request, 'store/product_detail.html', context)