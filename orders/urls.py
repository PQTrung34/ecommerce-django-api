from django.urls import path
from . import views

urlpatterns = [
    path('create-order/', views.createOrder, name='create-order'),
    path('get-orders/', views.getOrders, name='get-orders'),
    path('get-order/<id>/', views.getOrderById, name='get-order'),
    path('add-order-item/', views.addOrderItem, name='add-order-item'),
    path('update-order-status/<id>/', views.updateOrderStatus, name='update-order-status'),
    path('remove-order-item/', views.removeOrderItem, name='remove-order-item'),
]