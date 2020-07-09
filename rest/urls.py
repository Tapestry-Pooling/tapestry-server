from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('lab', views.LabViewSet)
router.register('labmember', views.LabMemberViewSet)


urlpatterns = [
    path('',include(router.urls))
]