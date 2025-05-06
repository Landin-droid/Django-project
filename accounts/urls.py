from django.urls import path
from . import views
from .views import ProfileUpdateView

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
]