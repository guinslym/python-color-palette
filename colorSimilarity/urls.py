from django.conf.urls import url, include
from django.contrib import admin

from applications.brandcolors.views import HomeRedirectView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include("applications.brandcolors.urls", namespace='brandcolors')),
]
