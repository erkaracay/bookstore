from django.urls import path
from .views import CompanyListCreateView, CompanyDetailView, CompanyMeView

urlpatterns = [
    path('', CompanyListCreateView.as_view(), name='company-list-create'),
    path('<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('me/', CompanyMeView.as_view(), name='company-me'),
]
