from django.contrib import admin
# from django.contrib.sites.models import Site, Group
from shoppingcart.models import *

class ProductAdmin(admin.ModelAdmin):
    def product_pic(self, obj):
        if obj.image_url and obj.image_url != 'null':
            return '<img src="{0}" style="max-width:50px;max-height:50px;" />'.format(obj.image_url)
        else:
            return ''
    product_pic.allow_tags = True
    product_pic.admin_order_field = 'image_url'
    
    list_display = ('product_pic', 'id', 'name', 'quantity', 'price', 'description')
    list_display_links = ('name',)
    search_fields = ['product_id', 'name', 'product_description']
    
class ShoppingCartAdmin(admin.ModelAdmin):
    def user_name(self, obj):
        return obj.user.get_full_name()
    list_display = ('user_name', 'product', 'count', 'date_added')
    search_fields = ['user__first_name', 'user__last_name', 'product__name']
        
class OrderAdmin(admin.ModelAdmin):
    def user_name(self, obj):
        return obj.user.get_full_name()
    
    def order_products(self, obj):
        return '<br>'.join(['{} - {} - {}'.format(o.count, o.product.price, o.product.name) for o in obj.get_orders()])
    order_products.allow_tags = True
    
    def order_total(self, obj):
        return '${}'.format(obj.get_price())
        
    list_display = ('user_name', 'id', 'date_ordered')
    search_fields = ['user__first_name', 'user__last_name']
    readonly_fields = ('order_products', 'order_total')
    
# admin.site.unregister(Site)
# admin.site.unregister(Group)
admin.site.register(Product, ProductAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Order, OrderAdmin)