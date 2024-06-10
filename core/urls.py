from rest_framework import routers
from .views import *
from django.urls import path, include

router = routers.DefaultRouter()
router.register('create_user', CreateUser, basename='create_user')
router.register('create_role', CreateRole, basename='create_role')
router.register('create_ticket', CreateTicket, basename='create_ticket')


urlpatterns = [
    path('', include(router.urls)),

]