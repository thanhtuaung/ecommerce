import json
from .models import *

def cookieCart(request):
    items = []
    order = {'items_count': 0, 'get_total': 0, 'shipping': False}
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

    for item in items:
        if item['product'].digital == False:
            order['shipping'] = True

    return {'items': items, 'order': order, 'items_count': items_count}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        print(customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        items_count = order.items_count
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        items_count = cookieData['items_count']
        order = cookieData['order']
    return {'items': items, 'order': order, 'items_count': items_count}


def guestOrder(request, data):

    name = data['user_data']['name']
    email = data['user_data']['email']

    customer = Customer.objects.create(email=email)
    customer.name = name
    customer.save()

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cookieData = cookieCart(request)
    items = cookieData['items']

    for item in items:
        product = item['product']
        orderItem = OrderItem.objects.create(
            order = order,
            product = product,
            quantity = item['quantity']
        )
    
    return customer, order


    