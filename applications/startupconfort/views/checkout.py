import uuid
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.base import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

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
from applications.startupconfort.models import Purchase

from applications.startupconfort.forms import CartItemQuantityForm

from django.contrib.auth.models import User

from hitcount.models import HitCount
from hitcount.views import HitCountDetailView

import braintree

from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail

def get_total_price_of_the_shipping_cart(user):
    number_of_products = CartItem.objects.filter(customer=user).count()
    if (number_of_products > 0):
        total = 8 + sum([item.product.price * item.quantity for item in CartItem.objects.filter(customer=user) ] )
    else:
        total = 0
    return total

def get_braintree_client_token():
    braintree.Configuration.configure(
              braintree.Environment.Sandbox,
              merchant_id=settings.BRAINTREE_MERCHANT_ID,
              public_key=settings.BRAINTREE_PUBLIC_KEY,
              private_key=settings.BRAINTREE_PRIVATE_KEY
                              )
    client_token = braintree.ClientToken.generate()
    return client_token

"""
tinker-toy
http://patorjk.com/software/taag/#p=display&f=Tinker-Toy&t=VoteUpAndDown

  o-o o             o              o
 /    |             | /            |
O     O--o o-o  o-o OO   o-o o  o -o-
 \    |  | |-' |    | \  | | |  |  |
  o-o o  o o-o  o-o o  o o-o o--o  o



"""

from django.core.exceptions import ObjectDoesNotExist
from applications.startupconfort.forms import BrainTreeFrom
from django.views.generic import FormView

from django import forms
class BraintreeSaleForm(forms.Form):
    payment_method_nonce = forms.CharField()


class ViewCheckoutFormView(FormView):
    template_name = 'startupconfort/pre_checkout_cart.html'
    # success_url = reverse_lazy('startupconfort:my_shopping_cart')
    form_class = BraintreeSaleForm
    http_method_names  = ['post', 'get']

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update stories """
        user = request.user
        if user.cartitem_set.count() < 1:
            messages.warning(request, "You cannot checkout if you have no item in your cart")
            return redirect(reverse_lazy('startupconfort:my_shopping_cart'))
        return super(ViewCheckoutFormView, self).dispatch(request, *args, **kwargs)


    def get_queryset(self):
        user=self.request.user
        return CartItem.objects.filter(customer=user)

    def get_context_data(self, **kwargs):
        context = super(ViewCheckoutFormView, self).get_context_data(**kwargs)
        user = self.request.user
        context['client_token'] = get_braintree_client_token()
        context['title'] = 'Cart'
        number_of_products = CartItem.objects.filter(customer=user).count()
        context['cartitem_list'] = CartItem.objects.filter(customer=user)
        context['total'] = get_total_price_of_the_shipping_cart(user)
        context['breadcrumb'] = 'checkout'
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super(ViewCheckoutFormView, self).form_valid(form)

class SussessfullTemplateView(TemplateView):
    template_name = 'startupconfort/successfull.html'

    def get_context_data(self, **kwargs):
        # import ipdb; ipdb.set_trace()
        context = super().get_context_data(**kwargs)
        context['title'] = 'Successfull'
        context['confirmation'] = '23jds3'
        return context

class BraintreePaymentProcessFormView(FormView):
    template_name = 'startupconfort/cart.html'
    # success_url = reverse_lazy('startupconfort:my_shopping_cart')
    form_class = BraintreeSaleForm
    http_method_names  = ['post', 'get']

    def get_success_url(self):
        return reverse('startupconfort:successfull_payment')

    def get_context_data(self, **kwargs):
        # import ipdb; ipdb.set_trace()
        context = super().get_context_data(**kwargs)
        context['client_token'] = get_braintree_client_token()
        context['breadcrumb'] = 'checkout'
        return context

    def form_invalid(self,form):
        # Add action to invalid form phase
        # import ipdb; ipdb.set_trace()
        messages.success(self.request, 'An error occured while processing the payment --sdfasfd')
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        # import ipdb; ipdb.set_trace()
        user = self.request.user
        nonce = form.cleaned_data['payment_method_nonce']

        result = braintree.Transaction.sale({
            "amount": get_total_price_of_the_shipping_cart(user),
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True
            }
        })

        # import ipdb; ipdb.set_trace()
        if result.is_success or result.transaction:
            print(result.transaction)
            messages.success(self.request, 'Payment proceed successfully')
            # Add Total into db with User Name and Product  + Quantity

            #send email
            user = self.request.user
            billing_email = user.shipping_address.billing_email
            customer_name = user.shipping_address.customer_name
            #total values
            #msg


            from django.core.mail import send_mail
            from postmarker.core import PostmarkClient

            postmark = PostmarkClient(
                server_token='7082cab0-5c69-46f6-9f18-519eb43a1dc0', account_token='66293eea-7445-42d1-b48d-3ad2a6a6f117'
                )

            #Clear Cart
            # CartItem.objects.filter(customer=user).all().delete()
            cartitems = CartItem.objects.filter(customer=user).all()

            total = 8 + sum([item.product.price * item.quantity for item in CartItem.objects.filter(customer=user) ] )




            from .checkout_utils import get_billing_template
            confirmation_number = str(uuid.uuid4())[::5]

            product = CartItem.objects.last().customer
            email = product.shipping_address.billing_email
            country = product.shipping_address.country
            address = product.shipping_address.shipping_address
            username = product.shipping_address.customer_name
            created = product.shipping_address.created

            content = get_billing_template(cartitems, email, username, address, country, confirmation_number, created, total)

            # import ipdb; ipdb.set_trace()
            res = postmark.emails.send(
                From='gmond071@uottawa.ca',
                To='3ioxz1xw.syc@20mm.eu',
                CC='gmond@uottawa.ca',
                Subject='Postmark test',
                HtmlBody=content
            )

            #confirmation number
            Purchase.objects.create(
                owner=user,
                confirmation_number=confirmation_number,
                table=content
                )
            # import ipdb; ipdb.set_trace()
            CartItem.objects.filter(customer=user).all().delete()

            return super().form_valid(form)
        else:
            logger.info('An error occured while processing the payment')
            messages.success(self.request, 'An error occured while processing the payment')
            return super().form_invalid(form)


class BillingView(LoginRequiredMixin,TemplateView):
    template_name = 'billing'

    def get(self, request, *args, **kwargs):
        super(BillingView, self).get(self, request, *args, **kwargs)
        user = request.user
        table = Purchase.objects.filter(owner=user).first().table
        if table:
            return HttpResponse(table)
        messages.success(self.request, 'An error occured  you do not have a Receipt associated with your account')
        return reverse('startupconfort:homepage')
