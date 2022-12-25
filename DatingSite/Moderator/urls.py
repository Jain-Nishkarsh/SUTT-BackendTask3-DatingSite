from . import views
from django.urls import path

app_name = 'Moderator'
urlpatterns = [
    path('', views.modHome, name='modhome'),
    path('ignoreReport/<int:reportID>/', views.ignoreReport, name='ignoreReport'),
    path('userAdminPage/<str:reportee>/', views.redirectAdminUser, name='userAdminPage'),
]