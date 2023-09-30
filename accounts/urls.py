from django.urls import path
from .views import LoginView, RegisterView

app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LoginView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
]
