from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
# Create your views here.

def createCategory(request):
    try:
        if request.method != 'POST':
            return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)

        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'You are not login'}, status=403)
        
        if not request.user.is_superuser:
            return JsonResponse({'success': False, 'message': 'You are not admin'}, status=403)

        data = json.loads(request.body)
        name = data.get('name')
        if not name:
            return JsonResponse({'success': False, 'message': 'Name is required'}, status=400)

        if Category.objects.filter(name=name).exists():
            return JsonResponse({'success': False, 'message': 'Category already exists'}, status=200)

        Category.objects.create(name=name)
        return JsonResponse({'success': True, 'message': 'Category created successfully!'}, status=201)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


def getCategories(request):
    try:
        if request.method != 'GET':
            return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)

        categories = Category.objects.all()
        data = [{'id': category.id, 'name': category.name} for category in categories]

        return JsonResponse({'success': True, 'data': data}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


def createProduct(request):
    try:
        if request.method != 'POST':
            return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)

        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'You are not login'}, status=403)
        
        if not request.user.is_superuser:
            return JsonResponse({'success': False, 'message': 'You are not admin'}, status=403)

        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        category = data.get('category')

        if not name or not description or not price or not category:
            return JsonResponse({'success': False, 'message': 'Product infomations are required'}, status=400)

        if Product.objects.filter(name=name).exists():
            return JsonResponse({'success': False, 'message': 'Product already exists'}, status=200)

        category = Category.objects.get(name=str(category).lower())
        if not category:
            return JsonResponse({'success': False, 'message': 'Category not found'}, status=404)
        
        Product.objects.create(name=name, description=description, price=price, category=category)
        return JsonResponse({'success': True, 'message': 'Product created successfully!'}, status=201)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


def getProductsByCategory(request, slug):
    try:
        if request.method != 'GET':
            return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)
        
        category = Category.objects.filter(slug=slug).first()
        if not category:
            return JsonResponse({'success': False, 'message': 'Category not found'}, status=404)

        products = Product.objects.filter(category__slug=slug)
        data = [{'id': product.id, 'name': product.name, 'description': product.description, 'price': product.price} for product in products]

        return JsonResponse({'success': True, 'data': data}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


def updateProduct(request, id):
    try:
        if request.method != 'PUT':
            return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)

        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'You are not login'}, status=403)
        
        if not request.user.is_superuser:
            return JsonResponse({'success': False, 'message': 'You are not admin'}, status=403)
        
        # if not Product.objects.filter(id=id).exists():
        #     return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
        
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        category = data.get('category')

        if not name or not description or not price or not category:
            return JsonResponse({'success': False, 'message': 'Product infomations are required'}, status=400)

        category = Category.objects.get(name=str(category).lower())
        if not category:
            return JsonResponse({'success': False, 'message': 'Category not found'}, status=404)
        
        product = Product.objects.get(id=id)
        if not product:
            return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
        
        product.name = name
        product.description = description
        product.price = price
        product.category = category
        product.save()

        return JsonResponse({'success': True, 'message': 'Product updated successfully!'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


def deleteProduct(request, id):
    try:
        if request.method != 'DELETE':
            return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)

        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'You are not login'}, status=403)
        
        if not request.user.is_superuser:
            return JsonResponse({'success': False, 'message': 'You are not admin'}, status=403)

        product = Product.objects.get(id=id)
        if not product:
            return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)

        product.delete()
        return JsonResponse({'success': True, 'message': 'Product deleted successfully!'}, status=204)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)