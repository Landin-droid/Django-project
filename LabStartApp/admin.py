from django.contrib import admin
from LabStartApp.models import User, Order, OrderItem, Product

admin.site.register(User)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)