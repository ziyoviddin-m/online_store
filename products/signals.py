from django.core.files.storage import default_storage
from django.db.models.signals import pre_save
from django.dispatch import receiver

from products.models import Product

'''
Этот скрипт нужен: когда супер пользователь меняет фото товара на новый, 
тогда старое фото автоматически заменяется новым, то есть старое фото удаляется 
'''

@receiver(pre_save, sender=Product)
def delete_old_photo(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Product.objects.get(pk=instance.pk)
            if old_instance.image != instance.image:
                # Удаление старой фотографии
                if old_instance.image:
                    default_storage.delete(old_instance.image.path)
        except Product.DoesNotExist:
            pass
