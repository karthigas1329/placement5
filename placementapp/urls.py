from django.urls import path
from .views import PlacementOfficerRegisterAPIView,StudentRegistrationView,recruiter_register,StudentCoordinatorRegisterView
from .views import CommonLoginAPIView,placement_login,StudentLoginView
urlpatterns = [
#registration
    path('placement-officer/register/', PlacementOfficerRegisterAPIView.as_view()),
    path('register/student/', StudentRegistrationView.as_view(), name='student-registration'),
    path('recruiter-register/', recruiter_register),
    path('student-coordinator/register/',StudentCoordinatorRegisterView.as_view(),name="student-coordinator-register"),
    
#login
    path("commonlogin/", CommonLoginAPIView.as_view(), name="login"),
    path("placementofficer-login/", placement_login),
    path('api/student-login/', StudentLoginView.as_view(), name='student-login'),
]
