from django.shortcuts import render
from pdb import set_trace as bp
from django.db.models import Q
from rest_framework import viewsets, mixins, status
from UserApp.models import User, Roles, ClassData, NationalityData
from UserApp.serializers import UserSerializer, PasswordSerializer, PasswordSerializerTwo, RoleSerializer, \
    ClassSerializer, NationalitySerializer
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.
class NationalityViewSet(viewsets.ModelViewSet):
    queryset = NationalityData.objects.all()
    serializer_class = NationalitySerializer


class ClassViewSet(viewsets.ModelViewSet):
    queryset = ClassData.objects.all()
    serializer_class = ClassSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RoleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().exclude(is_superuser=True).order_by('first_name')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ['role']

    @action(detail=False)
    def current_user(self, request):
        current_user = request.user
        serializer = self.get_serializer(current_user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def set_my_password(self, request):
        user = request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data['current_pwd']):
                return Response({"current_pwd": ['Current Password is Incorrect']}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data['new_pwd'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializerTwo(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['new_pwd'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
