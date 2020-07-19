from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'lab', views.LabViewSet)
router.register(r'machine-type', views.MachineTypeViewset)
router.register(r'test-kit', views.TestKitViewset)
router.register(r'lab-configuration', views.LabConfigurationViewset)
router.register(r'test', views.TestViewset)
router.register(r'status', views.StatusViewset)
router.register(r'matrix',views.MatrixViewset)
router.register(r'file', views.FileViewset)
router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
