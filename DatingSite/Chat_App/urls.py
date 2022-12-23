from . import views
from django.urls import path

app_name = 'Chat_App'
urlpatterns = [
    path('', views.chathome, name='chathome'),
    path('<str:withuser>/', views.chatpage, name='chatpage'),
]