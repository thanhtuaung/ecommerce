from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update-item/', views.update_item, name='update_item'),
    path('orders/create/', views.create_order, name='create_order')
]