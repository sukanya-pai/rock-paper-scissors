from django.urls import path
from . import views


urlpatterns = [
    path('home', views.home, name='home'),
        path('start/', views.game, name='game_inputs'),

    path('result/', views.result, name='result'),
]