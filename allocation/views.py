from django.shortcuts import render
from django.views.generic import TemplateView, View


# Create your views here.
class Onboard(TemplateView):
    template_name = "landing.html"

class DashboardView(View):
    def get(self, request):
        return render(request, "dashboard.html")

