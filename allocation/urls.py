from django.urls import path
from .views import DashboardView, Hostels, PaymentView

app_name = "allocation"
urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('select-hostel/', Hostels.as_view(), name='hostel-list'),
    path('<str:pk>/payment/', PaymentView.as_view(), name='payment'),
]
