from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _

from users.models import User
from .models import Product, Bill, Order

from .serializers import (
  ProductCreateSerializer,
  ProductGetSerializer,
  OrderCreateSerializer,
  BillCreateSerializer,
  OrderListSerializer,
  OrderGetSerializer,
  OrderPaidSerializer
)


def only_message_with_status(message, status):
  response = {
    'success': False,
    'status_code': status,
    'message': message
  }
  return response


class ProductListView(APIView):
  """
  Products list

  @:parameter Header JWT token
  """
  serializer_class = ProductGetSerializer
  permission_classes = (IsAuthenticated,)

  def get(self, request):
    products = Product.products.get_all()
    serializer = self.serializer_class(products, many=True)
    response = {
      'success': True,
      'status_code': status.HTTP_200_OK,
      'message': _('Successfully fetched products'),
      'products': serializer.data

    }
    return Response(response, status=status.HTTP_200_OK)


class ProductGetByIdView(APIView):
  """
  Product get by id

  @:parameter Header JWT token, login as admin or storemaster
  @:parameter id
  """
  serializer_class = ProductGetSerializer
  permission_classes = (IsAuthenticated,)

  def get(self, request, *args, **kwargs):
    try:
      product = Product.products.filter(pk=kwargs['id']).get()
      serializer = self.serializer_class(product)
      response = {
        'success': True,
        'status_code': status.HTTP_200_OK,
        'message': _('Successfully fetched products'),
        'product': serializer.data

      }
      return Response(response, status=status.HTTP_200_OK)
    except Exception:
      response = {
        'success': False,
        'status_code': status.HTTP_400_BAD_REQUEST,
        'message': _('Product not found'),
      }
      return Response(response, status=status.HTTP_200_OK)


class ProductCreateView(APIView):
  """
  Product create

  @:parameter Header JWT token, login as admin or storemaster
  @:parameter title
  @:parameter regular_price
  @:parameter dicount_price (optional)
  @:parameter slug (optional)
  @:parameter description (optional)
  @:parameter is_active (optional)
  """
  serializer_class = ProductCreateSerializer
  permission_classes = (IsAuthenticated,)

  def post(self, request):
    user = request.user
    # check the roles, only admin and storemaster allowed
    if user.role not in (User.ADMIN, User.STOREMASTER):
      return Response(only_message_with_status(_('You are not authorized to perform this action'),
                                               status.HTTP_403_FORBIDDEN), status.HTTP_403_FORBIDDEN)
    else:
      # Mutable state for new QueryDict
      validate_data = request.data.copy()
      validate_data['who_created'] = user.pk
      serializer = self.serializer_class(data=validate_data)
      valid = serializer.is_valid(raise_exception=True)

      if valid:
        serializer.save()
        status_code = status.HTTP_201_CREATED

        response = {
          'success': True,
          'statusCode': status_code,
          'message': _('Product successfully created!'),
          'product': serializer.data
        }
        return Response(response, status=status_code)


class OrderCreateView(APIView):
  """
  Order create

  @:parameter Header JWT token, login as admin or cashier
  @:parameter product_id
  """
  permission_classes = (IsAuthenticated,)

  def post(self, request):
    user = request.user
    # check the roles, only admin and cashier allowed
    if user.role not in (User.ADMIN, User.CASHIER):
      return Response(only_message_with_status(_('You are not authorized to perform this action'),
                                               status.HTTP_403_FORBIDDEN), status.HTTP_403_FORBIDDEN)
    else:
      validate_data = request.data.copy()
      try:
        product = Product.products.filter(pk=validate_data['product_id']).get()
      except Exception:
        return Response(only_message_with_status(_('Product not exists'),
                                                 status.HTTP_403_FORBIDDEN), status.HTTP_403_FORBIDDEN)
      order, bill = Order.orders.create_new(product, user)
      order_serialize = OrderCreateSerializer(order).data
      bill_serialize = BillCreateSerializer(bill).data
      status_code = status.HTTP_201_CREATED

      response = {
        'success': True,
        'statusCode': status_code,
        'message': _('Order and Bill successfully created!'),
        'order': order_serialize,
        'bill': bill_serialize
      }
      return Response(response, status=status_code)


class OrderListView(APIView):
  """
  Orders list

  @:parameter Header JWT token, login as admin or storemaster
  """
  serializer_class = OrderListSerializer
  permission_classes = (IsAuthenticated,)

  def get(self, request, *args, **kwargs):
    user = request.user
    if user.role not in (User.ADMIN, User.CASHIER, User.ACCOUNTANT, User.SELLER):
      return Response(only_message_with_status(_('You are not authorized to perform this action'),
                                               status.HTTP_403_FORBIDDEN), status.HTTP_403_FORBIDDEN)
    else:
      if args:
        orders = Order.orders.get_by_date(args)
      else:
        orders = Order.orders.get_all()
      serializer = self.serializer_class(orders, many=True)
      response = {
        'success': True,
        'status_code': status.HTTP_200_OK,
        'message': _('Successfully fetched products'),
        'orders': serializer.data

      }
      return Response(response, status=status.HTTP_200_OK)


class OrderPaidView(APIView):
  """
  Order update status to paid

  @:parameter Header JWT token, login as admin, cashier or accountant
  @:parameter order_id
  """
  serializer_class = OrderPaidSerializer
  permission_classes = (IsAuthenticated,)

  def post(self, request):
    user = request.user
    if user.role not in (User.ADMIN, User.CASHIER, User.ACCOUNTANT):
      return Response(only_message_with_status(_('You are not authorized to perform this action'),
                                               status.HTTP_403_FORBIDDEN), status.HTTP_403_FORBIDDEN)
    else:
      validate_data = request.data.copy()
      try:
        order = Order.orders.filter(pk=validate_data['order_id']).get()
      except Exception:
        return Response(only_message_with_status(_('Order not exists'),
                                                 status.HTTP_401_UNAUTHORIZED), status.HTTP_401_UNAUTHORIZED)
      valid = Order.orders.set_paid_status(instance=order)
      if valid:
        serializer = self.serializer_class(order).data
        response = {
          'success': True,
          'status_code': status.HTTP_200_OK,
          'message': _('Successfully fetched products'),
          'orders': serializer
        }
        return Response(response, status=status.HTTP_200_OK)
      else:
        return Response(only_message_with_status(_('Order is not created or processing.'),
                                                 status.HTTP_401_UNAUTHORIZED), status.HTTP_401_UNAUTHORIZED)


class OrderUpdateView(APIView):
  """
  Order update

  @:parameter Header JWT token, login as admin, cashier, accountant, seller
  @:parameter order_id
  """
  serializer_class = OrderPaidSerializer
  permission_classes = (IsAuthenticated,)

  def post(self, request):
    user = request.user
    if user.role not in (User.ADMIN, User.CASHIER, User.ACCOUNTANT, User.SELLER):
      return Response(only_message_with_status(_('You are not authorized to perform this action'),
                                               status.HTTP_403_FORBIDDEN), status.HTTP_403_FORBIDDEN)
    else:
      validate_data = request.data.copy()
      try:
        order = Order.orders.filter(pk=validate_data['order_id']).get()
      except Exception:
        return Response(only_message_with_status(_('Order not exists.'),
                                                 status.HTTP_403_FORBIDDEN), status.HTTP_403_FORBIDDEN)
      valid = Order.orders.set_processing_status(instance=order)
      if valid:
        serializer = self.serializer_class(order).data
        response = {
          'success': True,
          'status_code': status.HTTP_200_OK,
          'message': _('Successfully fetched products'),
          'orders': serializer
        }
        return Response(response, status=status.HTTP_200_OK)
      else:
        return Response(only_message_with_status(_('Order is not created.'),
                                                 status.HTTP_403_FORBIDDEN), status.HTTP_403_FORBIDDEN)


class OrderCloseView(APIView):
  """
  Order update

  @:parameter Header JWT token, login as admin, cashier, accountant, seller
  @:parameter order_id
  """
  serializer_class = OrderPaidSerializer
  permission_classes = (IsAuthenticated,)

  def post(self, request):
    user = request.user
    if user.role not in (User.ADMIN, User.CASHIER, User.ACCOUNTANT, User.SELLER):
      return Response(only_message_with_status(_('You are not authorized to perform this action'),
                                               status.HTTP_403_FORBIDDEN), status.HTTP_403_FORBIDDEN)
    else:
      validate_data = request.data.copy()
      try:
        order = Order.orders.filter(pk=validate_data['order_id']).get()
      except Exception:
        return Response(only_message_with_status(_('Order not exists'),
                                                 status.HTTP_403_FORBIDDEN), status.HTTP_403_FORBIDDEN)
      valid = Order.orders.set_done_status(instance=order)
      if valid:
        serializer = self.serializer_class(order).data
        response = {
          'success': True,
          'status_code': status.HTTP_200_OK,
          'message': _('Successfully fetched products'),
          'orders': serializer
        }
        return Response(response, status=status.HTTP_200_OK)
      else:
        return Response(only_message_with_status(_('Order is not paid'),
                                                 status.HTTP_403_FORBIDDEN), status.HTTP_403_FORBIDDEN)


class OrderGetByIdView(APIView):
  """
  Order update

  @:parameter Header JWT token, login as admin, cashier, accountant, seller
  @:parameter order_id
  """
  serializer_class = OrderGetSerializer
  permission_classes = (IsAuthenticated,)

  def get(self, request, *args, **kwargs):
    user = request.user
    if user.role not in (User.ADMIN, User.CASHIER, User.ACCOUNTANT, User.SELLER):
      return Response(only_message_with_status(_('You are not authorized to perform this action'),
                                               status.HTTP_403_FORBIDDEN), status.HTTP_403_FORBIDDEN)
    else:
      try:
        order = Order.orders.filter(pk=kwargs['id']).get()
      except Exception:
        return Response(only_message_with_status(_('Order not exists'),
                                                 status.HTTP_403_FORBIDDEN), status.HTTP_403_FORBIDDEN)
      serializer = self.serializer_class(order).data
      response = {
        'success': True,
        'status_code': status.HTTP_200_OK,
        'message': _('Successfully fetched order'),
        'orders': serializer
      }
      return Response(response, status=status.HTTP_200_OK)
