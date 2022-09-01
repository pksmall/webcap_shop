from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _

from users.models import User
from .models import Product

from .serializers import (
  ProductCreateSerializer,
  ProductGetSerializer
)


class ProductListView(APIView):
  """
  Products list

  @:parameter Header JWT token
  """
  serializer_class = ProductGetSerializer
  permission_classes = (IsAuthenticated,)

  def get(self, request):
    products = Product.objects.all()
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
      product = Product.objects.filter(pk=kwargs['id']).get()
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
      response = {
        'success': False,
        'status_code': status.HTTP_403_FORBIDDEN,
        'message': _('You are not authorized to perform this action')
      }
      return Response(response, status.HTTP_403_FORBIDDEN)
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