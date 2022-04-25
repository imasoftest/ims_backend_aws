from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'AppointmentCenter'

router = DefaultRouter()
router.register('preset_record', views.PresetRecordViewSet, basename='presetRecords')
router.register('preset_appointments', views.PresetAppointmentViewSet, basename='presetAppointments')
router.register('preset_appointments_session', views.PresetAppointmentSessionsViewset, basename='presetAppointmentsSession')
router.register('', views.AppointmentViewSet, basename='appointments')


urlpatterns = [
    path('deletePresetAppoinment/<int:id>/',views.PresetAppointmentViewSet.as_view({"delete":"deletePresetAppoinment"})),
    path('update_Appointmentstatus/', views.AppointmentViewSet.as_view({"put": "update_Appointmentstatus"}), name='update-status'),
    path('download_session_details/', views.PresetAppointmentSessionsViewset.as_view({"get": "downloadSessionDeatils"}), name='download-session'),
    path('', include(router.urls)),
    ]
