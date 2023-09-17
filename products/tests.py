from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from products.models import Product, ProductCategory


class IndexViewTestCase(TestCase):

    def test_view(self):
        url = reverse('home')
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - ZIYOVIDDIN')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductListViewTestCase(TestCase):
    fixtures = ['categories.json', 'genders.json', 'goods.json']

    def setUp(self):
        self.products = Product.objects.all().order_by('category')

    def test_list(self):
        url = reverse('products:products')
        response = self.client.get(url)
        
        self._common_test(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:6]))

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        url = reverse('products:category', kwargs={'category_id': category.pk})
        response = self.client.get(url)

        self._common_test(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.pk))
        )

    def test_searching(self):
        url = reverse('products:search_products')
        search = 'Рубашка'
        response = self.client.get(url, {'search': search})
        

        self._common_test(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(name__icontains=search))
        )

    def _common_test(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'ZIYOVIDDIN - Продукты')
        self.assertTemplateUsed(response, 'products/shop.html')