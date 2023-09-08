from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transition = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        order_items = self.orderitem_set.all()
        for item in order_items:
            if item.product.digital == False:
                shipping = True
                break
        return shipping
    
    @property
    def items_count(self):
        items = self.orderitem_set.all()
        count = sum([item.quantity for item in items])
        return count
    
    @property
    def get_total(self):
        items = self.orderitem_set.all()
        total = sum([item.get_total for item in items])
        return total
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product.name
    
    @property
    def get_total(self):
        return self.product.price * self.quantity
