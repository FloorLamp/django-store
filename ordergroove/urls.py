from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('shoppingcart.views',
    url(r'^$', 'home', name='home'),
    url(r'^login$', 'login_view', name='login_view'),
    url(r'^logout$', 'logout_view', name='logout_view'),
    url(r'^cart$', 'cart', name='cart'),
    url(r'^checkout$', 'checkout', name='checkout'),
    url(r'^orders$', 'orders', name='orders'),
    
    # ajax
    url(r'^modify_cart$', 'modify_cart', name='modify_cart'),
    
    # admin
    url(r'^admin/', include(admin.site.urls)),
)
