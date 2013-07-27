from decimal import Decimal
import json

from models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
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
    total_price = sum([p.count * p.product.price for p in products])
    template_params = {
        'products': products,
        'total_price': total_price,
    }
    return render_to_response(template, template_params, RequestContext(request))
    
@login_required
def modify_cart(request):
    response = {}
    if request.is_ajax() and request.method == 'POST':
        if 'id' in request.POST and 'action' in request.POST:
            action = request.POST['action']
            try:
                product = Product.objects.get(id=request.POST['id'])
            except ObjectDoesNotExist:
                response['status'] = 'product not found'
                return HttpResponse(json.dumps(response), mimetype='application/json')
            
            if action == 'add':
                cart_product, created = ShoppingCart.objects.get_or_create(user=request.user, product=product)
                cart_product.count += 1
                cart_product.save()
                response['status'] = 'ok'
                response['cart'] = list(ShoppingCart.objects.filter(user=request.user).values('product__name', 'product__image_url', 'product__price', 'count'))
            elif action == 'delete':
                ShoppingCart.objects.filter(user=request.user, product=product).delete()
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
                    
                cart_product.count = count
                cart_product.save()
            
    return HttpResponse(json.dumps(response, cls=JSONEncoder), mimetype='application/json')

class JSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(JSONEncoder, self).default(obj)