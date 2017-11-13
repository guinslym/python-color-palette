from django.conf.urls import url, include
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.conf import settings

from applications.brandcolors.views import HomeRedirectView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include("applications.brandcolors.urls", namespace='brandcolors')),
]


# Use static() to add url mapping to serve static files during development (only)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
