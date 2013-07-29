from decimal import Decimal
import json

from models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

def home(request, template='index.html'):
    products = Product.objects.all()
    login_error = request.session.pop('login_error', None)
    template_params = {
        'subdomain': request.subdomain,
        'products': products,
        'login_error': login_error,
    }
    return render_to_response(template, template_params, RequestContext(request))
    
def register(request, template='register.html'):
    if request.user.is_authenticated():
        return redirect('home')
    template_params = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            template_params['errors'] = form.errors
    
    return render_to_response(template, template_params, RequestContext(request))
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            request.session['login_error'] = 'Invalid username or password'
    
    return redirect('home')
        
def logout_view(request):
    logout(request)
    
    return redirect('home')

@login_required
def cart(request, template='cart.html'):
    products = ShoppingCart.objects.filter(user=request.user)
    total_price = sum([p.count * p.product.price for p in products])
    template_params = {
        'products': products,
        'total_price': total_price,
    }
    return render_to_response(template, template_params, RequestContext(request))
    
@login_required
def checkout(request, template='checkout.html'):
    if request.method == 'POST':
        cart_products = ShoppingCart.objects.filter(user=request.user)        
        if cart_products:
            new_order = Order(user=request.user)
            new_order.save()
            for p in cart_products:
                order_product = OrderProduct(order=new_order, product=p.product, count=p.count)
                order_product.save()
            cart_products.delete()
            request.session['new_order'] = new_order
        return redirect('checkout')
    else:
        if 'new_order' in request.session:
            template_params = {
                'new_order': request.session.pop('new_order')
            }
            return render_to_response(template, template_params, RequestContext(request))
        else:
            return redirect('orders')
    
@login_required
def orders(request, template='orders.html'):
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    template_params = {
        'orders': orders,
    }
    return render_to_response(template, template_params, RequestContext(request))
    
@login_required
def modify_cart(request):
    response = {}
    if request.method == 'POST' and 'id' in request.POST and 'action' in request.POST:
        action = request.POST['action']
        try:
            product = Product.objects.get(id=request.POST['id'])
        except ObjectDoesNotExist:
            response['status'] = 'product not found'
            return HttpResponse(json.dumps(response), mimetype='application/json')
            
        if action == 'add':
            if not product.change_quantity(-1):
                response['status'] = 'product unavailable'
                return HttpResponse(json.dumps(response), mimetype='application/json')
            cart_product, created = ShoppingCart.objects.get_or_create(user=request.user, product=product)
            cart_product.count = F('count') + 1
            cart_product.save()
            response['status'] = 'ok'
            response['product_quantity'] = Product.objects.get(id=request.POST['id']).quantity
        elif action == 'delete':
            try:
                cart_product = ShoppingCart.objects.get(user=request.user, product=product)
            except ObjectDoesNotExist:
                response['status'] = 'product not in cart'
                return HttpResponse(json.dumps(response), mimetype='application/json')
                
            product.change_quantity(cart_product.count)
            cart_product.delete()
            response['status'] = 'ok'
        elif action == 'update' and 'count' in request.POST:
            try:
                cart_product = ShoppingCart.objects.get(user=request.user, product=product)
            except ObjectDoesNotExist:
                response['status'] = 'product not found'
                return HttpResponse(json.dumps(response), mimetype='application/json')
                
            try:
                count = int(request.POST['count'])
            except:
                response['status'] = 'invalid count'
                return HttpResponse(json.dumps(response), mimetype='application/json')
            
            if product.change_quantity(cart_product.count-count):
                cart_product.count = count
                cart_product.save()
                response['status'] = 'ok'
            else:
                response['status'] = 'product unavailable'
            
    return HttpResponse(json.dumps(response, cls=JSONEncoder), mimetype='application/json')

class JSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(JSONEncoder, self).default(obj)