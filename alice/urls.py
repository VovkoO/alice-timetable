from django.urls import path, include
from . import views


urlpatterns = [
    path('get_request/', views.get_request, name='get_request'),
    path('', views.home_page, name='home_page')
]
