import json
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions, generics
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from pdb import set_trace as bp
import os
from NotificationApp import utils as notfication_utils
from anam_backend_main import mypermissions
from anam_backend_main.constants import Admin, Parent, Teacher
from .models import Child, PrivacyRights, SiblingGroup, Food, MenuItem, ChildDailyInformation, Picture, Contact, AuthPerson
from .serializers import ChildDailyInformationWriteSerializer, ChildDailyInformationReadSerializer, PrivacyRightsSrializer
from .serializers import ChildSerializer, PictureSerializer, FoodSerializer, MenuItemSerializer, AddFoodSerializer,AuthPersonSerializer

import io, base64
from PIL import Image

from ChildApp import serializers

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ChildViewSet(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ['nameOfClass']

    def create(self, request, *args, **kwargs):
        request.data['nationality'] = json.dumps(request.data['nationality'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        serializer.data['nationality'] = json.loads(request.data['nationality'])
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request,pk = None, *args, **kwargs):
        # instance = self.get_object()
        instance = Child.objects.get(id=pk)
        for key, value in request.data.items():
            if key == "photoFile":
                instance.photoFile = value
            if key == "first_name":
                instance.first_name = value
            if key == "last_name":
                instance.last_name = value
            if key =="gender":
                instance.gender = value
            if key =="address":
                instance.address = value
            if key == "nameOfClass":
                instance.nameOfClass = value
            if key =="firstNameOfMother":
                instance.firstNameOfMother = value
            if key =="lastNameOfMother":
                instance.lastNameOfMother = value
            if key == "phoneOfMother":
                instance.phoneOfMother = value
            if key == "emailOfMother":
                instance.emailOfMother = value
            if key == "firstNameOfFather":
                instance.firstNameOfFather = value
            if key == "lastNameOfFather":
                instance.lastNameOfFather = value
            if key == "phoneOfFather":
                instance.phoneOfFather = value
            if key == "emailOfFather":
                instance.emailOfFather = value
            if key == "isFatherNone":
                instance.isFatherNone = value
            if key == "isMotherNone":
                instance.isMotherNone = value
            if key == "allgeries":
                instance.allgeries = value
            if key == "food_restriction":
                instance.food_restriction = value
            if key == "health_issue":
                instance.health_issue = value
            if key == "flag_video":
                instance.flag_video = value
            if key == "flag_facebook":
                instance.flag_facebook = value
            if key == "flag_newsletter":
                instance.flag_newsletter = value
            if key == "flag_friday_letter":
                instance.flag_friday_letter = value
            if key == "flag_internet_sites":
                instance.flag_internet_sites = value
            if key == "flag_yearbook":
                instance.flag_yearbook = value
            if key == "flag_flyer":
                instance.flag_flyer = value
            if key == "flag_magazine":
                instance.flag_magazine = value
            if key == "flag_instagram":
                instance.flag_instagram = value
            if key == "flag_re_enrollment":
                instance.flag_re_enrollment = value
            if key == "flag_responsibility_discharge":
                instance.flag_responsibility_discharge = value
            if key == "flag_image_rights":
                instance.flag_image_rights = value
            if key == "flag_health_protocols":
                instance.flag_health_protocols = value
            if key == "flag_fin_contract":
                instance.flag_fin_contract = value
            if key == "flag_interieur_rules":
                instance.flag_interieur_rules = value
            if key == "nationality":
                instance.nationality = json.dumps(value)
            if key == "siblings":
                instance.siblings = json.dumps(value)
            if key == "birth":
                instance.birth = value
            if key == "emergencyContacts":
                for i in value:
                    id_ = i['id']
                    name = i['name']
                    email = i['email']
                    phone_number = i['phone_number']
                    if id_ is not None:
                        Contact.objects.filter(child_id=pk,id = id_).update(name=name,email=email,phone_number=phone_number)
                    else:
                        Contact.objects.create(child_id=pk,name=name,email=email,phone_number=phone_number)
            if key == "authPersons":
                for i in value:
                    id_ = i['id']
                    first_name = i['first_name']
                    last_name = i['last_name']
                    phone_number = i['phone_number']
                    if 'photo' in i:
                        image_b64 = i['photo'] # This is your base64 string image
                        format, imgstr = image_b64.split(';base64,')
                        ext = format.split('/')[-1]
                        photo_path = f'upload/photo/authPerson_{id_}.{ext}'
                        img = Image.open(io.BytesIO(base64.decodebytes(bytes(imgstr, "utf-8"))))
                        img.save(photo_path)
                        if id_ is not None:
                            AuthPerson.objects.filter(child_id=pk,id = id_).update(photo = photo_path, first_name=first_name,last_name=last_name,phone_number=phone_number)
                        else:
                            AuthPerson.create(child_id=pk,photo = photo_path, first_name=first_name,last_name=last_name,phone_number=phone_number)
                    else:
                        if id_ is not None:
                            AuthPerson.objects.filter(child_id=pk,id = id_).update(first_name=first_name,last_name=last_name,phone_number=phone_number)
                        else:
                            AuthPerson.objects.create(child_id=pk,first_name=first_name,last_name=last_name,phone_number=phone_number)
            if key == "photo":
                # instance.photo = value
                image_b64 = value # This is your base64 string image
                format, imgstr = image_b64.split(';base64,')
                ext = format.split('/')[-1]
                photo_path = f'upload/child_{pk}.{ext}'
                img = Image.open(io.BytesIO(base64.decodebytes(bytes(imgstr, "utf-8"))))
                img.save(photo_path)
                instance.photo = photo_path

            if key == "privacyRights":
                instance.privacyRights = value

            instance.save()

        return Response('Update Successful')

    def get_queryset(self):
        if self.request.user.role.name == Admin:
            return Child.objects.all().order_by('first_name')
        else:
            user = self.request.user
            try:
                if user.role.name == Teacher:
                    clssnameList = json.loads(user.classnames)
                    query = Q(nameOfClass=clssnameList[0])
                    for classname in clssnameList:
                        query = query | Q(nameOfClass=classname)
                    if 'nameOfClass' in self.request.GET:
                        return Child.objects.filter(nameOfClass=self.request.GET['nameOfClass'])
                    return Child.objects.filter(query)
                    
                    
                if user.role.name == Parent:
                    return user.child.sibling_group.childs
            except Exception:
                return Child.objects.none()

    @action(detail=True, methods=['post'])
    def remove_from_sibling(self, request, pk=None):
        child = self.get_object()
        prev_group_id = child.sibling_group.id
        sibling_group = SiblingGroup.objects.filter(numberOfSiblings=0).first()
        if not sibling_group:
            sibling_group = SiblingGroup()
            sibling_group.save()
        sibling_group.numberOfSiblings -= 1
        sibling_group.save()

        child.sibling_group = sibling_group
        child.save()
        notfication_utils.change_parent_sibling_group(prev_group_id, child.parent)
        return Response(sibling_group.pk)

    @action(detail=True, methods=['post'])
    def upload_picture(self, request, pk=None):
        child = self.get_object()
        serializer = PictureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(receiver = child)
            image = request.data['image']
            with open(os.path.join(BASE_PATH,image.name),'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)
            return Response("Success")
        else:
            return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def pictures(self, request, pk=None):
        child = self.get_object()
        child_serializer = ChildSerializer(
            child, context=self.get_serializer_context())
        serializer = PictureSerializer(
            child.pictures, many=True, context=self.get_serializer_context())
        return Response({'child': child_serializer.data, 'pictures': serializer.data})

    

    @action(detail=True, url_path="latest_dailyinfo")
    def get_latest_dailyinformation(self, request, pk=None,**kwargs):
        # child = self.get_object()
        child = Child.objects.get(id=pk)
        daily_info = ChildDailyInformation.objects.filter(
            child=child).order_by('-updated_at').first()
        serializer = ChildDailyInformationReadSerializer(
            daily_info, context=self.get_serializer_context())
        child_serializer = ChildSerializer(
            child, context=self.get_serializer_context())
        return Response({'dailyInfo': serializer.data, 'child': child_serializer.data})

    @action(detail=False, url_path="children")
    def get_children_loggedin_user(self, request):
        user = request.user
        if user.role.name == "Parent":
            resp = []
            child = Child.objects.filter(parent = user).values()
            for data in child:
                emergencyContacts = list(Contact.objects.filter(child_id = data['id']).values())
                authPersons = list(AuthPerson.objects.filter(child_id = data['id']).values())
                # add server url to photo of child
                if data['photo'] is not None and data['photo'] != '':
                    photoUrl = 'http://3.136.224.87/media/' + data['photo']
                    data.update([('photo',photoUrl)])
                # add server url to photo of authpersons
                for auth in authPersons:
                    if auth['photo'] is not None and auth['photo'] != '':
                        photoUrl = 'http://3.136.224.87/media/' + auth['photo']
                        auth.update([('photo',photoUrl)])
                
                data.update([('emergencyContacts', emergencyContacts)])
                data.update([('authPersons', authPersons)])
            return Response(child)
        return Response(data="No Permissions",status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def add_child_to_sibling_group(request, pk):
    if request.user.role.name != Admin:
        return Response({'userrole': ['You are not Admin']}, status=status.HTTP_400_BAD_REQUEST)
    sibling_group = get_object_or_404(SiblingGroup.objects.all(), pk=pk)
    if 'children' in request.data:
        childIdList = request.data['children']
        children = []
        for child_id in childIdList:
            child = get_object_or_404(Child.objects.all(), pk=child_id)
            children.append(child)
        for child in children:
            if (child.sibling_group.id != sibling_group.id):
                sibling_group.numberOfSiblings += 1
            prev_group_id = child.sibling_group.id
            child.sibling_group = sibling_group
            child.save()
            notfication_utils.change_parent_sibling_group(prev_group_id, child.parent)
        sibling_group.save()

    return Response('success')


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    # permission_classes = (permissions.IsAuthenticated,
    #                       mypermissions.IsAdminRole)


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    # permission_classes = (permissions.IsAuthenticated,
    #                       mypermissions.IsAdminTeacherRole)
    filterset_fields = ['weekName', 'dayName']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        if 'weekName' in request.GET and 'dayName' in request.GET:
            weekName = request.GET.get('weekName')
            dayName = request.GET.get('dayName')
            if not queryset.first():
                menuItem = MenuItem(weekName=weekName, dayName=dayName)
                menuItem.save()
                serializer = self.get_serializer(menuItem)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path="AddFood")
    def addFood(self, request):
        serializer = AddFoodSerializer(data=request.data)
        if serializer.is_valid():
            weekName = serializer.validated_data.pop('weekName')
            dayName = serializer.validated_data.pop('dayName')
            queryset = self.get_queryset()
            menuItem = queryset.filter(
                dayName=dayName, weekName=weekName).order_by('-created_at').first()
            if not menuItem:
                menuItem = MenuItem(weekName=weekName, dayName=dayName)
                menuItem.save()

            foods = serializer.validated_data.pop('foods')
            menuItem.foods.add(*foods)
            menuItem.save()
            serializer = self.get_serializer(menuItem)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path="removefoodfrommenu")
    def removeFood(self, request):
        serializer = AddFoodSerializer(data=request.data)
        if serializer.is_valid():
            weekName = serializer.validated_data.pop('weekName')
            dayName = serializer.validated_data.pop('dayName')
            queryset = self.get_queryset()
            menuItem = queryset.filter(
                dayName=dayName, weekName=weekName).order_by('-created_at').first()
            if not menuItem:
                menuItem = MenuItem(weekName=weekName, dayName=dayName)
                menuItem.save()

            foods = serializer.validated_data.pop('foods')
            menuItem.foods.remove(*foods)
            menuItem.save()
            serializer = self.get_serializer(menuItem)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChildDailyInformationViewSet(viewsets.ModelViewSet):
    queryset = ChildDailyInformation.objects.all()
    serializer_class = ChildDailyInformationWriteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ChildDailyInformationReadSerializer
        else:
            return ChildDailyInformationWriteSerializer


class MyPictureViewSet(generics.ListAPIView, generics.DestroyAPIView):
    serializer_class = PictureSerializer
    permission_classes = (permissions.IsAuthenticated,
                          mypermissions.IsParentRole)

    def get_queryset(self):
        user = self.request.user
        children = Child.objects.filter(parent=user)
        q_object = Q()
        for child in children:
            q_object = q_object | Q(receiver=child)
        return Picture.objects.filter(q_object).order_by('-created_at')
    

class ChildPictureViewset(viewsets.ModelViewSet):
    serializer_class = PictureSerializer
    
    def destroy(self, request, **kwargs):
        pictureObj = Picture.objects.filter(id=kwargs['id'])
        image_path = pictureObj.values('image')[0]['image']
        join_both_path = os.path.join(BASE_PATH,image_path)
        os.remove(join_both_path)
        pictureObj.delete()
        return Response("Deleted successflly")




class PrivacyRightsViewset(viewsets.ModelViewSet):
    queryset = PrivacyRights.objects.all()
    serializer_class = PrivacyRightsSrializer