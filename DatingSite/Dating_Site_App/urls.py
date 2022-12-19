from . import views
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
# from .views import EditPage


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', TemplateView.as_view(template_name="Dating_Site_App/login.html"), name='login'),
    path('accounts/', include('allauth.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('messageRequests/', views.messageRequests, name='messagerequestspage'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/edit/', views.editProfile, name='editpage'),
    # path('friendship/', include('friendship.urls')),
    path('blockUser/<str:touser>/', views.blockUser, name='blockuser'),
    path('sendMessageRequest/<str:touser>/', views.sendMessageRequest, name='sendmessagerequest'),
    path('respondMessageRequest/<str:fromuser>/<str:response>', views.respondMessageRequest, name='respondmessagerequest'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)