from django.contrib import admin
from django.urls import path

from user.views import UserView, LoginView

urlpatterns = [
    path('api/register/', UserView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
]
