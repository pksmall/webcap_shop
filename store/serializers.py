from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import Product


class ProductCreateSerializer(serializers.ModelSerializer):
  """
  Product Create Serializer
  """
  class Meta:
    model = Product
    fields = [
      'title',
      'regular_price',
      'discount_price',
      'slug',
      'description',
      'is_active',
      'who_created'
    ]

  def create(self, validated_data):
    product = Product.objects.create(title=validated_data['title'], regular_price=validated_data['regular_price'],
                                     who_created=validated_data['who_created'])
    return product

  def validate(self, data):
    if not data['title']:
        raise serializers.ValidationError(_("title required"))
    if not data['regular_price']:
        raise serializers.ValidationError(_("regular_price required"))
    return data


class ProductGetSerializer(serializers.ModelSerializer):
  """
  Product Getter Serializer
  """
  class Meta:
    model = Product
    fields = [
      'id',
      'title',
      'regular_price',
      'discount_price',
      'created_at',
      'updated_at'
    ]
