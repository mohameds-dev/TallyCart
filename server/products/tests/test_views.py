from django.test import TestCase
from products.models import Product, Tag
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

class TestProductRetrievalViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('products')

    def test_get_all_products_returns_200_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_products_returns_an_empty_list_of_products(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 0)

    def test_create_a_product_and_list_view_returns_a_list_with_that_product(self):
        Product.objects.create(name="Test Product")
        response = self.client.get(self.url)
        
        self.assertEqual(response.data[0]['name'], "Test Product")

    def test_create_a_product_and_retrieve_view_returns_the_product(self):
        product = Product.objects.create(name="Test Product")
        response = self.client.get(reverse('product', args=[product.id]))

        self.assertEqual(response.data['name'], "Test Product")

    def test_retrieve_view_returns_not_found_if_product_does_not_exist(self):
        response = self.client.get(reverse('product', args=[999]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_a_product_with_tags_and_list_view_returns_the_product_with_tags(self):
        product = Product.objects.create(name="Test Product")
        product.tags.add(Tag.objects.create(name="TestTag"))
        response = self.client.get(self.url)
        
        self.assertEqual(response.data[0]['tags'][0], {'id': 1, 'name': 'TestTag'})

class TestProductSearchViews(TestCase):
    def setUp(self):    
        self.client = APIClient()
        self.url = reverse('products')

    def test_create_a_product_with_tags_and_search_by_name_returns_result_with_one_product(self):
        Product.objects.create(name="Test Product")
        response = self.client.get(self.url, {'search': 'Test Product'})

        self.assertEqual(len(response.data), 1)

    def test_create_a_product_with_tags_and_search_by_incorrect_name_returns_empty_result(self):
        Product.objects.create(name="Test Product")
        response = self.client.get(self.url, {'search': 'Incorrect Name'})

        self.assertEqual(len(response.data), 0)

    def test_create_a_product_with_tags_and_search_by_tag_returns_result_with_one_product(self):
        product = Product.objects.create(name="Test Product")
        product.tags.add(Tag.objects.create(name="TestTag"))
        response = self.client.get(self.url, {'search': 'TestTag'})

        self.assertEqual(len(response.data), 1)

    def test_create_two_products_with_tags_and_search_by_name_returns_correct_products(self):
        product1 = Product.objects.create(name="Test Product 1")
        product2 = Product.objects.create(name="Test Product 2")
        tag = Tag.objects.create(name="TestTag")
        product1.tags.add(tag)
        product2.tags.add(tag)
        response = self.client.get(self.url, {'search': 'TestTag'})

        self.assertEqual(len(response.data), 2)

    def test_create_two_products_with_tags_and_search_by_incorrect_tag_returns_empty_result(self):
        product1 = Product.objects.create(name="Test Product 1")
        product2 = Product.objects.create(name="Test Product 2")
        product1.tags.add(Tag.objects.create(name="TestTag1"))
        product2.tags.add(Tag.objects.create(name="TestTag2"))
        response = self.client.get(self.url, {'search': 'Incorrect Tag'})

        self.assertEqual(len(response.data), 0)

    def test_create_two_products_with_tags_and_search_by_tag_returns_correct_products(self):
        product1 = Product.objects.create(name="Test Product 1")
        product1.tags.add(Tag.objects.create(name="TestTag1"))
        product2 = Product.objects.create(name="Test Product 2")
        product2.tags.add(Tag.objects.create(name="TestTag2"))
        response = self.client.get(self.url, {'search': 'TestTag1'})

        self.assertEqual(len(response.data), 1)

