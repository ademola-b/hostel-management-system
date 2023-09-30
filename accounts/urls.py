from django.urls import path
from .views import LoginView, RegisterView, UpdateProfileView

app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LoginView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('update-profile/', UpdateProfileView.as_view(), name="update_profile"),
]
