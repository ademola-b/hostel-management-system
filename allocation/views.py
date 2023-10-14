from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View, ListView
import stripe
import time

from .forms import FilterForm

from accounts.models import Student


from .decorators import redirect_anonymous_user, user_profile_checker
from .models import Hall, AllocatedRooms, Room


# Create your views here.
class Onboard(TemplateView):
    template_name = "landing.html"

@method_decorator(redirect_anonymous_user, name='get')
class DashboardView(View, LoginRequiredMixin):
    def get(self, request):
        try:
            if request.user.is_warden:
                print("warder")
                halls = Hall.objects.all()
                return render(request, "dashboard.html", {'halls':halls})
            else:
                print("not warder")
                alloc_room = AllocatedRooms.objects.get(student = request.user.student)
                return render(request, "dashboard.html", {'alloc_room':alloc_room})      
        except:
            return render(request, "dashboard.html")

    
@method_decorator(redirect_anonymous_user, name='get')
@method_decorator(user_profile_checker, name='get')
class Hostels(ListView, LoginRequiredMixin):
    # queryset = Hall.objects.all()
    model = Hall
    context_object_name = "halls"
    template_name = 'hostel/select-hostel.html'

    def get_queryset(self):
        user = self.request.user
        if user.gender == 'male':
            halls = Hall.objects.filter(gender = 'boys')
        else:
            halls = Hall.objects.filter(gender = 'girls')

        return halls
    

@method_decorator(redirect_anonymous_user, name='get')
class PaymentView(View):
    template_name = 'hostel/payment.html'

    def get(self, request, pk):
        #get hall
        hall = Hall.objects.get(hall_id = pk)
        return render(request, self.template_name, {'hall':hall})
    
    def post(self, request, pk):
        student = Student.objects.get(user = request.user)

        try:
            hall = Hall.objects.get(hall_id = pk)
            if student.payment_made == True:
                messages.warning(request, "You have already made payment and hostel should have been allocated you.")
            else:
                stripe.api_key = settings.STRIPE_SECRET_KEY
                #payment logic
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types = ['card'],
                    line_items = [
                        {
                            'price_data': {
                                'currency': 'USD',
                                'product_data': {
                                    'name': hall.name,
                                },
                                'unit_amount': hall.price
                            },
                            'quantity': 1
                        }
                    ],
                    mode = 'payment',
                    success_url = f'{settings.REDIRECT_DOMAIN}allocation/payment_successful/{pk}/?session_id={{CHECKOUT_SESSION_ID}}',
                    # success_url = settings.REDIRECT_DOMAIN + 'allocation/payment_successful/?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url = settings.REDIRECT_DOMAIN + 'allocation/payment_cancelled?session_id={CHECKOUT_SESSION_ID}',
                )
                checkout_session_id = checkout_session.id,
                return redirect(checkout_session.url, code = 303)
        except Exception as e:
            messages.error(request, f"An error occurred:{e}")
            return redirect("allocation:hostel-list")
    
# class PaymentView(View):
#     template_name = 'hostel/payment.html'

#     def get(self, request, pk):
#         #get hall
#         hall = Hall.objects.get(hall_id = pk)
#         return render(request, self.template_name, {'hall':hall})
    
#     def post(self, request, pk):
#         student = Student.objects.get(user = request.user)
#         # alloc_student = AllocatedRooms.objects.get(student=student)
#         hall = Hall.objects.get(hall_id = pk)
        

#         if student.payment_made == True:
#             messages.warning(request, "You already paid for hostel and have been allocated a room")
#         else:
#             #allocate a temporary hall
            
#             #get allocated hall
#             try:
#                 with transaction.atomic():

#                     alloc_room = AllocatedRooms.objects.exists()

#                     if alloc_room:
#                         #get last room created
#                         room = Room.objects.filter(hall=hall).last()
#                         if room is not None:
#                             print(f"room occ - {room.room_num} - {room.current_occupancy}")
#                             if room.current_occupancy < 4:
#                                 AllocatedRooms.objects.create(student = student, room = room)
#                                 room.current_occupancy += 1
#                                 room.save()
                                
#                             else:
#                                 #create another room
#                                 if hall.room_number <= 0 and hall.status == 'unavailable':
#                                     student.payment_made = False
#                                     student.save()
#                                     messages.error(request, "Hall is occupied, kindly select another hall")
#                                     # return redirect('allocation:hostel-list')
#                                 else:
#                                     hall.room_number -= 1

#                                     if hall.room_number <= 0:
#                                         hall.status = 'unavailable'
                                    
#                                     new_room = Room.objects.create(hall=hall, room_num=room.room_num + 1)
#                                     AllocatedRooms.objects.create(student = student, room = new_room)
#                                     new_room.current_occupancy += 1
#                                     new_room.save()
#                                     hall.save()             
#                         else:
#                             #create a new room
#                             new_room = Room.objects.create(hall=hall, room_num=1)
#                             AllocatedRooms.objects.create(student = student, room = new_room)
#                             new_room.current_occupancy += 1
#                             new_room.save()
                            
#                     else:
#                         room = Room.objects.create(hall=hall, room_num = 1)
#                         AllocatedRooms.objects.create(student = student, room = room)
#                         room.current_occupancy += 1
#                         room.save()
#                         messages.success(request, "You have been allocated a room5")   

#                     stripe.api_key = settings.STRIPE_SECRET_KEY
#                     #payment logic
#                     checkout_session = stripe.checkout.Session.create(
#                         payment_method_types = ['card'],
#                         line_items = [
#                             {
#                                 'price_data': {
#                                     'currency': 'USD',
#                                     'product_data': {
#                                         'name': hall.name,
#                                     },
#                                     'unit_amount': hall.price
#                                 },
#                                 'quantity': 1
#                             }
#                         ],
#                         mode = 'payment',
#                         success_url = settings.REDIRECT_DOMAIN + 'allocation/payment_successful?session_id={CHECKOUT_SESSION_ID}',
#                         cancel_url = settings.REDIRECT_DOMAIN + 'allocation/payment_cancelled?session_id={CHECKOUT_SESSION_ID}',
#                     )
#                     return redirect(checkout_session.url, code = 303)
#                     # raise Exception("Payment Failed. Retry")
        
#             except Exception as e:
#                 print(e)
#                 messages.error(request, f"An error occurred: {e}")
#                 return redirect("allocation:hostel-list")
                 

#         return render(request, self.template_name, {'hall':hall})
    

class PaymentSuccessfulView(View):
    def get(self, request, pk):
        checkout_session_id = request.GET.get('session_id', None)
        user_id = request.user.user_id

        # user_payment = Student.objects.get(user=user_id)
        

        student = Student.objects.get(user = request.user)
        hall = Hall.objects.get(hall_id = pk)
            #get allocated hall
        try:
            with transaction.atomic():

                alloc_room = AllocatedRooms.objects.exists()

                if alloc_room:
                    #get last room created
                    room = Room.objects.filter(hall=hall).last()
                    if room is not None:
                        print(f"room occ - {room.room_num} - {room.current_occupancy}")
                        if room.current_occupancy < 4:
                            AllocatedRooms.objects.create(student = student, room = room)
                            room.current_occupancy += 1
                            room.save()
                            
                        else:
                            #create another room
                            if hall.room_number <= 0 and hall.status == 'unavailable':
                                student.payment_made = False
                                student.save()
                                messages.error(request, "Hall is occupied, kindly select another hall")
                                # return redirect('allocation:hostel-list')
                            else:
                                hall.room_number -= 1

                                if hall.room_number <= 0:
                                    hall.status = 'unavailable'
                                
                                new_room = Room.objects.create(hall=hall, room_num=room.room_num + 1)
                                AllocatedRooms.objects.create(student = student, room = new_room)
                                new_room.current_occupancy += 1
                                new_room.save()
                                hall.save()             
                    else:
                        #create a new room
                        new_room = Room.objects.create(hall=hall, room_num=1)
                        AllocatedRooms.objects.create(student = student, room = new_room)
                        new_room.current_occupancy += 1
                        new_room.save()
                        
                else:
                    room = Room.objects.create(hall=hall, room_num = 1)
                    AllocatedRooms.objects.create(student = student, room = room)
                    room.current_occupancy += 1
                    room.save()
                    messages.success(request, "You have been allocated a room5")   

                
                # raise Exception("Payment Failed. Retry")
    
        except Exception as e:
            print(e)
            messages.error(request, f"An error occurred: {e}")
            return redirect("allocation:hostel-list")
        
        student.stripe_checkout_id = checkout_session_id
        student.payment_made = True
        student.save()
        messages.success(request, "You have been allocated to a room")
                 
        return redirect('allocation:allocated-room')

class PaymentCancelledView(View):
    def get(self, request):
        messages.warning(request, "Payment Cancelled, try again")
        return redirect("allocation:hostel-list")

@csrf_exempt
def stripe_webhook(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY
	time.sleep(10)
	payload = request.body
	signature_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
		)
	except ValueError as e:
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		return HttpResponse(status=400)
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		session_id = session.get('id', None)
		time.sleep(15)
		user_payment = Student.objects.get(stripe_checkout_id=session_id)
		user_payment.payment_made = True
		user_payment.save()
	return HttpResponse(status=200)



@method_decorator(redirect_anonymous_user, name='get')
class AllocatedRoomView(View):
    template_name = "hostel/allocated_room.html"

    def get(self, request):
        try:
            student = Student.objects.get(user = request.user)
            alloc_room = AllocatedRooms.objects.get(student = student)

        except AllocatedRooms.DoesNotExist:
            messages.warning(request, "You have not been allocated a room")
            return redirect('allocation:hostel-list')

        return render(request, self.template_name, {'alloc_room':alloc_room})
    
@method_decorator(redirect_anonymous_user, name='get')
class RegisteredStudentsView(View):
    template_name = "hostel/registered-students.html"

    def get(self, request):
        reg_stds = Student.objects.all()
        form = FilterForm()
        return render(request, self.template_name, {'students':reg_stds, 'form':form})
    
    def post(self, request):
        form = FilterForm(request.POST)
        
        gender = request.POST.get('gender')
        level = request.POST.get('level')
        department = request.POST.get('department')
        payment = request.POST.get('payment')

        if payment == 'paid':
            if department != '':
                filtered_query = Student.objects.filter(
                level = level,
                department = department,
                user__gender = gender,
                payment_made = True
                )
            else:
                filtered_query = Student.objects.filter(
                level = level,  
                user__gender = gender,
                payment_made = True
                )
        else:
            if department != '':
                filtered_query = Student.objects.filter(
                level = level,
                department = department,
                user__gender = gender,
                payment_made = False
                )
            else:
                filtered_query = Student.objects.filter(
                level = level,  
                user__gender = gender,
                payment_made = False
                )

        return render(request, self.template_name, {'students':filtered_query,'form':form, 'filtered':filtered_query})
    

class AllocatedStudentsView(View):

    def get(self, request):
        alloc_std = AllocatedRooms.objects.all()
        return render(request, "hostel/allocated-students.html", {'alloc_stds':alloc_std})
    
class AllocatedHallView(View):

    def get(self, request, pk):
        alloc_hall = AllocatedRooms.objects.filter(room__hall__hall_id=pk)
        return render(request, "hostel/allocated-students.html", {'hall':alloc_hall})
    
        


