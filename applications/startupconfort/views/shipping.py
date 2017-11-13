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

from applications.startupconfort.forms import ShippingAddressForm
from applications.startupconfort.models import ShippingAddress


"""
tinker-toy
http://patorjk.com/software/taag/#p=display&f=Tinker-Toy&t=VoteUpAndDown

 o-o  o                                  O     o    o
|     |    o           o                / \    |    |
 o-o  O--o   o-o  o-o    o-o  o--o     o---o o-O  o-O o-o o-o o-o o-o
    | |  | | |  | |  | | |  | |  |     |   ||  | |  | |   |-'  \   \
o--o  o  o | O-o  O-o  | o  o o--O     o   o o-o  o-o o   o-o o-o o-o
             |    |              |
             o    o           o--o

"""

class ShippingAddressCreateView(LoginRequiredMixin, CreateView):
    template_name = "shippingaddress/create.html"
    form_class = ShippingAddressForm
    success_url = reverse_lazy('startupconfort:checkout_view')

    def form_valid(self, form):
        """
        Assign the author to the request.user
        """
        form.instance.customer = self.request.user
        return super(ShippingAddressCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ShippingAddressUpdateView, self).get_context_data(**kwargs)
        context['breadcrumb'] = 'shipping'
        context['title'] = 'shipping'
        return context

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update stories """
        user = request.user
        if user.cartitem_set.count() < 1:
            messages.warning(request, "You cannot create a Shipping Address if you have no item in your cart")
            return redirect(reverse_lazy('startupconfort:my_shopping_cart'))
        return super(ShippingAddressCreateView, self).dispatch(request, *args, **kwargs)


class ShippingAddressDeleteView(LoginRequiredMixin, DeleteView):
    model = ShippingAddress
    success_url = reverse_lazy('startupconfort:checkout_view')

    def get_context_data(self, **kwargs):
        context = super(ShippingAddressDeleteView, self).get_context_data(**kwargs)
        context['breadcrumb'] = 'shipping'
        return context

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update stories """
        obj = self.get_object()
        if obj.customer != self.request.user:
            messages.warning(request, "This Shipping Cart doesn't belongs to your account")
            return redirect(obj)
        return super(ShippingAddressDeleteView, self).dispatch(request, *args, **kwargs)

class ShippingAddressUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "shippingaddress/update.html"
    model = ShippingAddress
    form_class = ShippingAddressForm
    success_url = reverse_lazy('startupconfort:checkout_view')

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update stories """
        obj = self.get_object()
        if obj.customer != self.request.user:
            messages.warning(request, "This Shipping Cart doesn't belongs to your account")
            return redirect(obj)
        user = request.user
        if user.cartitem_set.count() < 1:
            messages.warning(request, "You cannot update your Shipping Address if you have no item in your cart")
            return redirect(reverse_lazy('startupconfort:my_shopping_cart'))
        return super(ShippingAddressUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ShippingAddressUpdateView, self).get_context_data(**kwargs)
        context['breadcrumb'] = 'shipping'
        context['title'] = 'shipping'
        return context
