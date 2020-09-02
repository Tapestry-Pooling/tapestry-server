from django.urls import path, include, re_path
from rest_framework_nested import routers
from django.conf.urls import url
from . import views
from django.views.generic import TemplateView
from rest_framework_jwt.views import refresh_jwt_token

from rest_auth.registration.views import VerifyEmailView, RegisterView
from rest_auth.views import (
    PasswordResetView, PasswordResetConfirmView
)

router = routers.SimpleRouter()

router.register(r'lab', views.LabViewSet)
router.register(r'machine-type', views.MachineTypeViewset)
router.register(r'test-kit', views.TestKitViewset)
router.register(r'lab-configuration', views.LabConfigurationViewset)
router.register(r'test', views.TestViewSet)
router.register(r'status', views.StatusViewset)
router.register(r'matrix',views.MatrixViewset)
router.register(r'file', views.FileViewset)
router.register(r'user', views.UserViewSet)
router.register(r'city', views.CityViewSet)
router.register(r'country', views.CountryViewSet)

lab_router = routers.NestedSimpleRouter(router, r'lab', lookup='lab')
lab_router.register(r'member', views.LabMemberViewSet, basename='lab-member')
lab_router.register(r'test', views.LabTestViewSet, basename='lab-test')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(lab_router.urls)),
    url(r'^auth/login/$', views.LoginView.as_view(), name='rest_login'),
    url(r'^auth/password/reset/$', views.PasswordResetView.as_view(),
        name='rest_password_reset'),
    url(r'^auth/password/reset/confirm/$', views.PasswordResetConfirmView.as_view(),
        name='rest_password_reset_confirm'),
    url(r'^auth/login/$', views.LoginView.as_view(), name='rest_login'),
    # URLs that require a user to be logged in with a valid session / token.
    url(r'^auth/logout/$', views.LogoutView.as_view(), name='rest_logout'),
    url(r'^user/$', views.UserDetailsView.as_view(), name='rest_user_details'),
    url(r'^auth/password/change/$', views.PasswordChangeView.as_view(),
        name='rest_password_change'),

    url(r'^auth/register/', views.RegisterView.as_view(), name='rest_register'),
    # url(r'^auth/verify-email/$', views.VerifyEmailView.as_view(), name='rest_verify_email'),

    url(r'^auth/account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(),
        name='account_confirm_email'),

    url(r'^auth/refresh/', refresh_jwt_token),
    url(r'^inactive', views.inactive_view, name='account_inactive'),
    
    re_path(r'^account-confirm-email/', VerifyEmailView.as_view(),
     name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(),
     name='account_confirm_email'),

    path('test/<int:id>/upload/', views.UploadUrlView.as_view(), name='upload_url'),

    url(r'^', include('django.contrib.auth.urls')),
]
