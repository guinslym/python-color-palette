from django.conf.urls import url, include
from django.contrib.auth.models import User
from django.contrib import admin

from applications.startupconfort.views.checkout import (
    BraintreePaymentProcessFormView,
    ViewCheckoutFormView,
    SussessfullTemplateView,
    BillingView,
)
from applications.startupconfort.views.base import (
    StartupConfortHomePageView,
    StartupProducteDetailView,
    VoteUpOrDownView,
    AboutUs,
)

from applications.startupconfort.views.cart import (
    AddToCartView,
    ShowCartItemsListView,
    CartItemQuantityUpdateView,
    CartItemDeleteView,
)

from applications.startupconfort.views.shipping import (
    ShippingAddressCreateView,
    ShippingAddressUpdateView,
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [

    url(r'^billing/$',
    BillingView.as_view(),
    name='billing'),

    url(r'^checkout/$',
        BraintreePaymentProcessFormView.as_view(),
        name='checkout_braintree'),
    url(r'^successfull_payment/$',
        SussessfullTemplateView.as_view(),
        name='successfull_payment'),


    url(r'^payment_preprocess/$',
        ViewCheckoutFormView.as_view(),
        name='checkout_view'),





    #voteUpOrDown
    url(r'^voteUpOrDown/(?P<slug>[-\w]+)/$',
        VoteUpOrDownView.as_view(),
        name='voteUpOrDown'),

    url(r'^addtocart/(?P<slug>[-\w]+)/$',
        AddToCartView.as_view(),
        name='addProductToCart'),

    url(r'^update_quantity/(?P<pk>\d+)/$',
        CartItemQuantityUpdateView.as_view(),
        name='update_quantity'),
    url(r'^myCart/$',
        ShowCartItemsListView.as_view(),
        name='my_shopping_cart'),

    url(r'^about/$',
        AboutUs.as_view(),
        name='about'),

    url(r'^shipping_address_update/(?P<pk>\d+)/$',
        ShippingAddressUpdateView.as_view(),
        name="shipping_address_update"),
    url(r'^shipping_address_create/$',
        ShippingAddressCreateView.as_view(),
        name='shipping_address_create'),

    url(r'^delete/(?P<pk>\d+)/$',
        CartItemDeleteView.as_view(),
        name="delete_this_item"),
    
    url(r'^(?P<slug>[-\w]+)/$',
        StartupProducteDetailView.as_view(),
        name='product_detail'),
    url(r'^',
        StartupConfortHomePageView.as_view(),
        name='homepage'),
]
