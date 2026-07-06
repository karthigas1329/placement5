from django.urls import path
from .views import PlacementOfficerRegisterAPIView

urlpatterns = [
    path('placement-officer/register/', PlacementOfficerRegisterAPIView.as_view()),
]


from . import views 
from django.urls import path
from .views import *