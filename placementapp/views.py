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

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PlacementOfficerSerializer


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

#login
#common login
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer

class CommonLoginAPIView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

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
    
#placement officer login

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PlacementOfficer


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
        user = PlacementOfficer.objects.get(email=email)

    except PlacementOfficer.DoesNotExist:

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


#student login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import StudentRegistrationSerializer

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