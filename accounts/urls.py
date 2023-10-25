from django.urls import path, reverse
from .views import LoginView, RegisterView, UpdateProfileView, ProfileView, load_departments
from django.views.generic.base import RedirectView

app_name = "accounts"

urlpatterns = [
    # path('admin/', RedirectView.as_view(url=reverse('admin:index')), name='admin_page'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LoginView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('update-profile/', UpdateProfileView.as_view(), name="update_profile"),
    path('load-depts/', load_departments, name="departments"),
    path('profile/', ProfileView.as_view(), name="profile"),
]
