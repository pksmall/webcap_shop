from django.urls import path

from .views import (
    ProductCreateView,
    ProductListView,
    ProductGetByIdView
)

urlpatterns = [
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/get/<int:id>', ProductGetByIdView.as_view(), name='product_get_by_id')
]
