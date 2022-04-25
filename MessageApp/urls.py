from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'MessageApp'

router = DefaultRouter()
router.register('', views.MessageViewSet, basename='child')

urlpatterns = [
   path('update_message/<int:message_id>/', views.MessageViewSet.as_view({'put': 'update_message'})),
   path('delete_message/<int:message_id>/', views.MessageViewSet.as_view({'delete': 'delete_message'})),
   path('compose/', views.MessageComposeView.as_view()),
   path('reply/<int:headerpk>/', views.MessageReplyView.as_view()),
   path('file/upload/', views.AttachFileUploadView.as_view()),

   path('', include(router.urls))
]
