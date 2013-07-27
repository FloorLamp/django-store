from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('shoppingcart.views',
    # Examples:
    url(r'^$', 'home', name='home'),
    url(r'^login$', 'login_view', name='login_view'),
    url(r'^logout$', 'logout_view', name='logout_view'),
    url(r'^cart$', 'cart', name='cart'),
    # url(r'^ordergroove/', include('ordergroove.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
