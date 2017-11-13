from django.contrib import admin

# Register your models here.


from applications.startupconfort.models import Startup
from applications.startupconfort.models import StartupProduct
from applications.startupconfort.models import StartupColor
from applications.startupconfort.models import Category
from applications.startupconfort.models import Gallery
from applications.startupconfort.models import StartupProductImage
from applications.startupconfort.models import CartItem

class StartupAdmin(admin.ModelAdmin):
    pass

class StartupColorAdmin(admin.ModelAdmin):
    pass

class StartupProductAdmin(admin.ModelAdmin):
    pass

class StartupProductImageAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class GalleryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Startup, StartupAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(StartupColor, StartupColorAdmin)
admin.site.register(StartupProduct, StartupProductAdmin)
admin.site.register(StartupProductImage, StartupProductImageAdmin)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(Startup, StartupAdmin)
