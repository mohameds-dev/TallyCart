from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from shops.models import Shop

class TestShopRetrievalViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('shops')

    def test_get_all_shops_returns_200_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_shops_returns_an_empty_list_of_shops(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 0)

    def test_create_a_shop_and_list_view_returns_a_list_with_that_shop(self):
        Shop.objects.create(name="Test Shop")
        response = self.client.get(self.url)

        self.assertEqual(response.data[0]['name'], "Test Shop")

    def test_create_a_shop_and_retrieve_view_returns_the_shop(self):
        shop = Shop.objects.create(name="Test Shop")
        response = self.client.get(reverse('shop', args=[shop.id]))

        self.assertEqual(response.data['name'], "Test Shop")

    def test_retrieve_view_returns_not_found_if_shop_does_not_exist(self):
        response = self.client.get(reverse('shop', args=[999]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class TestShopSearchViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('shops')

    def test_search_by_name_returns_correct_shops(self):
        Shop.objects.create(name="Test Shop")
        Shop.objects.create(name="Another Shop")
        response = self.client.get(self.url, {'search': 'Test'})
        
        self.assertEqual(response.data[0]['name'], "Test Shop")

    def test_search_by_incorrect_name_returns_empty_list(self):
        Shop.objects.create(name="Test Shop")
        response = self.client.get(self.url, {'search': 'Incorrect Name'})

        self.assertEqual(len(response.data), 0)

    def test_search_by_address_returns_correct_shops(self):
        Shop.objects.create(name="Test Shop", address="123 Main St")
        Shop.objects.create(name="Another Shop", address="456 Main St")
        response = self.client.get(self.url, {'search': 'Main St'})

        self.assertEqual(len(response.data), 2)
        
    def test_search_by_incorrect_address_returns_empty_list(self):
        Shop.objects.create(name="Test Shop", address="123 Main St")
        response = self.client.get(self.url, {'search': 'Incorrect Address'})

        self.assertEqual(len(response.data), 0)
