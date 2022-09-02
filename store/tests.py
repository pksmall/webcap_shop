import json
from django.urls import path, include, reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, URLPatternsTestCase

from users.models import User
from .models import Product, Order, Bill


class TestProductsModel(APITestCase, URLPatternsTestCase):
  urlpatterns = [
    path('user/auth/', include('users.urls')),
    path('store/', include('store.urls'))
  ]
  login_data = {'email': 'a@a.com', 'password': 'test'}

  def login_process(self):
    url = reverse('login')
    response = self.client.post(url, self.login_data)
    login_response_data = json.loads(response.content)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTrue('access' in login_response_data)
    token = login_response_data['access']
    return token

  def setUp(self):
    user = User.objects.create_user(
      email=self.login_data['email'],
      password=self.login_data['password'],
      role=User.ADMIN
    )
    self.data1 = Product.products.create(title='django beginners', who_created=user,
                                         regular_price='20.00', slug='django-beginners')
    self.data2 = Product.products.create(title='django advanced', who_created=user,
                                         regular_price='20.00', is_active=False,
                                         slug='django-advanced')

  def test_products_model_entry(self):
    """
    Test product model data insertion/types/field attributes
    """
    data = self.data1
    self.assertTrue(isinstance(data, Product))
    self.assertEqual(str(data), 'django beginners')

  def test_products_custom_manager_basic(self):
    """
    Test product model custom manager returns only active products
    """
    data = Product.products.all()
    self.assertEqual(data.count(), 1)

  def test_products_create_url(self):
    """
    Test product url create
    """
    token = self.login_process()

    # Test the endpoint
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
    data = {'title': 'test product', 'regular_price': '1.01'}
    response = client.post(reverse('product_create'), data)
    response_data = json.loads(response.content)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual('test product', response_data['product']['title'])

  def test_products_get_by_id_url(self):
    """
    Test product url get_by_id
    """
    token = self.login_process()

    # Get correct url
    data = self.data1
    url = reverse('product_get_by_id', args=[data.id])
    self.assertEqual(url, '/store/product/get/{}'.format(data.id))

    # Test the endpoint
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
    response = client.get(url)
    response_data = json.loads(response.content)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual('django beginners', response_data['product']['title'])

  def test_products_list_url(self):
    """
    Test product url list
    """
    token = self.login_process()

    # Test the endpoint
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
    response = client.get(reverse('product_list'))
    response_data = json.loads(response.content)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(Product.products.get_all().count(), len(response_data['products']))


class TestOrderModel(APITestCase, URLPatternsTestCase):
  urlpatterns = [
    path('user/auth/', include('users.urls')),
    path('store/', include('store.urls'))
  ]
  login_data = {'email': 'a@a.com', 'password': 'test'}

  def login_process(self):
    url = reverse('login')
    response = self.client.post(url, self.login_data)
    login_response_data = json.loads(response.content)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTrue('access' in login_response_data)
    token = login_response_data['access']
    return token

  def setUp(self):
    user = User.objects.create_user(
      email=self.login_data['email'],
      password=self.login_data['password'],
      role=User.ADMIN
    )
    self.product = Product.products.create(title='django beginners', who_created=user,
                                          regular_price='20.00', slug='django-beginners')
    self.order, self.bill = Order.orders.create_new(product=self.product, user=user)

  def test_order_model_entry(self):
    """
    Test order model data insertion/types/field attributes
    """
    self.assertTrue(isinstance(self.order, Order))
    self.assertTrue(isinstance(self.bill, Bill))
    self.assertEqual(self.order.status, Order.CREATED)

  def test_order_create_url(self):
    """
    Test order url create
    """
    token = self.login_process()

    # Test the endpoint
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
    data = {'product_id': self.product.id}
    response = client.post(reverse('order_create'), data)
    response_data = json.loads(response.content)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual('Order and Bill successfully created!', response_data['message'])

  def test_order_get_by_id_url(self):
    """
    Test order url get_by_id
    """
    token = self.login_process()

    # Get correct url
    url = reverse('order_get_by_id', args=[self.order.id])
    self.assertEqual(url, '/store/order/get/{}'.format(self.order.id))

    # Test the endpoint
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
    response = client.get(url)
    response_data = json.loads(response.content)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual('Successfully fetched order', response_data['message'])

  def test_order_list_url(self):
    """
    Test order url list
    """
    token = self.login_process()

    # Test the endpoint
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
    response = client.get(reverse('order_list'))
    response_data = json.loads(response.content)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(Order.orders.count(), len(response_data['orders']))
