from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update-item/', views.update_item, name='update_item'),

    # order
    path('orders/create/', views.create_order, name='create_order'),
    path('customer/orders/', views.order_history, name='customer_orders'),
    path('customer/orders/<str:pk>/', views.order_detail, name='order_detail'),

    #product
    path('products/<str:pk>/', views.product_detail, name='product_detail')
]