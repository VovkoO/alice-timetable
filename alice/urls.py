from django.urls import path
from . import views


urlpatterns = [
    path('main/', views.main_page, name='main_page'),
    path('get_request/', views.get_request, name='get_request'),
    path('add_timetable/', views.add_timetable, name='add_timetable'),
    path('timetable/', views.timetable, name='timetable'),
    path('add_lesson/', views.add_lesson, name='add_lesson'),
    path('change_lesson/', views.change_lesson, name='change_lesson'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('', views.home_page, name='home_page')
]
