from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json

# Create your views here.

def index(request):
    return JsonResponse({'success': True, 'message': 'Hello World!'}, status=200)

def registerUser(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                return JsonResponse({'success': False, 'message': 'Username and password are required'}, status=400)
            
            userExist = User.objects.filter(username=username).exists()
            if userExist:
                return JsonResponse({'success': False, 'message': 'User already exists'}, status=200)
            User.objects.create_user(username=username, password=password)
            return JsonResponse({'success': True, 'message': 'User created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)

def loginUser(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return JsonResponse({'success': False, 'message': 'Username and password are required'}, status=400)
        
        user = User.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'success': False, 'message': 'Login failed'}, status=401)
    return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)

def logoutUser(request):
    try:
        logout(request)
        return JsonResponse({'success': True, 'message': 'Logout successful'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400) 