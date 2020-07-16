from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api/lab', views.LabViewSet)
router.register(r'api/labmember', views.LabMemberViewSet)
router.register(r'api/machine-type', views.MachineTypeViewset)
router.register(r'api/test-kit', views.TestKitViewset)
router.register(r'api/lab-configuration', views.LabConfigurationViewset)
router.register(r'api/test', views.TestViewset)
router.register(r'api/status', views.StatusViewset)
router.register(r'api/matrix',views.MatrixViewset)
router.register(r'api/file', views.FileViewset)

urlpatterns = [
    path('', include(router.urls)),
]
