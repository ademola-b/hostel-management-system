from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, ListView

from accounts.models import Student


from .decorators import redirect_anonymous_user, user_profile_checker
from .models import Hall, AllocatedRooms, Room


# Create your views here.
class Onboard(TemplateView):
    template_name = "landing.html"

@method_decorator(redirect_anonymous_user, name='get')
class DashboardView(View, LoginRequiredMixin):
    def get(self, request):
        return render(request, "dashboard.html")
    
@method_decorator(redirect_anonymous_user, name='get')
@method_decorator(user_profile_checker, name='get')
class Hostels(ListView, LoginRequiredMixin):
    queryset = Hall.objects.all()
    template_name = 'hostel/select-hostel.html'

@method_decorator(redirect_anonymous_user, name='get')
class PaymentView(View):
    template_name = 'hostel/payment.html'

    def get(self, request, pk):
        #get hall
        hall = Hall.objects.get(hall_id = pk)
        return render(request, self.template_name, {'hall':hall})
    
    def post(self, request, pk):
        student = Student.objects.get(user = request.user)
        # alloc_student = AllocatedRooms.objects.get(student=student)
        hall = Hall.objects.get(hall_id = pk)

        if student.payment_made == True:
            messages.warning(request, "You already paid for hostel and have been allocated a room")
        else:
            #allocate a temporary hall
            
            #get allocated hall
            try:
                with transaction.atomic():
                    student.payment_made = True
                    student.save()
                    messages.success(request, "Payment Successful")

                    alloc_room = AllocatedRooms.objects.exists()

                    if alloc_room:
                        #get last room created
                        # room = Room.objects.latest('room_id')
                        room = Room.objects.filter(hall=hall).last()
                        if room is not None:
                            print(f"room occ - {room.room_num} - {room.current_occupancy}")
                            if room.current_occupancy < 4:
                                AllocatedRooms.objects.create(student = student, room = room)
                                room.current_occupancy += 1
                                room.save()
                                messages.success(request, "You have been allocated a room")
                                #redirect to specified page
                            else:
                                #create another room
                                if hall.room_number <= 0 and hall.status == 'unavailable':
                                    student.payment_made = False
                                    student.save()
                                    #reverse payment
                                    messages.error(request, "Hall is occupied, kindly select another hall")
                                    return redirect('allocation:hostel-list')
                                else:
                                    hall.room_number -= 1

                                    if hall.room_number <= 0:
                                        hall.status = 'unavailable'
                                    
                                    new_room = Room.objects.create(hall=hall, room_num=room.room_num + 1)
                                    AllocatedRooms.objects.create(student = student, room = new_room)
                                    new_room.current_occupancy += 1
                                    new_room.save()
                                    messages.success(request, "You have been allocated a room")

                                hall.save()             
                        else:
                            #create a new room
                            new_room = Room.objects.create(hall=hall, room_num=1)
                            AllocatedRooms.objects.create(student = student, room = new_room)
                            new_room.current_occupancy += 1
                            new_room.save()
                            messages.success(request, "You have been allocated to a room")          

                    else:
                        room = Room.objects.create(hall=hall, room_num = 1)
                        AllocatedRooms.objects.create(student = student, room = room)
                        room.current_occupancy += 1
                        room.save()
                        messages.success(request, "You have been allocated a room")                

                    #payment logic
                    # raise Exception("Payment Failed. Retry")
        
            except Exception as e:
                print(e)
                messages.error(request, f"An error occurred: {e}")
                return redirect("allocation:hostel-list")
                 

        return render(request, self.template_name, {'hall':hall})

        


