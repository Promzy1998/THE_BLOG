from django.urls import path
from django.contrib.auth.views import LogoutView
from .models import CustomUser
from .views import SignupLoginView, Logout, UrlView 

urlpatterns = [
    path("signup_login/", SignupLoginView.as_view(), name="signup_login"),  # Handles both signup & login
    # path("Test/", TestView.as_view(), name="Tview"), 
    path("author_blog/<str:name>", UrlView.as_view(), name="UrlView"), 
    path("Logout/", Logout.as_view(), name="Logout"),  # Logout and redirect
]
