from django.urls import path
from .views import PlacementOfficerRegisterAPIView,StudentRegistrationView,recruiter_register,StudentCoordinatorRegisterView
from .views import CommonLoginAPIView,placement_login,RecruiterLogin_login,StudentLoginView,TrainingCoordinatorLoginView,AdminLoginView
from .views import ForgotPasswordAPIView,ResetPasswordAPIView,get_admin_dashboard_data,TrainingCoordinatorDashboardView,RecruiterDashboardView

urlpatterns = [
#registration
    path('placement-officer/register/', PlacementOfficerRegisterAPIView.as_view()),
    path('register/student/', StudentRegistrationView.as_view(), name='student-registration'),
    path('recruiter-register/', recruiter_register),
    path('student-coordinator/register/',StudentCoordinatorRegisterView.as_view(),name="student-coordinator-register"),
    
#login
    path("commonlogin/", CommonLoginAPIView.as_view(), name="login"),
    path("login/", placement_login),
    path("RecruiterLogin/",RecruiterLogin_login),
    path('studentlogin/', StudentLoginView.as_view(), name='student-login'),
    path("training-coordinator/login/",TrainingCoordinatorLoginView.as_view(),name="training-coordinator-login"),
    path("admin/login/", AdminLoginView.as_view(), name="admin-login"),
    path("forgot-password/",ForgotPasswordAPIView.as_view(),name="forgot-password"),
    path("reset-password/",ResetPasswordAPIView.as_view(),name="reset-password"),

#Dashboard
    path('admin-dashboard/', get_admin_dashboard_data, name='admin-dashboard'),
    path("training-coordinator/dashboard/", TrainingCoordinatorDashboardView.as_view(), name="training-coordinator-dashboard"),
    path('recruiter-dashboard/', RecruiterDashboardView.as_view(), name='recruiter-dashboard'),

]

