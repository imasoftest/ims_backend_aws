from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'ChildApp'

router = DefaultRouter()
router.register('', views.ChildViewSet, basename='child')

urlpatterns = [
    path('privacyRights/', views.PrivacyRightsViewset.as_view({'get': 'list', 'post': 'create','put':'update'})),
    path('privacyRights/<int:pk>/', views.PrivacyRightsViewset.as_view({'put':'update','delete':'destroy'})),
    path('sibling/pictures/', views.MyPictureViewSet.as_view()),
    path('sibling/pictures/<int:pk>/', views.MyPictureViewSet.as_view()),
    path('deletePicture/<int:id>/',views.ChildPictureViewset.as_view({'delete':'destroy'})),
    path('', include(router.urls)),

    path('sibling/<int:pk>/add/', views.add_child_to_sibling_group)
]
