from django.contrib import admin
from LabStartApp.models import User, Product
from orders.models import OrderItem

admin.site.register(User)
admin.site.register(OrderItem)
admin.site.register(Product)