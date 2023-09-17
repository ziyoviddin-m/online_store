from django.db import models
from users.models import User


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUS = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    address = models.CharField(max_length=256)
    postcode = models.CharField(max_length=10)
    email = models.EmailField(max_length=256)
    basket_history = models.JSONField(default=dict)
    status = models.SmallIntegerField(default=CREATED, choices=STATUS)
    created = models.DateTimeField(auto_now_add=True)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order #{self.id} {self.first_name} {self.last_name}'