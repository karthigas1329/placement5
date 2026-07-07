from django.urls import path
from .views import PlacementOfficerRegisterAPIView,StudentRegistrationView,recruiter_register,StudentCoordinatorRegisterView

urlpatterns = [
    path('placement-officer/register/', PlacementOfficerRegisterAPIView.as_view()),
    path('register/student/', StudentRegistrationView.as_view(), name='student-registration'),
    path('recruiter-register/', recruiter_register),
    path('student-coordinator/register/',StudentCoordinatorRegisterView.as_view(),name="student-coordinator-register"),
]
