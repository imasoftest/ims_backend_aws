from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from .models import User, Roles, ClassData, NationalityData
from anam_backend_main.myserializerfields import Base64ImageField
from ChildApp.models import Child
import json
from pdb import set_trace as bp


class ChildSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(max_length=50, validators=[UniqueValidator(queryset=User.objects.all())])
    classNames = serializers.SerializerMethodField()
    password = serializers.CharField(max_length=255, write_only=True, required=False)
    child = ChildSmallSerializer(read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)
    notes = serializers.CharField(allow_blank=True)
    picture = Base64ImageField(required=False)

    class Meta:
        model = User
        read_only_fields = ['last_login']
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role', 'role_name', 'notes',
                  'picture', 'classnames', 'classNames', 'password', 'child', 'phoneNumber', 'altPhoneNumber',
                  'address','dob')

    def get_classNames(self, obj):
        try:
            data = json.loads(obj.classnames)
            # bp()
            if (type(data) == type([])):
                return data
            return []
        except Exception:
            return []

    def create(self, validated_data):
        print(validated_data)
        if 'password' in validated_data:
            print(True)
            validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)


class PasswordSerializer(serializers.Serializer):
    current_pwd = serializers.CharField(required=True)
    new_pwd = serializers.CharField(required=True)


class PasswordSerializerTwo(serializers.Serializer):
    new_pwd = serializers.CharField(required=True)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassData
        fields = '__all__'


class NationalitySerializer(serializers.ModelSerializer):
    createdBy = serializers.CharField(source='createdBy.first_name', read_only=True)

    def create(self, validated_data):
        validated_data['createdBy'] = self.context['request'].user
        return super(NationalitySerializer, self).create(validated_data)

    class Meta:
        model = NationalityData
        fields = '__all__'
        # read_only_fields = ['createdBy']
