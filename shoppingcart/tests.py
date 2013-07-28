from decimal import Decimal
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from shoppingcart.models import *

class ShoppingCartTests(TestCase):
    client = Client()
        
    def test_product_quantity(self):
        """
        Tests that changing product quantity works.
        """
        product = Product.objects.create(name='Test product', price=Decimal('100'), quantity=10)
        for i in xrange(5):
            product.change_quantity(-1)
        product = Product.objects.get(id=product.id)
        self.assertEqual(product.quantity, 5)
        
        product.change_quantity(1)
        product = Product.objects.get(id=product.id)
        self.assertEqual(product.quantity, 6)
        
        product.quantity = 0
        product.save()
        product.change_quantity(-1)
        product = Product.objects.get(id=product.id)
        self.assertEqual(product.quantity, 0)
        
    def test_cart(self):
        """
        Tests cart functionality.
        """
        product = Product.objects.create(name='Test product', price=Decimal('100'), quantity=10)
        product2 = Product.objects.create(name='Test product 2', price=Decimal('20'), quantity=50)
        
        # assert products are displayed
        response = self.client.get(reverse('home'))
        self.assertQuerysetEqual(response.context['products'], ['<Product: {}>'.format(p) for p in Product.objects.all()])
        
        # create user and login, add product to cart
        user = User.objects.create_user('test', None, 'test')
        self.client.login(username='test', password='test')
        self.client.post(reverse('modify_cart'), {'id': product.id, 'action': 'add'})
        product = Product.objects.get(id=product.id)
        cart_product = ShoppingCart.objects.filter(user=user, product=product)[0]
        
        # assert product shows up in cart
        response = self.client.get(reverse('cart'))
        self.assertQuerysetEqual(response.context['products'], ['<ShoppingCart: {}>'.format(cart_product)])
        
        # assert correct product, product quantity and count
        self.assertEqual(cart_product.product, product)
        self.assertEqual(product.quantity, 9)
        self.assertEqual(cart_product.count, 1)
        
        # update product count in cart
        self.client.post(reverse('modify_cart'), {'id': product.id, 'action': 'update', 'count': 5})
        product = Product.objects.get(id=product.id)
        cart_product = ShoppingCart.objects.filter(user=user, product=product)[0]
        
        # assert product updated in cart
        self.assertEqual(product.quantity, 5)
        self.assertEqual(cart_product.count, 5)
        
        # assert total price
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.context['total_price'], 5 * Decimal('100'))
        
        # delete product from cart
        self.client.post(reverse('modify_cart'), {'id': product.id, 'action': 'delete'})
        product = Product.objects.get(id=product.id)
        self.assertEqual(product.quantity, 10)
        self.assertEqual(ShoppingCart.objects.filter(user=user, product=product).count(), 0)
        
        # assert nothing in cart after being removed
        response = self.client.get(reverse('cart'))
        self.assertQuerysetEqual(response.context['products'], [])
        
    def test_orders(self):
        """
        Tests ordering functionality.
        """
        product = Product.objects.create(name='Test product', price=Decimal('100'), quantity=10)
        product2 = Product.objects.create(name='Test product 2', price=Decimal('20'), quantity=50)
        
        # create user and login
        user = User.objects.create_user('test', None, 'test')
        self.client.login(username='test', password='test')
        
        # order products
        self.client.post(reverse('modify_cart'), {'id': product.id, 'action': 'add'})
        self.client.post(reverse('modify_cart'), {'id': product.id, 'action': 'update', 'count': 2})
        self.client.post(reverse('modify_cart'), {'id': product2.id, 'action': 'add'})
        self.client.post(reverse('modify_cart'), {'id': product2.id, 'action': 'update', 'count': 20})
        self.client.post(reverse('checkout'))
        product = Product.objects.get(id=product.id)
        product2 = Product.objects.get(id=product2.id)
        
        # assert nothing in cart after ordering
        self.assertEqual(ShoppingCart.objects.filter(user=user, product=product).count(), 0)
        
        # assert order exists and correct products and price
        order = Order.objects.filter(user=user)[0]
        order_products = order.get_orders()
        self.assertEqual(order_products.count(), 2)
        self.assertEqual(order_products.get(id=product.id).product, product)
        self.assertEqual(order_products.get(id=product2.id).product, product2)
        self.assertEqual(order.get_price(), 2 * Decimal('100') + 20 * Decimal('20'))
        
        # assert order shows up in orders
        response = self.client.get(reverse('orders'))
        self.assertQuerysetEqual(response.context['orders'], ['<Order: {}>'.format(order)])
        