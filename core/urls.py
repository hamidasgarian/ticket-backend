from rest_framework import routers
from .views import *
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'user', user_view, basename='user')
router.register(r'role', role_view, basename='role')
router.register(r'ticket', ticket_view, basename='ticket')
router.register(r'stadium', stadium_view, basename='stadium')
router.register(r'team', team_view, basename='team')
router.register(r'match', match_view, basename='match')


urlpatterns = [
    path('', include(router.urls)),

]