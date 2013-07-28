from decimal import Decimal
from django.db import models
from django.db.models import F
from django.contrib.auth.models import User

TWO_DECIMAL_PLACES = Decimal('1.00')

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.IntegerField()
    image_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    
    def in_stock(self):
        return self.quantity > 0
    
    # use F object to change quantity atomically. Returns true if ok, false if negative quantity
    def change_quantity(self, count):
        if self.quantity + count < 0:
            return False
        else:
            self.quantity = F('quantity') + count
            self.save()
            return True
    
    def __unicode__(self):
        return self.name

class ShoppingCart(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    count = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return '{}, {} {}'.format(self.user.get_full_name(), self.count, self.product.name)
        
class Order(models.Model):
    user = models.ForeignKey(User)
    date_ordered = models.DateTimeField(auto_now_add=True)
    
    def get_orders(self):
        return self.orderproduct_set.all()
        
    def get_price(self):
        return sum([p.count * p.product.price for p in self.get_orders()]).quantize(TWO_DECIMAL_PLACES)
    
    def __unicode__(self):
        return '{} order at {}'.format(self.user.get_full_name(), self.date_ordered)
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    count = models.IntegerField()