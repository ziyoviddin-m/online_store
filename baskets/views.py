from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render

from products.models import *


@login_required
def basket(request):
    categories = ProductCategory.objects.all()
    
    context = {
        'categories': categories,
        'title': 'ZIYOVIDDIN - Корзина'
    }
    return render(request, 'baskets/basket.html', context)

@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, product_id):
    basket = Basket.objects.get(id=product_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_all_delete(request):
    baskets = Basket.objects.filter(user=request.user)
    baskets.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])