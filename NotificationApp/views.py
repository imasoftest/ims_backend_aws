from django.shortcuts import render
from .serializers import NotificationStatusRecordSerializer, NotificationReadSerializer, NotificationWriteSerializer, NotificationReceiverSerializer,NotificationGlobalSerializer
from .models import Notification, NotificationStatusRecord, NotificationModel
from rest_framework.decorators import action
from rest_framework import permissions, viewsets
from pdb import set_trace as bp
from rest_framework.response import Response
from UserApp.models import User, ClassData
from ChildApp.models import Child
from anam_backend_main import mypermissions
# Create your views here.


# class NotificationRecordListSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = NotificationStatusRecordSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#     filterset_fields = ['is_read']

#     def get_queryset(self):
#         user = self.request.user
#         return user.received_notification_status.all()


# class NotificationDataViewSet(viewsets.ModelViewSet):
#     permission_classes = (permissions.IsAuthenticated, mypermissions.IsAdminRole)

#     def get_queryset(self):
#         user = self.request.user
#         return user.sent_notifications.order_by('-created_at').all()

#     def get_serializer_class(self):
#         user = self.request.user.id
#         if 'sender' not in self.request.data:
#             self.request.data['sender'] = user
#         if self.action == 'list' or self.action == 'retrieve':
#             return NotificationReadSerializer
#         else:
#             return NotificationWriteSerializer

#     @action(detail=True, url_path='receivers')
#     def getReceivers(self, request, pk=None):
#         instance = self.get_object()
#         serializer = NotificationReceiverSerializer(instance.notification_status_list.all(), many=True, context=self.get_serializer_context())
#         return Response(serializer.data)

class NotificationGlobalViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = NotificationModel.objects.all()
    serializer_class = NotificationGlobalSerializer

    def create(self, request, *args, **kwargs):
        # request.data['user'] = request.user.id
        if 'classroom_id' in request.data:
            classroom_ids = request.data['classroom_id']
            for classroom_id in classroom_ids:
                className = ClassData.objects.filter(id =classroom_id ).values('name').get()['name']
                parent_id_list = list(Child.objects.filter(nameOfClass = className).values('parent_id'))
                for parent in parent_id_list:
                    user_id = parent['parent_id']
                    data = {
                        "notificationMessage":request.data['notificationMessage'],
                        "module":"General",
                        "user":User.objects.get(id=user_id)
                        }
                    NotificationModel(**data).save()
            return Response("Notifications sent successfully.")
        
        elif 'user_ids' in request.data:
            for user_id in request.data['user_ids']:
                data = {
                        "notificationMessage":request.data['notificationMessage'],
                        "module":"General",
                        "user":User.objects.get(id=user_id)
                        }
                NotificationModel(**data).save()
            return Response("Notifications sent successfully")
            
        else:
            return super().create(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        data = NotificationModel.objects.all()
        return Response(data=NotificationGlobalSerializer(data, many=True).data)
    
    def getUserNotif(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        data = NotificationModel.objects.filter(user_id=user_id).order_by('-created_at')
        return Response(data=NotificationGlobalSerializer(data, many=True).data)

    def update(self, request, *args, **kwargs):
        try:
            is_read = request.data['is_read']
            if is_read :
                NotificationModel.objects.filter(id=kwargs['pk']).update(is_read=is_read)
            return Response("successfully updated") 
        except Exception as e:
            return Response(str(e))
    
    def destroy(self, request, *args, **kwargs):
        try:
            NotificationModel.objects.filter(id=kwargs['pk']).delete()
            return Response('Notification got deleted successfully')
        except Exception as e:
            return Response(str(e))