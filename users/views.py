from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.translation import gettext_lazy as _

from .serializers import (
    AuthUserRegistrationSerializer,
    AuthUserLoginSerializer,
    AuthUserListSerializer
)

from .models import User


class AuthUserRegistrationView(APIView):
  """
  Register view endpoint

  @:parameter email
  @:parameter password
  @:parameter role (optional)
  @:parameter first_name (optional)
  @:parameter last_name (optional)
  """
  serializer_class = AuthUserRegistrationSerializer
  permission_classes = (AllowAny, )

  def post(self, request):
      serializer = self.serializer_class(data=request.data)
      valid = serializer.is_valid(raise_exception=True)

      if valid:
          serializer.save()
          status_code = status.HTTP_201_CREATED

          response = {
              'success': True,
              'statusCode': status_code,
              'message': _('User successfully registered!'),
              'user': serializer.data
          }

          return Response(response, status=status_code)


class AuthUserListView(APIView):
  """
  List view

  @:parameter Header with JWT access token
  """
  serializer_class = AuthUserListSerializer
  permission_classes = (IsAuthenticated,)

  def get(self, request):
    user = request.user
    if user.role != User.ADMIN:
      response = {
        'success': False,
        'status_code': status.HTTP_403_FORBIDDEN,
        'message': _('You are not authorized to perform this action')
      }
      return Response(response, status.HTTP_403_FORBIDDEN)
    else:
      users = User.objects.all()
      serializer = self.serializer_class(users, many=True)
      response = {
        'success': True,
        'status_code': status.HTTP_200_OK,
        'message': _('Successfully fetched users'),
        'users': serializer.data

      }
      return Response(response, status=status.HTTP_200_OK)


class AuthUserLoginView(APIView):
  """
  Login view

  @:parameter email
  @:parameter password
  """
  serializer_class = AuthUserLoginSerializer
  permission_classes = (AllowAny,)

  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    valid = serializer.is_valid(raise_exception=True)

    if valid:
      status_code = status.HTTP_200_OK

      response = {
        'success': True,
        'statusCode': status_code,
        'message': _('User logged in successfully'),
        'access': serializer.data['access'],
        'refresh': serializer.data['refresh'],
        'authenticatedUser': {
          'email': serializer.data['email'],
          'role': serializer.data['role']
        }
      }

      return Response(response, status=status_code)
