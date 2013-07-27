from models import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

def home(request, template='index.html'):
    products = Product.objects.all()
    template_params = {'products': products}
    return render_to_response(template, template_params, RequestContext(request))