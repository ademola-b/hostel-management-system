from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView


from .decorators import redirect_anonymous_user
from .models import Hall


# Create your views here.
class Onboard(TemplateView):
    template_name = "landing.html"

@method_decorator(redirect_anonymous_user, name='get')
class DashboardView(View, LoginRequiredMixin):
    def get(self, request):
        return render(request, "dashboard.html")
    
@method_decorator(redirect_anonymous_user, name='get')
class Hostels(ListView, LoginRequiredMixin):
    queryset = Hall.objects.all()
    template_name = 'hostel/select-hostel.html'

class PaymentView(View):
    template_name = 'hostel/payment.html'

    def get(self, request, pk):
        #get hall
        hall = Hall.objects.get(hall_id = pk)
        return render(request, self.template_name, {'hall':hall})


