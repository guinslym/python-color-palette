from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, \
                                 UpdateView, RedirectView

from applications.brandcolors.models import Fabric
from applications.brandcolors.models import StartupColor
from applications.brandcolors.forms import FabricForm, HexcodeForm
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse

class HomeListView(ListView):
    template_name = "fabric/fabric_home.html"
    model = Fabric


class HomeRedirectView(RedirectView):
    url = reverse_lazy('brandcolors:homepage')


import webcolors

import math

from colorthief import ColorThief

def distance(color1, color2):
    return math.sqrt(sum([(e1-e2)**2 for e1, e2 in zip(color1, color2)]))


def best_match(sample, colors):
    by_distance = sorted(colors, key=lambda c: distance(c, sample))
    return by_distance[0:5]

from django.conf import settings

class FabricDetailView(DetailView):
    template_name = "fabric/fabric.html"
    model = Fabric

    def get_context_data(self, **kwargs):
        context = super(FabricDetailView, self).get_context_data(**kwargs)
        context['list_of_colors'] = list(StartupColor.objects.values_list('color', flat=True))
        context['list_of_colors'] = set(context['list_of_colors'])
        picture = self.object
        color_thief = ColorThief(settings.BASE_DIR + picture.picture.url)
        # get the dominant color
        dominant_color = color_thief.get_color(quality=1)
        # build a color palette
        palette = color_thief.get_palette(color_count=10)

        context['dominant_color'] = webcolors.rgb_to_hex(dominant_color)
        palette = [webcolors.rgb_to_hex(color) for color in palette]
        context['palette_dominant_color'] = palette

        # import pdb; pdb.set_trace()
        rgb_list_of_colors = [webcolors.hex_to_rgb(color) for color in context['list_of_colors'] ]
        result = best_match(dominant_color, rgb_list_of_colors )
        brandcolors = [webcolors.rgb_to_hex(color) for color in result]
        context['brandcolors'] = brandcolors
        # import ipdb; ipdb.set_trace()
        return context


def find_color_of_our_database():
    list_of_colors = list(StartupColor.objects.values_list('color', flat=True))
    list_of_colors = set(list_of_colors)
    return list_of_colors

class ThemeView(TemplateView):
    template_name='fabric/theme.html'

    def get_context_data(self, **kwargs):
        context = super(ThemeView, self).get_context_data(**kwargs)
        # import pdb; pdb.set_trace()
        color = '#'+kwargs.get('color')
        # color = '#974d4c'
        context['color'] = color
        color = webcolors.hex_to_rgb(color)
        #Find startup that has a color theme close to kwargs['color']
        list_of_colors = find_color_of_our_database()
        rgb_list_of_colors = [ webcolors.hex_to_rgb(color) for color in list_of_colors ]

        result = best_match(color, rgb_list_of_colors )
        brandcolors = [webcolors.rgb_to_hex(color) for color in result]
        context['brandcolors'] = brandcolors

        startup = StartupColor.objects.filter(color=brandcolors[0]).first()
        startups = list()
        for color in brandcolors:
            this_startup = StartupColor.objects.filter(color=color).first().startup
            startups.append(
                {'startup': this_startup.title,  'number':this_startup.brand_color.count(),
                 'colors':this_startup.brand_color.all()
                 })

        context['startups'] = startups

        return context


class FabricCreateView(CreateView):
    template_name = "fabric/fabric_create.html"
    form_class = FabricForm

    def form_valid(self, form):
        """
        Assign the author to the request.user
        """
        form.instance.author = self.request.user
        return super(FabricCreateView, self).form_valid(form)


class FabricDeleteView(DeleteView):
    model = Fabric
    success_url = reverse_lazy('brandcolors:homepage')


class FabricUpdateView(UpdateView):
    template_name = "fabric/fabric_update.html"
    model = Fabric
    form_class = FabricForm
