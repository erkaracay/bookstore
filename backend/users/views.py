from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import Group
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from companies.models import Company
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class RegisterUserView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: UserSerializer, 400: "Validation Error"},
        operation_description="Register a new user (buyer/seller/admin)."
    )
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Add to default group
            user_group = Group.objects.get(name='Buyer')
            user.groups.add(user_group)

            # Admin group (if superuser)
            if user.user_type == 'admin' and user.is_superuser:
                admin_group, _ = Group.objects.get_or_create(name='Admin')
                user.groups.add(admin_group)

            user.save()

            response_data = {"user": serializer.data}

            # If seller with company_name (i.e. not "Individual")
            company_name = request.data.get("company_name")
            if user.user_type == "seller" and company_name and company_name != "Individual":
                company = Company.objects.create(name=company_name, owner=user)
                company_serializer = CompanySerializer(company)
                response_data["company"] = company_serializer.data

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Log out the user by blacklisting their refresh token.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description="The refresh token to blacklist.")
            }
        ),
        responses={
            205: 'Refresh token blacklisted successfully.',
            400: 'Invalid refresh token or request body.'
        }
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
