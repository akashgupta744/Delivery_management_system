from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['name','email','password','address']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['product_name','product_img','product_price','delivery_boy','delivered_img','invoice_img']