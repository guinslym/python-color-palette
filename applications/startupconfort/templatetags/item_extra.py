from django import template
import datetime
from applications.startupconfort.models import CartItem
#https://github.com/guinslym/mywadiyabi/blob/master/applications/wadiyabi/templatetags/registration.py


register = template.Library()



@register.filter
def replace_commas(string):
    return string.replace(',', '_')



@register.simple_tag
def get_total_for_this_cart(items):
    # import ipdb; ipdb.set_trace()
    try:
        user = items.first().customer
    except:
        return ("{0:.2f}".format(0))
    number_of_products = CartItem.objects.filter(customer=user).count()
    if (number_of_products > 0):
        total = 8 + sum([item.product.price * item.quantity for item in CartItem.objects.filter(customer=user) ] )
    else:
        total = 0
    return ("{0:.2f}".format(total))
