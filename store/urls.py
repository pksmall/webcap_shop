from django.urls import path

from .views import (
    ProductCreateView,
    ProductListView,
    ProductGetByIdView,
    OrderCreateView,
    OrderListView,
    OrderUpdateView,
    OrderCloseView,
    OrderGetByIdView
)

urlpatterns = [
    # products endpoints
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/get/<int:id>', ProductGetByIdView.as_view(), name='product_get_by_id'),

    # orders endpoints
    path('order/create/', OrderCreateView.as_view(), name='order_create'),
    path('order/list/', OrderListView.as_view(), name='order_list'),
    path('order/update/', OrderUpdateView.as_view(), name='order_update'),
    path('order/close/', OrderCloseView.as_view(), name='order_close'),
    path('order/get/<int:id>', OrderGetByIdView.as_view(), name='order_get_by_id'),
]
