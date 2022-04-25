from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from django.db.models import Q
from pdb import set_trace as bp
from django.http import QueryDict
import json

from djqscsv import render_to_csv_response

from anam_backend_main import mypermissions
from .models import Appointment, PresetAppointmentSessions, TimeRangeItem, PresetItem, PresetRecord, PresetAppointment
from .models import PresetStatus
from NotificationApp.models import NotificationModel
from ChildApp.models import Child
from UserApp.models import User, ClassData
from .serializers import AppointmentWriteSerializer, AppointmentReadSerializer, PresetAppointmentSerializer, PresetRecordSerializer,\
    PresetAppointmentReadSerializer, PresetAppointmentWriteSerializer, PresetItemSerializer, SessionSerializer, TimeRangeSerializer
from anam_backend_main.constants import Parent, Teacher, Admin, \
    Bamboo, Iroko, Baobab, Acajou
# Create your views here.


class AppointmentViewSet(viewsets.ModelViewSet):
    print('c est bien moi AppointmentViewSet')
    queryset = Appointment.objects.all()
    serializer_class = AppointmentWriteSerializer

    def get_queryset(self):
        user = self.request.user
        if self.request.user.role.name == Admin:
            return Appointment.objects.all()
        elif self.request.user.role.name == Teacher:
            return Appointment.objects.filter(teacher=user)
        else:
            queryset = Child.objects.filter(parent=user)
            return Appointment.objects.filter(child__in=queryset)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'update':
            return AppointmentReadSerializer
        else:
            return AppointmentWriteSerializer

    @action(detail=False, url_path='user/(?P<userPk>\\d+)')
    def get_by_user(self, request, userPk=None):
        user = get_object_or_404(User, pk=userPk)
        queryset = self.get_queryset().filter(Q(teacher=user) | Q(parent=user))
        serializer = AppointmentReadSerializer(
            queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    def update_Appointmentstatus(self, request):
        status = request.data['status']
        appointment_id = request.data['appointment_id']
        child_id = request.data['child_id']
        teacher_id = request.data['teacher_id']

        childName = Child.objects.filter(id=child_id).values('first_name', 'last_name').get()
        childName = childName['first_name'] + ' ' + childName['last_name']
        if status == 'accept':
            notificationMessage = f"{childName}'s appointment got accepted"
        elif status == 'reject':
            notificationMessage = f"{childName}'s appointment got rejected"
        elif status == 'reschedule':
            notificationMessage = f"{childName}'s appointment requested for reschedule"
        elif status == 'proceed_reject':
            Appointment.objects.filter(id=appointment_id).delete()
            return Response({"Appointment deleted"})

        Appointment.objects.filter(id=appointment_id).update(status=status)

        # CAll Notification for teacher
        data = {
            "notificationMessage": notificationMessage,
            "module": "Appointment",
            "user": User.objects.get(id=teacher_id)
        }
        NotificationModel(**data).save()
        # Call Notification for Admin
        data = {
            "notificationMessage": notificationMessage,
            "module": "Appointment",
            "user": User.objects.get(id=2)
        }
        NotificationModel(**data).save()

        return Response({"Status updated"})


class PresetRecordViewSet(viewsets.ModelViewSet):
    queryset = PresetRecord.objects.all()
    serializer_class = PresetRecordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @action(detail=False, url_path='current')
    def get_current_record(self, request, userPk=None):
        queryset = self.get_queryset().order_by('-created_at').first()
        if not queryset:
            return Response("There is not any record", status=status.HTTP_204_NO_CONTENT)
        serializer = PresetRecordSerializer(
            queryset, context=self.get_serializer_context())
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        validated_data = request.data
        if('presetItems' in validated_data):
            presetItemsData = validated_data.pop('presetItems')

            for presetItemData in presetItemsData:
                presetItem = get_object_or_404(
                    PresetItem, pk=presetItemData.get('id'))

                if 'timeranges' in presetItemData:
                    timeranges_data = presetItemData.pop('timeranges')
                    id_list = []
                    for timerange_data in timeranges_data:
                        pk = timerange_data.pop('id')
                        timerangeItem = None
                        created = False
                        try:
                            timerangeItem = TimeRangeItem.objects.get(
                                pk=pk, presetItem=presetItem)
                        except ObjectDoesNotExist:
                            timerangeItem = TimeRangeItem.objects.create(
                                presetItem=presetItem, **timerange_data)
                            timerangeItem.save()
                        id_list.append(timerangeItem.id)
                        if not created:
                            timerangeSerializer = TimeRangeSerializer(
                                instance=timerangeItem, data=timerange_data, partial=partial)
                            if timerangeSerializer.is_valid():
                                timerangeSerializer.save()
                            else:
                                return Response(timerangeSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    timeranges = presetItem.timeranges.all()
                    for timerange in timeranges:
                        if timerange.id not in id_list:
                            timerange.delete()
                # print(presetItem)
                presetItemSerializer = PresetItemSerializer(
                    instance=presetItem, data=presetItemData, partial=partial)
                if presetItemSerializer.is_valid():
                    presetItemSerializer.save()
                else:
                    return Response(presetItemSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class PresetAppointmentViewSet(viewsets.ModelViewSet):
    queryset = PresetAppointment.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = PresetAppointmentSerializer

    def create(self, request):
        slot_time = request.data['duration']
        start_Date = datetime.strptime(request.data['startDate'], '%d-%m-%Y').date()
        end_Date = datetime.strptime(request.data['endDate'], '%d-%m-%Y').date()
        # calculate no. of days
        delta = end_Date - start_Date
        no_of_days = delta.days
        mySlotList = []
        for i in range(no_of_days+1):
            date_required = start_Date + timedelta(days=i)
            startTime_str = request.data['startTime']
            endTime_str = request.data['endTime']
            mySlotList_each_day = self.get_daily_slots(
                start=startTime_str, end=endTime_str, slot=slot_time, date=date_required)
            mySlotList.extend(mySlotList_each_day)
       # date_required = datetime.strptime(request.data['startDate'], '%d-%m-%Y').date()
        # mySlotList = self.get_daily_slots(start=startTime_str, end=endTime_str, slot=slot_time, date=date_required)
        request.data['startDate'] = datetime.strptime(request.data['startDate'], '%d-%m-%Y').date()
        request.data['endDate'] = datetime.strptime(request.data['endDate'], '%d-%m-%Y').date()
        request.data['startTime'] = datetime.strptime(request.data['startTime'], '%H:%M:%S').time()
        request.data['endTime'] = datetime.strptime(request.data['endTime'], '%H:%M:%S').time()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        appointment_id = serializer.data['id']
        for i in range(len(mySlotList)-1):
            start = mySlotList[i]
            end = mySlotList[i+1]
            startDate = start.date()
            endDate = end.date()
            startTime = start.time()
            endTime = end.time()
            if startDate == endDate:
                presetAppointmentSession = PresetAppointmentSessions.objects.create(
                    appointment_id=appointment_id, startDate=startDate, endDate=endDate,
                    startTime=startTime, endTime=endTime)
                presetAppointmentSession.save()
        AppointmentData = serializer.data

        className = ClassData.objects.filter(id=serializer.data['className']).values('name').get()['name']
        parent_id_list = list(Child.objects.filter(nameOfClass=className).values('parent_id'))
        for parent in parent_id_list:
            user_id = parent['parent_id']
            data = {
                "notificationMessage": f"Preset-appointment has been set for class:{className}.",
                "module": "Preset-Appointment",
                "user": User.objects.get(id=user_id)
            }
            NotificationModel(**data).save()

        queryset = PresetAppointmentSessions.objects.filter(appointment_id=appointment_id).values()
        finalData = {'AppointmentData': AppointmentData, "SessionData": list(queryset)}
        return Response(finalData)

    def get_daily_slots(self, start, end, slot, date):
        # combine start time to respective day
        dt = datetime.combine(date, datetime.strptime(start, '%H:%M:%S').time())
        slots = [dt]
        # increment current time by slot till the end time
        while (dt.time() < datetime.strptime(end, '%H:%M:%S').time()):
            dt = dt + timedelta(minutes=slot)
            slots.append(dt)
        return slots

    def list(self, request):
        data = PresetAppointment.objects.all()
        responseData = list(PresetAppointmentSerializer(data, many=True).data)
        responseList = []

        for i in range(len(responseData)):
            eachDict = {}
            eachDict['appointment'] = dict(responseData[i])
            appointment_id = eachDict['appointment']['id']
            queryset = PresetAppointmentSessions.objects.filter(appointment_id=appointment_id).values()
            eachDict['SessionData'] = list(queryset)
            responseList.append(eachDict)

        return Response(responseList)

    def retrieve(self, request, pk=None):
        data = PresetAppointment.objects.filter(className_id=pk)
        responseData = list(PresetAppointmentSerializer(data, many=True).data)
        responseList = []

        for i in range(len(responseData)):
            eachDict = {}
            eachDict['appointment'] = dict(responseData[i])
            appointment_id = eachDict['appointment']['id']
            queryset = PresetAppointmentSessions.objects.filter(appointment_id=appointment_id).values()
            eachDict['SessionData'] = list(queryset)
            responseList.append(eachDict)

        return Response(responseList)

    def deletePresetAppoinment(self, request, **kwargs):
        try:
            PresetAppointmentSessions.objects.filter(appointment_id=kwargs['id']).delete()
            PresetAppointment.objects.filter(id=kwargs['id']).delete()
            return Response("deleted")
        except Exception as e:
            return Response({"error": str(e)})

    def get_queryset(self):
        """
        current_preset=True in query parameter, return presetAppointments of current preset
        else; return All presetAppointments
        """
        req = self.request
        is_current_preset = req.query_params.get('current_preset')
        queryset = PresetAppointment.objects.none()
        # print(is_current_preset)
        if is_current_preset == 'true':

            currentRecord = PresetRecord.objects.filter(
                status=PresetStatus.Started).order_by('-created_at').first()
            if currentRecord:
                queryset = PresetAppointment.objects.filter(
                    presetInfo=currentRecord)
            else:
                return PresetAppointment.objects.none()
        else:
            queryset = PresetAppointment.objects.all()
        if(self.request.user.role == Admin):
            return queryset
        elif self.request.user.role == Teacher:
            user = self.request.user
            classnames = user.get_classNames()
            if len(classnames) == 0:
                return PresetAppointment.objects.none()
            q_object = Q()
            for name in classnames:
                q_object = q_object | Q(className=name)
            # print( PresetAppointment.objects.filter(q_object))
            return PresetAppointment.objects.filter(q_object)
        else:
            return queryset

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'update':
            return PresetAppointmentReadSerializer
        else:
            return PresetAppointmentWriteSerializer

    @action(detail=False, url_path='current_user')
    def get_preset_apnts_current_user(self, request):
        user = request.user
        if user.role != Parent:
            return Response([])
        children = user.child.sibling_group.childs.all()
        serializer = PresetAppointmentReadSerializer(PresetAppointment.objects.filter(child__in=children).all(), many=True,
                                                     context=self.get_serializer_context())
        return Response(serializer.data)


class PresetAppointmentSessionsViewset(viewsets.ModelViewSet):
    queryset = PresetAppointmentSessions.objects.all()
    serializer_class = SessionSerializer

    def downloadSessionDeatils(self, request, *args, **kwargs):
        sessionQuerySet = PresetAppointmentSessions.objects.filter(child_id__isnull=False).values(
            'id', 'appointment_id', 'appointment__title', 'child__first_name', 'child__last_name', 'child__nameOfClass', 'startDate', 'endDate', 'startTime', 'endTime')
        # used djqscsv package method
        return render_to_csv_response(sessionQuerySet)
