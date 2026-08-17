from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PlacementOfficerSerializer

#registration
#placement officer
class PlacementOfficerRegisterAPIView(APIView):

    def post(self, request):
        serializer = PlacementOfficerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Registration Successful",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#recruiter registration

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Recruiter
from .serializers import RecruiterSerializer
from datetime import date

# @api_view(['POST'])
# def recruiter_register(request):

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def recruiter_register(request):

    if request.method == "GET":
        return Response({"message": "Recruiter API Working"})

    # POST logic here

    count = Recruiter.objects.count() + 1

    hr_id = f"HR-{count:03}"

    today = date.today().strftime("%d/%m/%Y")

    data = request.data.copy()

    data["hr_id"] = hr_id
    data["registered_on"] = today

    serializer = RecruiterSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message":"Registration Successful",
            "data":serializer.data
        },status=status.HTTP_201_CREATED)

    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#student registration
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentRegistrationSerializer

class StudentRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = StudentRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Registration successful!"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#training coordinator

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import StudentCoordinator
from .serializers import StudentCoordinatorSerializer


class StudentCoordinatorRegisterView(APIView):

    def post(self, request):
        serializer = StudentCoordinatorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Student Coordinator registered successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#login
#common login
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import commonLoginSerializer

class CommonLoginAPIView(APIView):

    def post(self, request):
        serializer = commonLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        role = serializer.validated_data["role"]

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is None:
            return Response(
                {
                    "success": False,
                    "message": "Invalid email or password."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        if user.role != role:
            return Response(
                {
                    "success": False,
                    "message": "Selected role does not match the user."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "success": True,
                "message": "Login successful.",

                "access": str(refresh.access_token),
                "refresh": str(refresh),

                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role,
                }
            },
            status=status.HTTP_200_OK
        )
    
#PLACEMENTOFFICERLOGIN

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PlacementOfficerlogin


@api_view(["POST"])
def placement_login(request):

    email = request.data.get("Email")
    password = request.data.get("password")

    if not email:
        return Response({
            "Email":"Email is required*"
        },status=400)

    if not password:
        return Response({
            "password":"Password is required*"
        },status=400)

    try:
        user = PlacementOfficerlogin.objects.get(email=email)

    except PlacementOfficerlogin.DoesNotExist:

        return Response({
            "loginError":"Invalid Email or Password. Please try again."
        },status=400)

    if user.password != password:

        return Response({
            "loginError":"Invalid Email or Password. Please try again."
        },status=400)

    return Response({

        "message":"Login Successful",

        "user":{

            "id":user.id,
            "email":user.email

        }

    },status=200)

#recruiterlogin

from rest_framework.decorators import api_view
from .models import RecruiterLogin

@api_view(["POST"])
def RecruiterLogin_login(request):

    email = request.data.get("Email")
    password = request.data.get("password")

    if not email:
        return Response({
            "Email":"Email is required*"
        },status=400)

    if not password:
        return Response({
            "password":"Password is required*"
        },status=400)

    try:
        user = RecruiterLogin.objects.get(email=email)

    except RecruiterLogin.DoesNotExist:

        return Response({
            "loginError":"Invalid Email or Password. Please try again."
        },status=400)

    if user.password != password:

        return Response({
            "loginError":"Invalid Email or Password. Please try again."
        },status=400)

    return Response({

        "message":"Login Successful",

        "user":{

            "id":user.id,
            "email":user.email

        }

    },status=200)

#studentlogin 
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class StudentLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({"detail": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Authenticate checks the credentials against the database
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            # Generate JWT tokens manually
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'role': user.role,
                'full_name': user.full_name,
                'email': user.email
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid Email or Password."}, status=status.HTTP_401_UNAUTHORIZED)

#trainingcoordinator login

from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import TrainingCoordinator
from .serializers import TrainingCoordinatorLoginSerializer


class TrainingCoordinatorLoginView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = TrainingCoordinatorLoginSerializer(data=request.data)

        if serializer.is_valid():

            email = serializer.validated_data["Email"]
            password = serializer.validated_data["password"]

            try:
                coordinator = TrainingCoordinator.objects.get(
                    official_email=email
                )

            except TrainingCoordinator.DoesNotExist:

                return Response(
                    {
                        "success": False,
                        "message": "Invalid Email or Password"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            if not check_password(password, coordinator.password):

                return Response(
                    {
                        "success": False,
                        "message": "Invalid Email or Password"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            refresh = RefreshToken()

            return Response(
                {
                    "success": True,
                    "message": "Login Successful",

                    "access": str(refresh.access_token),
                    "refresh": str(refresh),

                    "user": {
                        "id": coordinator.id,
                        "name": coordinator.full_name,
                        "email": coordinator.official_email,
                        "department": coordinator.department,
                    }
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#adminlogin

from .models import Admin
from .serializers import AdminLoginSerializer

class AdminLoginView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = AdminLoginSerializer(data=request.data)

        if serializer.is_valid():

            email = serializer.validated_data["Email"]
            password = serializer.validated_data["password"]

            try:
                admin = Admin.objects.get(email=email)

            except Admin.DoesNotExist:

                return Response(
                    {
                        "success": False,
                        "message": "Invalid Credentials"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            if not admin.verify_password(password):

                return Response(
                    {
                        "success": False,
                        "message": "Invalid Credentials"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            refresh = RefreshToken()

            return Response({

                "success": True,
                "message": "Login Successful",

                "access": str(refresh.access_token),
                "refresh": str(refresh),

                "admin": {
                    "id": admin.id,
                    "full_name": admin.full_name,
                    "email": admin.email
                }

            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#forgotpassword

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import (urlsafe_base64_encode,urlsafe_base64_decode)
from django.utils.encoding import (force_bytes,force_str)
from django.core.mail import send_mail
from .serializers import (ForgotPasswordSerializer,ResetPasswordSerializer)

User = get_user_model()

class ForgotPasswordAPIView(APIView):

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)

            except User.DoesNotExist:
                return Response(
                    {
                        "success": False,
                        "message": "Email not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_link = (
                f"http://localhost:5173/reset-password/{uid}/{token}/"
            )
            send_mail(
                subject="Password Reset",
                message=f"""
Hello,

Click below to reset your password.

{reset_link}

If you didn't request this, ignore this email.
""",

                from_email=None,
                recipient_list=[email],
            )

            return Response(
                {
                    "success": True,
                    "message": "Reset link sent successfully."
                }
            )

        return Response(serializer.errors, status=400)
    
class ResetPasswordAPIView(APIView):

    def post(self, request):

        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            uid = serializer.validated_data["uid"]
            token = serializer.validated_data["token"]
            password = serializer.validated_data["password"]

            try:
                user_id = force_str(
                    urlsafe_base64_decode(uid)
                )
                user = User.objects.get(pk=user_id)

            except:
                return Response(
                    {
                        "message": "Invalid Link"
                    },
                    status=400
                )

            if not PasswordResetTokenGenerator().check_token(
                user,
                token
            ):

                return Response(
                    {
                        "message": "Invalid or Expired Token"
                    },
                    status=400
                )

            user.set_password(password)
            user.save()
            return Response(
                {
                    "success": True,
                    "message": "Password Changed Successfully"
                }
            )

        return Response(serializer.errors, status=400)

#adminDashboard
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_admin_dashboard_data(request):
    mock_data = {
        "status": "success",
        "data": {
            "stats": {
                "totalPlacements": "4,120",
                "activeStudents": "12,482",
                "verifiedRecruiters": "3,142",
                "partnerCompanies": "312"
            },
            "placementData": [
                { "month": "Jan", "placements": 22 },
                { "month": "Feb", "placements": 34 },
                { "month": "Mar", "placements": 28 },
                { "month": "Apr", "placements": 47 },
                { "month": "May", "placements": 39 },
                { "month": "Jun", "placements": 58 }
            ],
            "activityLog": [
                { "id": 1, "type": "new_user", "heading": "New User Registration", "subtitle": "Alex Morgan", "time": "2 mins ago" },
                { "id": 2, "type": "doc_upload", "heading": "Company Document Uploaded", "subtitle": "Nexus Dynamics", "time": "45 mins ago" },
                { "id": 3, "type": "recruiter_verify", "heading": "Recruiter Verified", "subtitle": "Global Tech", "time": "3 hrs ago" },
                { "id": 4, "type": "security_update", "heading": "Security Policy Updated", "subtitle": "Applied globally", "time": "5 hrs ago" },
                { "id": 5, "type": "login_failed", "heading": "Failed Login Attempt", "subtitle": "IP:192.168.1.45", "time": "8 hrs ago" }
            ],
            "userManagement": [
                { "id": 1, "name": "Sarah K. Jenkins", "email": "sarah.j@globalhr.com", "role": "RECRUITER", "activity": "Published \"Senior AI Architect\" role", "time": "2 mins ago" },
                { "id": 2, "name": "David Lee", "email": "d.lee@candidate.me", "role": "CANDIDATE", "activity": "Submitted portfolio via AI matching", "time": "1 hour ago" }
            ]
        }
    }
    return Response(mock_data)

#Training coordinator dashboard
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import DashboardSummary
from .serializers import DashboardSummarySerializer

class TrainingCoordinatorDashboardView(APIView):

    def get(self, request):
        dashboard = DashboardSummary.objects.first()

        if dashboard is None:
            return Response({
                "message": "No dashboard summary data available."
            })

        serializer = DashboardSummarySerializer(dashboard)
        return Response(serializer.data)    
        

#recruiter Dashboard
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.utils import timezone

from .models import *
from .serializers import *

class RecruiterDashboardView(APIView):
    """
    Single endpoint that returns everything the RecruiterDashboard needs.
    GET /api/dashboard/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Stats – prefer stored snapshots, fall back to live counts
        stored_stats = {s.key: s for s in DashboardStat.objects.all()}
        active_jobs = Job.objects.filter(status='active').count()
        new_apps = Application.objects.filter(
            applied_at__date=timezone.now().date()
        ).count()
        interviews_today = Interview.objects.filter(
            scheduled_at__date=timezone.now().date(),
            status='scheduled'
        ).count()
        placements_count = Placement.objects.count()

        def build_stat(key, live_value, default_badge='', default_class=''):
            s = stored_stats.get(key)
            if s:
                return {
                    'id': s.id,
                    'key': s.key,
                    'title': key.replace('_', ' ').upper(),
                    'value': s.value,
                    'badgeText': s.badge_text or default_badge,
                    'badgeClass': s.badge_class or default_class,
                }
            return {
                'id': None,
                'key': key,
                'title': key.replace('_', ' ').upper(),
                'value': live_value,
                'badgeText': default_badge,
                'badgeClass': default_class,
            }

        stats = [
            build_stat('active_jobs', active_jobs, '+12% VS LAST MO', 'Rec-Dashboard-badge-positive'),
            build_stat('new_applications', new_apps or Application.objects.count(), '+4 NEW TODAY', 'Rec-Dashboard-badge-blue'),
            build_stat('interviews_today', interviews_today, 'URGENT', 'Rec-Dashboard-badge-urgent'),
            build_stat('placements', placements_count, 'Target: 20', 'Rec-Dashboard-badge-target'),
        ]

        # Pipeline
        stage_map = {
            'sourcing': 'SOURCING',
            'applied': 'APPLIED',
            'interviewing': 'INTERVIEWING',
            'offer': 'OFFER STAGE',
        }
        stage_counts = dict(
            Application.objects.values('stage').annotate(c=Count('id')).values_list('stage', 'c')
        )
        # Include sourcing even if zero applications in that stage
        max_count = max(stage_counts.values()) if stage_counts else 1
        pipeline = []
        for key, label in stage_map.items():
            count = stage_counts.get(key, 0)
            pct = int((count / max_count) * 100) if max_count else 0
            pipeline.append({
                'stage': label,
                'count': count,
                'percentage': f'{pct}%',
            })

        pipeline_metrics = [
            {'label': 'AVG. RESPONSE', 'value': '4.2d'},
            {'label': 'CONVERSION', 'value': '18%'},
            {'label': 'TIME TO HIRE', 'value': '22d'},
        ]

        # Upcoming interviews
        interviews_qs = Interview.objects.filter(
            scheduled_at__gte=timezone.now(),
            status='scheduled'
        ).select_related('application__candidate', 'application__job')[:10]
        interviews = InterviewSerializer(interviews_qs, many=True).data

        # Resume verification table (from candidates + latest application status)
        verifications = []
        for c in Candidate.objects.all()[:20]:
            app = c.applications.order_by('-applied_at').first()
            status_label = app.status if app else 'pending'
            verifications.append({
                'id': c.id,
                'candidate': c.name,
                'resume': {
                    'label': 'Verified' if c.resume_verified else 'Pending',
                    'verified': c.resume_verified,
                },
                'portfolio': {
                    'label': 'Available' if c.portfolio_available else 'Not Available',
                    'available': c.portfolio_available,
                },
                'status': {
                    'label': status_label.capitalize(),
                    'value': status_label,
                },
            })

        ai_insights = AIInsightSerializer(
            AIInsight.objects.filter(is_active=True)[:5], many=True
        ).data

        quick_links = QuickLinkSerializer(
            QuickLink.objects.filter(is_active=True), many=True
        ).data

        return Response({
            'user': UserSerializer(request.user).data,
            'stats': stats,
            'pipeline': pipeline,
            'pipeline_metrics': pipeline_metrics,
            'interviews': interviews,
            'verifications': verifications,
            'ai_insights': ai_insights,
            'quick_links': quick_links,
        })

