from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Tix

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def tix_index(request):
    tix = Tix.objects.filter(user=request.user)
    return render(request, 'tix/index.html', {'tix': tix})

@login_required
def tix_detail(request, tix_id):
    tix = Tix.objects.get(id=tix_id)
    return render(request, 'tix/detail.html', {'tix': tix})

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class TixCreate(CreateView):
    model = Tix
    fields = ['event_name', 'venue', 'location', 'date']
    success_url = '/tix/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TixUpdate(UpdateView):
    model = Tix
    fields = ['event_name', 'venue', 'location', 'date']

class TixDelete(DeleteView):
    model = Tix
    success_url = '/tix/'