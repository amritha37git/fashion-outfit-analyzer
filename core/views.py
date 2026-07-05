from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

