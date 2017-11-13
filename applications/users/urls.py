from django.conf.urls import url
from applications.users import views as user_views

urlpatterns = [
	url('^register/', user_views.UserRegister.as_view(), name = 'register'),
	url('^login/', user_views.UserLogin.as_view(), name = 'login'),
]
