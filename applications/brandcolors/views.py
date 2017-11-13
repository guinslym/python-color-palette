from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, \
                                 UpdateView, RedirectView

from applications.brandcolors.models import Fabric
from applications.brandcolors.forms import FabricForm


class HomeListView(ListView):
    template_name = "fabric/fabric_home.html"
    model = Fabric


class HomeRedirectView(RedirectView):
    url = reverse_lazy('brandcolors:homepage')


class FabricDetailView(DetailView):
    template_name = "fabric/fabric.html"
    model = Fabric


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
