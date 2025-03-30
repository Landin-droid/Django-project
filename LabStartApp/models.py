from django.db import models


class Order(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    products = models.TextField()
    creation_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return '%s %s %s' % (self.order_id, self.products, self.status)

    class Meta:
        managed = False
        db_table = 'orders'


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
