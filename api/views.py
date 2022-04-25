from django.conf import settings
from NotificationApp.models import NotificationModel
from UserApp.models import User
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import permissions, status, viewsets, mixins
from rest_framework.response import Response
from anam_backend_main import mypermissions
from pdb import set_trace as bp
import os
from anam_backend_main.constants import Classroom, All, Admin
import datetime
from .models import SchoolDocument, MiniClub, ExchangeLibrary, BookStatus, Marketing
from .serializers import UploadSerializer, SchoolDocumentUploadSerializer, SchoolDocumentSerializer,\
    MiniClubSerializer, ExchangeLibrarySerializer, MarketingReadSerializer, MarketingWriteSerializer,\
    RegisterChildMiniClubSerializer, UnRegisterChildMiniClubSerializer
from NotificationApp.utils import send_broadcast
# Create your views here.
from django.core.files.storage import default_storage
from ChildApp.models import Child
import json

@api_view(['POST'])
# @permission_classes((permissions.IsAuthenticated,))
def uploadPicture(request):

    serializer = UploadSerializer(request.POST, request.FILES)
    if serializer.is_valid():
        #  Saving POST'ed file to storage
        file = request.FILES['file']
        file_name = default_storage.save(file.name, file)
        file = default_storage.open(file_name)
        file_url = default_storage.url(file_name)
        return Response(file_url)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def write_uploaded_file(f):
    media_root = settings.MEDIA_ROOT
    datestr = datetime.datetime.today().strftime("%d-%m-%y-%H-%M-%S")
    with open(os.path.join(r'/home/ubuntu/IMSBackend/upload/pictures/',f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return os.path.join(r'/home/ubuntu/IMSBackend/upload/pictures/',f.name)


@api_view(['POST'])
# @permission_classes((permissions.IsAuthenticated, mypermissions.IsAdminRole))
def uploadSchoolDocument(request, documentFor=All):
    
    if 'classRoom_names' in request.data:
        classRoom_names = json.loads(request.data['classRoom_names'])
        for classroom_name in classRoom_names:
            print(classroom_name)
            # save notification for all parents with classroom
            parent_id_list = list(Child.objects.filter(nameOfClass = classroom_name).values('parent_id'))
            for parent in parent_id_list:
                user_id = parent['parent_id']
                data = {
                    "notificationMessage":f"New School document got added",
                    "module":"School-Document",
                    "user":User.objects.get(id=user_id)
                }
                NotificationModel(**data).save()

            serializer = SchoolDocumentUploadSerializer(data={"url" : request.data['url']})
            if serializer.is_valid():
                f = request.FILES['url']
                serializer.save(name=f.name, documentfor=classroom_name)
        return Response('Documents added successfully')
    
    elif 'parent_ids' in request.data:
        for parent_id in request.data['parent_ids']:
            # save notification
            data = {
            "notificationMessage":f"New School document got added",
            "module":"School-Document",
            "user":User.objects.get(id=parent_id)
            }
            NotificationModel(**data).save()

            serializer = SchoolDocumentUploadSerializer(data=request.data['url'])
            if serializer.is_valid():
                f = request.FILES['url']
                serializer.save(name=f.name, documentfor=parent_id)
        return Response('Documents added successfully')
    
    parent_id_list = list(User.objects.all().values('id'))
    for parent in parent_id_list:
        user_id = parent['id']
        data = {
                    "notificationMessage":f"New School document got added",
                    "module":"School-Document",
                    "user":User.objects.get(id=user_id)
                }
        NotificationModel(**data).save()

    serializer = SchoolDocumentUploadSerializer(data=request.data)
    if serializer.is_valid():
        f = request.FILES['url']
        serializer.save(name=f.name, documentfor=documentFor)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SchoolDocumentViewSet(viewsets.ReadOnlyModelViewSet, mixins.DestroyModelMixin):
    queryset = SchoolDocument.objects.all()
    serializer_class = SchoolDocumentSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def destory(self, request, *args, **kwargs):
        if request.user.role != Admin:
            return Response("You don't have enough permission", status=status.HTTP_400_BAD_REQUEST)
        return super().destory(request, *args, **kwargs)


class MiniClubViewSet(viewsets.ModelViewSet):
    queryset = MiniClub.objects.order_by('-date')
    serializer_class = MiniClubSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def destory(self, request, *args, **kwargs):
        if request.user.role.name != Admin:
            return Response("You don't have enough permission", status=status.HTTP_400_BAD_REQUEST)
        return super().destory(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path="thisweek")
    def get_thisweek_club(self, request):
        first_day_of_week = datetime.datetime.today() - datetime.timedelta(days=datetime.datetime.today().isoweekday() % 7)
        clubs = MiniClub.objects.filter(date__gte=first_day_of_week).order_by('date')
        serializer = MiniClubSerializer(
            clubs, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path="unregister")
    def remove_siblings_from_club(self, request, pk=None):
        club = self.get_object()
        serializer = UnRegisterChildMiniClubSerializer(data=request.data)
        if serializer.is_valid():
            child = serializer.validated_data.get('child')
            club.children.remove(*child.sibling_group.childs.all())
            club_serializer = MiniClubSerializer(club, context=self.get_serializer_context())
            return Response(club_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path="register")
    def addChildToClub(self, request, pk=None):
        club = self.get_object()
        serializer = RegisterChildMiniClubSerializer(
            data=request.data, context=self.get_serializer_context())
        if serializer.is_valid():
            child = serializer.validated_data.get('child')
            children = club.children.all()
            if child not in children:
                club.children.add(child)
                club.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        send_broadcast()
        return response

    def update(self, request, pk, **kwargs):
        data = request.data
        response = MiniClub.objects.filter(id = pk).update(**data)
        return Response('updated Successfully')

class ExchangeLibraryViewSet(viewsets.ModelViewSet):
    # def update(self, request, *args, **kwargs):
    #     bp( )
    queryset = ExchangeLibrary.objects.order_by('title').all()
    serializer_class = ExchangeLibrarySerializer
    permission_classes = (permissions.IsAuthenticated,)
    # def create(self, request, *args, **kwargs):
    #     format = '%Y-%m-%d'
    #     request.data.get('booked_on') = datetime.datetime.strptime(request.data.get('booked_on'), format)
    #     request.data.get('returned_on') = datetime.datetime.strptime(request.data.get('returned_on'), format)

    def destory(self, request, *args, **kwargs):
        if request.user.role != Admin:
            return Response("You don't have enough permission", status=status.HTTP_400_BAD_REQUEST)
        return super().destory(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path="rentBook")
    def rent_book(self, request, pk=None):
        child_id = request.data['child_id']
        book = self.get_object()
        if book.status == BookStatus.RENTED:
            return Response("Already Rented By Another User", status=status.HTTP_400_BAD_REQUEST)
        book.status = BookStatus.RENTED
        book.booked_status = True
        # book.child = request.user.child
        children = Child.objects.get(parent=request.user,id=child_id)
        book.child = children
        if 'returned_on' not in request.data:
            book.returned_on = None
        book.save()
        serializer = ExchangeLibrarySerializer(
            book, context=self.get_serializer_context())
        return Response(serializer.data)


class MarketingViewSet(viewsets.ModelViewSet):
    queryset = Marketing.objects.order_by('-created_at').all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return MarketingReadSerializer
        else:
            return MarketingWriteSerializer
