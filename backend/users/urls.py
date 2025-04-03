from django.urls import path
from .views import RegisterUserView, LogoutView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('logout/', LogoutView.as_view(), name='logout-user'),
]
