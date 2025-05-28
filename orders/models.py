from django.utils import timezone
from django.db import models
from django.db.models import Sum, F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from LabStartApp.models import User, Product


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'В ожидании'
        PROCESSED = 'processed', 'Обработан'
        SHIPPED = 'shipped', 'Отправлен'
        DELIVERED = 'delivered', 'Доставлен'
        CANCELLED = 'cancelled', 'Отменён'

    order_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    order_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address = models.CharField(max_length=512, default=None)
    city = models.CharField(max_length=128, default=None)
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

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    class Meta:
        db_table = 'orders'
        ordering = ['-order_date']

class OrderItem(models.Model):
    order_item_id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Order, models.DO_NOTHING, related_name='order_items', blank=True, null=True)
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Товар № {self.order_item_id}'

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        db_table = 'order_items'

@receiver(post_save, sender=OrderItem)
def update_order_price_on_save(sender, instance, **kwargs):
    instance.order.update_price()

@receiver(post_delete, sender=OrderItem)
def update_order_price_on_delete(sender, instance, **kwargs):
    instance.order.update_price()