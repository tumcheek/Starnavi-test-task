from django.urls import path
from rest_framework import routers

from . import views

app_name = 'social_network'

router = routers.SimpleRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'analytics', views.AnalyticsViewSet)

urlpatterns = [
    path('users/', views.UserAPIView.as_view(), name='users'),
    path('user-activity/', views.UserActivityAPIView.as_view(), name='user-activity'),
]

urlpatterns += router.urls

