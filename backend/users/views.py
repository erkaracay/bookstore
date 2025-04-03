from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import Group
from .serializers import UserSerializer

User = get_user_model()

class RegisterUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Assign user to 'buyer' group by default
            user_group = Group.objects.get(name='Buyer')
            user.groups.add(user_group)

            # If user is an admin, assign them to the 'admin' group
            if user.user_type == 'admin' and user.is_superuser:
                admin_group, created = Group.objects.get_or_create(name='Admin')
                user.groups.add(admin_group)
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
