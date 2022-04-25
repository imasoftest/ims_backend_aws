from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'NotificationApp'

router = DefaultRouter()
# router.register('headers', views.NotificationDataViewSet, basename='notification_headers')
# router.register('', views.NotificationRecordListSet, basename='notification')



urlpatterns = [
    # path('', include(router.urls)),
    path('global/',views.NotificationGlobalViewset.as_view({'get': 'list', 'post': 'create'})),
    path('global/<int:pk>/',views.NotificationGlobalViewset.as_view({'get':'retrieve','put':'update','delete':'destroy'})),
    path('getUserNotif/<int:user_id>/',views.NotificationGlobalViewset.as_view({'get': 'getUserNotif'})),
]
