from django.urls import path
from .views import SensorListCreateAPIView, MeasurementAPIView, SensorDetailAPIView

urlpatterns = [
    path('sensors/', SensorListCreateAPIView.as_view(), name='sensor_list'),
    path('sensors/<int:pk>/', SensorDetailAPIView.as_view(), name='sensor_detail'),
    path('measurements/', MeasurementAPIView.as_view(), name='measurements'),
]
