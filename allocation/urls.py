from django.urls import path
from .views import (DashboardView, Hostels, PaymentView, 
                    AllocatedRoomView, RegisteredStudentsView, 
                    AllocatedStudentsView, AllocatedHallView,
                    PaymentSuccessfulView, PaymentCancelledView,
                    RoomDetailsView)

from . import views

app_name = "allocation"
urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('select-hostel/', Hostels.as_view(), name='hostel-list'),
    path('<str:pk>/payment/', PaymentView.as_view(), name='payment'),
    path('allocated-room/', AllocatedRoomView.as_view(), name='allocated-room'),
    path('registered-students/', RegisteredStudentsView.as_view(), name="registered-students"),
    path('allocated-students/', AllocatedStudentsView.as_view(), name="allocated-students"),
    path('allocated-hall/', AllocatedHallView.as_view(), name="allocated-hall"),

    path('payment_successful/<str:pk>/', PaymentSuccessfulView.as_view(), name="payment_successful"),
    path('payment_cancelled', PaymentCancelledView.as_view(), name="payment_cancelled"),
    # path('stripe_webhook', views.stripe_webhook, name="stripe_webhook"),

    path('room-details/', RoomDetailsView.as_view(), name="room_detail")

]
