from django.urls import path
from . import views

urlpatterns = [
    path('create-category/', views.createCategory, name='create-category'),
    path('categories/', views.getCategories, name='get-categories'),
    path('create-product/', views.createProduct, name='create-product'),
    path('category/<slug>/', views.getProductsByCategory, name='get-products-by-category'),
    path('update-product/<id>/', views.updateProduct, name='update-product'),
    path('delete-product/<id>/', views.deleteProduct, name='delete-product'),
]