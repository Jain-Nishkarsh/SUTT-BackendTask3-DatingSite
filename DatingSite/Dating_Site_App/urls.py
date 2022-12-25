from . import views
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
# from .views import EditPage


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', TemplateView.as_view(template_name="Dating_Site_App/login.html"), name='login'),
    path('accounts/', include('allauth.urls')),
    path('modLoginPage/', TemplateView.as_view(template_name="Dating_Site_App/modlogin.html"), name='modLoginPage'),
    path('modLogin/', views.modLogin, name='modlogin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('messageRequests/', views.messageRequests, name='messagerequestspage'),
    path('blocklist/', views.blocklist, name='blocklist'),
    path('allmatches/', views.allmatches, name='allmatches'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/edit/', views.editProfile, name='editpage'),
    path('blockUser/<str:touser>/', views.blockUser, name='block'),
    path('unblockUser/<str:touser>/', views.unblockUser, name='unblock'),
    path('unmatch/<str:touser>/', views.Unmatch, name='unmatch'),
    path('report/<str:reportee>/', views.Report, name='report'),
    path('reportPage/<str:reportee>/', views.ReportPage, name='reportPage'),
    path('sendMessageRequest/<str:touser>/', views.sendMessageRequest, name='sendmessagerequest'),
    path('unsendMessageRequest/<str:touser>/', views.unsendMessageRequest, name='unsendmessagerequest'),
    path('respondMessageRequest/<str:fromuser>/<str:response>', views.respondMessageRequest, name='respondmessagerequest'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)