from django.urls import path, include
from . import views


urlpatterns = [
    path('get_request/', views.get_request, name='get_request'),
    path('add_timetable/', views.add_timetable, name='add_timetable'),
    path('timetable/', views.timetable, name='timetable'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.home_page, name='home_page')
]
