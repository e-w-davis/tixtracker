import re
import uu
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import uuid
import boto3
from .models import Tix, Photo

# Create your views here.
S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'tixtracker'
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

def add_photo(request, tix_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, tix_id=tix_id)
            photo.save()
        except:
            print('An error occured uploading file to S3')
    return redirect('detail', tix_id=tix_id)

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