from rest_framework import generics, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Company
from .serializers import CompanySerializer
from users.permissions import IsOwnerOrAdmin

class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    @swagger_auto_schema(
        operation_summary="List all companies (Admin only)",
        operation_description="Retrieve a list of all companies. Only accessible to admin users.",
        responses={200: CompanySerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new company",
        operation_description="Create a new company. Only authenticated users can perform this action.",
        request_body=CompanySerializer,
        responses={201: CompanySerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    @swagger_auto_schema(
        operation_summary="Retrieve a company",
        operation_description="Retrieve details of a specific company by ID.",
        responses={200: CompanySerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a company",
        operation_description="Update details of a specific company. Only the owner or admin can perform this action.",
        request_body=CompanySerializer,
        responses={200: CompanySerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a company",
        operation_description="Delete a specific company. Only the owner or admin can perform this action.",
        responses={204: "No Content"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class CompanyMeView(generics.RetrieveAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve your company",
        operation_description="Retrieve the company owned by the currently authenticated user.",
        responses={200: CompanySerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return Company.objects.get(owner=self.request.user)