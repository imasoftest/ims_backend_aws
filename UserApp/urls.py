from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as token_views
from . import views

app_name = 'UserApp'

router = DefaultRouter()
router.register('', views.UserViewSet, basename='user')

urlpatterns = [
    # URLs for managing the roles
    path('roles/', views.RoleViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('roles/<int:pk>/', views.RoleViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # URLs for managing the roles
    path('classes/', views.ClassViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('classes/<int:pk>/', views.ClassViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # URLs for managing the Nationalities
    path('nationalities/', views.NationalityViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('nationalities/<int:pk>/', views.NationalityViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('login/', token_views.obtain_auth_token),
    path('', include(router.urls)),
    

]
