from models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

def home(request, template='index.html'):
    products = Product.objects.all()
    template_params = {'products': products}
    return render_to_response(template, template_params, RequestContext(request))
    
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
    else:
        pass
    
    return redirect('home')
        
def logout_view(request):
    logout(request)
    
    return redirect('home')

@login_required
def cart(request, template='cart.html'):
    products = ShoppingCart.objects.filter(user=request.user)
    template_params = {'products': products}
    return render_to_response(template, template_params, RequestContext(request))