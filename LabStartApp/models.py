from django.db import models
from django.db.models import Sum, F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=100)
    phone_number = models.CharField(unique=True, max_length=20)
    password = models.TextField()
    address = models.TextField(blank=True, null=True)
    registration_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        managed = False
        db_table = 'users'


class Order(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    order_date = models.DateField()
    status = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Заказ № {self.order_id}'

    def update_price(self):
        total = self.order_items.aggregate(
            total_price=Sum(F('price') * F('quantity'))
        )['total_price'] or 0
        self.price = total
        self.save()

    class Meta:
        managed = False
        db_table = 'orders'

class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Товар {self.name}'

    class Meta:
        managed = False
        db_table = 'products'

class OrderItem(models.Model):
    order_item_id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey('Order', models.DO_NOTHING, related_name='order_items', blank=True, null=True)
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Товар № {self.order_item_id}'

    class Meta:
        managed = False
        db_table = 'order_items'

@receiver(post_save, sender=OrderItem)
def update_order_price_on_save(sender, instance, **kwargs):
    instance.order.update_price()

@receiver(post_delete, sender=OrderItem)
def update_order_price_on_delete(sender, instance, **kwargs):
    instance.order.update_price()