from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'lab', views.LabViewSet)
router.register(r'machine-type', views.MachineTypeViewset)
router.register(r'test-kit', views.TestKitViewset)
router.register(r'lab-configuration', views.LabConfigurationViewset)

urlpatterns = [
    path('', include(router.urls)),
]
