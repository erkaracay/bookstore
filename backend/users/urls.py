from django.urls import path
from .views import RegisterUserView, LogoutView, UserMeView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('logout/', LogoutView.as_view(), name='logout-user'),
    path('me/', UserMeView.as_view(), name='user-me'),
]
