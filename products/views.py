import random

from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.shortcuts import HttpResponseRedirect, render
from django.views.generic import DetailView, ListView, TemplateView
from django.core.cache import cache

from common.mixin import TitleMixin

from .models import *


class IndexView(TitleMixin, ListView):
    model = Product
    template_name = 'products/index.html'
    context_object_name = 'products'
    title = 'Store - ZIYOVIDDIN'

    def get_queryset(self):
        return Product.objects.order_by('-name')[:8]

    def get_context_data(self, *, object_list=None,**kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        return context


class ProductDetailView(TitleMixin, DetailView):
    model = Product
    template_name = 'products/detail.html'
    pk_url_kwarg = 'product_id'
    title = 'ZIYOVIDDIN - Продукт'

    def get_context_data(self, *, object_list=None,**kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = cache.get('product')
        if not product:
            context['product'] = Product.objects.get(id=self.object.id)
            cache.set('product', context['product'], 360)
        else:
            context['product'] = product

        context['products'] = Product.objects.order_by('-id')[random.randint(1, 5) :random.randint(5, 10)]
        return context


class ProductListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/shop.html'
    context_object_name = 'products'
    paginate_by = 6
    ordering = 'category'
    title = 'ZIYOVIDDIN - Продукты'

    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        search = self.request.GET.get('search')

        if search:
            queryset = queryset.filter(name__icontains=search)
        elif category_id:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['count'] = self.model.objects.count()
        return context
    

@login_required
def favorite(request):
    favorites = FavoriteProduct.objects.filter(user=request.user)

    context = {
        'favorites': favorites,
        'title': 'ZIYOVIDDIN - Избранный'

    }
    return render(request, 'products/favorites.html', context)

@login_required
def favorite_add(request, pk):
    product = Product.objects.get(id=pk)
    favorites = FavoriteProduct.objects.filter(user=request.user, product=product)

    if not favorites.exists():
        FavoriteProduct.objects.create(user=request.user, product=product)
    else:
        favorites.first()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def favorite_delete(request, pk):
    favorite = FavoriteProduct.objects.get(id=pk)
    favorite.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def favorite_del_all(request):
    favorites = FavoriteProduct.objects.filter(user=request.user)
    favorites.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ContactView(TitleMixin, TemplateView):
    template_name = 'products/contact.html'


# def products(request, category_id=None, page_number=1):
#     categories = ProductCategory.objects.all()
#     count = Product.objects.count()

#     search = request.GET.get('search')
#     if search:
#         products = Product.objects.filter(name__icontains=search)
#     else:
#         products = Product.objects.filter(category_id=category_id, ) if category_id else Product.objects.all()

#     products = products.order_by('category')

#     per_page = 6
#     paginator = Paginator(products, per_page)
#     products_paginator = paginator.page(page_number)

#     baskets = []
#     if request.user.is_authenticated:
#         baskets = Basket.objects.filter(user=request.user)

#     context = {
#         'products': products_paginator,
#         'categories': categories,
#         'count': count,
#         'baskets': baskets,
#         'title': ' ZIYOVIDDIN - Продукты'
#     }
#     return render(request, 'products/shop.html', context)