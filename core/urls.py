from rest_framework import routers
from .views import *
from django.urls import path, include

router = routers.DefaultRouter()
router.register('user', User, basename='user')
router.register('role', Role, basename='role')
router.register('ticket', Ticket, basename='ticket')


urlpatterns = [
    path('', include(router.urls)),

]