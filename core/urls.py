from rest_framework import routers
from .views import *
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'user', user_view, basename='user')
router.register(r'role', role_view, basename='role')
router.register(r'ticket', ticket_view, basename='ticket')
router.register(r'stadium', stadium_view, basename='stadium')
router.register(r'team', team_view, basename='team')
router.register(r'match', match_view, basename='match')
router.register(r'tools', tools, basename='tools')
router.register(r'capacity', capacity_view, basename='capacity')
router.register(r'capacity', add_veriy_ticket_v2, basename='capacity')


urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
