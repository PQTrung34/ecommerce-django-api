from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
# Create your views here.


def createOrder(request):
    try:
        if request.method != 'POST':
            return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)
        
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'You are not login'}, status=403)
        
        user = request.user
        Order.objects.create(customer=user)
        return JsonResponse({'success': True, 'message': 'Order created successfully!'}, status=201)

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
    

def getOrders(request):
    try:
        if request.method != 'GET':
            return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)
        
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'You are not login'}, status=403)
        
        orders = Order.objects.filter(customer=request.user).order_by('-created_at')
        data = [{
            'id': order.id,
            'created_at': order.created_at
            } for order in orders]
        return JsonResponse({'success': True, 'data': data}, status=200)

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
    

def getOrderById(request, id):
    try:
        if request.method != 'GET':
            return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)
        
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'You are not login'}, status=403)
        
        order = Order.objects.get(customer=request.user, id=id)
        if not order:
            return JsonResponse({'success': False, 'message': 'Order not found'}, status=404)
        data = [{
            'product': item.product.name,
            'quantity': item.quantity,
            'price': item.product.price,
            'total': item.get_total
            } for item in order.orderitem_set.all()]
        total_order_amount = sum(item.get_total for item in order.orderitem_set.all())
        return JsonResponse({'success': True, 'data': data, 'total_order_amount': total_order_amount}, status=200)

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
    

def updateOrderStatus(request, id, status):
    try:
        if request.method != 'PUT':
            return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)
        
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'You are not login'}, status=403)
        
        order = Order.objects.get(customer=request.user, id=id)
        if not order:
            return JsonResponse({'success': False, 'message': 'Order not found'}, status=404)
        
        order.complete = status
        order.save()

        return JsonResponse({'success': True, 'message': 'Order status updated successfully!'}, status=200)

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
    

def addOrderItem(request):
    try:
        if request.method != 'POST':
            return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)
        
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'You are not login'}, status=403)
        
        data = json.loads(request.body)
        orderId = data.get('orderId')
        productId = data.get('productId')

        if not orderId or not productId:
            return JsonResponse({'success': False, 'message': 'OrderId and productId are required'}, status=400)
        
        order = Order.objects.get(customer=request.user, id=orderId)
        if not order:
            return JsonResponse({'success': False, 'message': 'Order not found'}, status=404)

        product = Product.objects.get(id=productId)
        if not product:
            return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
        
        orderItem = OrderItem.objects.filter(order=order, product=product).first()
        if orderItem:
            orderItem.quantity += 1
            orderItem.save()
            return JsonResponse({'success': True, 'message': 'Order item updated successfully!'}, status=200)
        
        OrderItem.objects.create(order=order, product=product, quantity=1)

        return JsonResponse({'success': True, 'message': 'Order item added successfully!'}, status=201)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
    
def removeOrderItem(request):
    try:
        if request.method != 'POST':
            return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)
        
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'You are not login'}, status=403)
        
        data = json.loads(request.body)
        orderId = data.get('orderId')
        productId = data.get('productId')
        if not orderId or not productId:
            return JsonResponse({'success': False, 'message': 'OrderId and productId are required'}, status=400)
        
        order = Order.objects.get(customer=request.user, id=orderId)
        if not order:
            return JsonResponse({'success': False, 'message': 'Order not found'}, status=404)

        product = Product.objects.get(id=productId)
        if not product:
            return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
        
        orderItem = OrderItem.objects.filter(order=order, product=product).first()
        if not orderItem:
            return JsonResponse({'success': False, 'message': 'Order item not found'}, status=404)
        
        if orderItem.quantity > 1:
            orderItem.quantity -= 1
            orderItem.save()
            return JsonResponse({'success': True, 'message': 'Order item quantity updated successfully!'}, status=200)
        
        orderItem.delete()
        return JsonResponse({'success': True, 'message': 'Order item deleted successfully!'}, status=204)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)