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
from applications.startupconfort.models import Category

from applications.startupconfort.forms import CartItemQuantityForm

from django.contrib.auth.models import User

from hitcount.models import HitCount
from hitcount.views import HitCountDetailView

import braintree

# url(r'^$', HomePageView.as_view(), name='home'),
class StartupConfortHomePageView(TemplateView):

    template_name = "startupconfort/home.html"

    def get_context_data(self, **kwargs):
        logger.info('homepage')
        context = super(StartupConfortHomePageView, self).get_context_data(**kwargs)
        context['products'] = StartupProduct.objects.all()[:3]
        products = StartupProduct.objects.select_related('category')
        #pillow
        pillow = Category.objects.filter(title='Pillow')
        context['pillows'] = products.filter(category=pillow)[:3]
        #tie
        tie = Category.objects.filter(title='Tie')
        context['ties'] = products.filter(category=tie)[:3]
        #pillow
        tpillow = Category.objects.filter(title='Travel Pillow')
        context['tpillows'] = products.filter(category=tpillow)[:3]
        return context

# url(r'^(?P<slug>[-\w]+)/$', ArticleDetailView.as_view(), name='article-detail'),
class StartupProducteDetailView(HitCountDetailView):

    model = StartupProduct
    count_hit = True
    template_name = "startupconfort/detail.html"

    def get_context_data(self, **kwargs):
        context = super(StartupProducteDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Detail'
        product = self.object
        context['colors'] = product.startup.brand_color.all()
        context['colors'] = ["#" + color.color for color in context['colors'] ]
        # import ipdb; ipdb.set_trace()
        return context


class AboutUs(TemplateView):
    template_name = "startupconfort/about.html"

    def get_context_data(self, **kwargs):
        context = super(AboutUs, self).get_context_data(**kwargs)
        context['title'] = "About us"
        return context




"""
tinker-toy
http://patorjk.com/software/taag/#p=display&f=Tinker-Toy&t=VoteUpAndDown


o   o      o      o   o        O          o o-o
|   |      |      |   |       / \         | |  \
o   o o-o -o- o-o |   | o-o  o---oo-o   o-O |   O o-o o   o   oo-o
 \ /  | |  |  |-' |   | |  | |   ||  | |  | |  /  | |  \ / \ / |  |
  o   o-o  o  o-o  o-o  O-o  o   oo  o  o-o o-o   o-o   o   o  o  o
                        |
                        o

"""

class VoteUpOrDownView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(StartupProduct, slug=kwargs['slug'] )
        user_id = request.user.id
        #import ipdb; ipdb.set_trace()
        if product in StartupProduct.votes.all(user_id):
            product.votes.delete(user_id)
            messages.success(request, 'We deleted your Like')
            return HttpResponse('Deleted your vote')
            # return redirect(reverse('wadiyabi:product_detail',kwargs={'slug':kwargs['slug']}))
        else:
            product.votes.up(user_id)
            messages.success(request, 'Thanks for liking my StartupProduct')
            return HttpResponse('Added your vote')
            # return redirect(reverse('wadiyabi:product_detail',kwargs={'slug':kwargs['slug']}))


def handler404(request):
    response = render(request, 'robots_and_errors/page_not_found.html')
    logger.info('Error page not found 404')
    response.status_code = 404
    return response

def handler500(request):
    response = render(request, 'robots_and_errors/server_error.html')
    logger.info('Error page not found 500')
    response.status_code = 500
    return response
