from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=200,unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    customer_name = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    product_name = models.CharField(max_length=200)
    product_img = models.ImageField(upload_to='product_img')
    product_price = models.PositiveIntegerField()
    delivery_boy = models.ForeignKey(User,on_delete=models.CASCADE)
    delivered_img = models.ImageField(upload_to='delivered_img',default='delivered.jpg')
    invoice_img = models.ImageField(upload_to='invoice_img',default='invoicep.jpg')
    status = models.CharField(max_length=200,default='Order Confirm')
    def __str__(self) -> str:
        return self.customer_name.name