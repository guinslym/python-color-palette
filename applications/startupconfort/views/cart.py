from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.base import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

#logging
import logging
logger = logging.getLogger(__name__)

#Django
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.http import HttpResponseRedirect

#Protection
from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

#messages
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


from applications.startupconfort.models import Startup
from applications.startupconfort.models import StartupProduct
from applications.startupconfort.models import StartupColor
from applications.startupconfort.models import Gallery as StartupProductImage
from applications.startupconfort.models import CartItem

from applications.startupconfort.forms import CartItemQuantityForm

from django.contrib.auth.models import User

from hitcount.models import HitCount
from hitcount.views import HitCountDetailView

import braintree

"""
tinker-toy
http://patorjk.com/software/taag/#p=display&f=Tinker-Toy&t=VoteUpAndDown

  o-o          o  o   o
 /             |  |   | o
O      oo o-o -o- o   o   o-o o   o   o
 \    | | |    |   \ /  | |-'  \ / \ /
  o-o o-o-o    o    o   | o-o   o   o




"""


def get_total_price_of_the_shipping_cart(user):
    number_of_products = CartItem.objects.filter(customer=user).count()
    if (number_of_products > 0):
        total = 8 + sum([item.product.price * item.quantity for item in CartItem.objects.filter(customer=user) ] )
    else:
        total = 0
    return total

import braintree

def get_braintree_client_token():
    braintree.Configuration.configure(
              braintree.Environment.Sandbox,
              merchant_id=settings.BRAINTREE_MERCHANT_ID,
              public_key=settings.BRAINTREE_PUBLIC_KEY,
              private_key=settings.BRAINTREE_PRIVATE_KEY
                              )
    client_token = braintree.ClientToken.generate()
    return client_token


class AddToCartView(LoginRequiredMixin, TemplateView):
    template_name = 'startupconfort/cart.html'

    def is_this_product_is_already_in_the_cart(self, cartitems, product):
        # import pytest; pytest.set_trace()
        if (len(cartitems) >= 1) :
            for item in cartitems:
                if item.product.slug == product.slug:
                    return True
        return False

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        product = get_object_or_404(StartupProduct, slug=kwargs['slug'] )
        user = request.user
        # Request all the cartitems belonging to the user.
        cartitems = CartItem.objects.filter(customer=user, product=product).all()

        if self.is_this_product_is_already_in_the_cart(cartitems, product):
            #messages
            messages.info(request, 'this product is already in your shopping cart')
            return render(request, 'startupconfort/cart.html', context)
        else:
            #add the production into the Shopping Cart
            CartItem.objects.create(customer=user, product=product)
            #messages
            context['total'] = get_total_price_of_the_shipping_cart(user)
            messages.success(request, 'We added that product into your cart')
            return render(request, 'startupconfort/cart.html', context)

    def get_context_data(self, **kwargs):
        context = super(AddToCartView, self).get_context_data(**kwargs)
        user = self.request.user
        context['cartitem_list'] = CartItem.objects.filter(customer=user)
        context['title'] = "Cart"
        # context['client_token'] = get_braintree_client_token()
        return context


class ShowCartItemsListView(LoginRequiredMixin, ListView):
    model = CartItem
    context_object_name = 'cartitem_list'
    template_name = 'startupconfort/cart.html'

    def get_queryset(self):
        user=self.request.user
        return CartItem.objects.filter(customer=user)

    def get_context_data(self, **kwargs):
        context = super(ShowCartItemsListView, self).get_context_data(**kwargs)
        user = self.request.user
        # context['client_token'] = get_braintree_client_token()
        context['title'] = 'Cart'
        number_of_products = CartItem.objects.filter(customer=user).count()
        context['total'] = get_total_price_of_the_shipping_cart(user)
        context['breadcrumb'] = 'cart'
        return context


class CartItemDeleteView(LoginRequiredMixin, DeleteView):
    #Delete an item in the cart
    model = CartItem

    def get_success_url(self):
        """
        I do have a bug here
        """
        user = self.request.user
        number_of_products = CartItem.objects.filter(customer=user).count()
        # import ipdb; ipdb.set_trace()
        if number_of_products > 0:
            return reverse_lazy('startupconfort:my_shopping_cart')
        else:
            return reverse_lazy('startupconfort:homepage')

    def get_context_data(self, **kwargs):
        context = super(CartItemDeleteView, self).get_context_data(**kwargs)
        user = self.request.user
        context['title'] = "Update the Quantity"
        return context

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update stories """
        obj = self.get_object()
        if obj.customer != self.request.user:
            messages.warning(request, "This Cart Item doesn't belongs to your account")
            return redirect(obj)
        return super(CartItemDeleteView, self).dispatch(request, *args, **kwargs)


class CartItemQuantityUpdateView(LoginRequiredMixin, UpdateView):
    template_name_suffix = '/update' #startupconfort/cartitem/update
    model = CartItem
    form_class = CartItemQuantityForm

    def get_success_url(self):
            # if 'slug' in self.kwargs:
            #     slug = self.kwargs['slug']
            # else:
            #     slug = 'demo'
            # return reverse('startupconfort:homepage', kwargs={'pk': self._id, 'slug': slug})
            return reverse_lazy('startupconfort:my_shopping_cart')

    def get_context_data(self, **kwargs):
        context = super(CartItemQuantityUpdateView, self).get_context_data(**kwargs)
        user = self.request.user
        context['title'] = "Update the Quantity"
        return context

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update stories """
        obj = self.get_object()
        if obj.customer != self.request.user:
            messages.warning(request, "This Cart Item doesn't belongs to your account")
            return redirect(obj)
        return super(CartItemQuantityUpdateView, self).dispatch(request, *args, **kwargs)
