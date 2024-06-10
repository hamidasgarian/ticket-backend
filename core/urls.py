from rest_framework import routers
from .views import *
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'user', User, basename='user')
router.register(r'role', Role, basename='role')
router.register(r'ticket', Ticket, basename='ticket')


urlpatterns = [
    path('', include(router.urls)),

]