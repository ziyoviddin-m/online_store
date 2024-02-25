from django.db import models
from django.urls import reverse
from django.utils import timezone

# from django.contrib.auth.models import User
from users.models import User


class Gender(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Gender'
        verbose_name_plural = 'Genders'


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField('Название',max_length=256, unique=True)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена',max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество',default=0)
    image = models.ImageField('Фото товара',upload_to='products_image')
    category_gender = models.ForeignKey(Gender, on_delete=models.PROTECT, verbose_name='Пол')
    category = models.ForeignKey(ProductCategory,on_delete=models.PROTECT, verbose_name='Категория')

    
    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category_gender.title} / {self.category.name}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'



class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)
    
    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()
    
    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'
    
    def sum(self):
        return self.product.price * self.quantity
    
    def de_json(self):
        basket_item = {
            'products_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum())
        }
        return basket_item
    


class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Favorite Product'
        verbose_name_plural = 'Favorite Products'




