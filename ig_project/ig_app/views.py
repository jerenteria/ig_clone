from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .forms import *

# Create your views here.

def index(request):
    return render(request, "index.html")

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, "home.html")

def register(request):
    if request.method=='POST':
        # validate the data
        errors=User.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect("/")
        ## encrypting our password
        ## store plaintext password in variable
        user_pw=request.POST['pw']
        ## hash the password
        hash_pw=bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        #test
        print(hash_pw)
        new_user=User.objects.create(user_name=request.POST['user_name'], password=hash_pw)
        print(new_user)
        request.session['user_id']=new_user.id
        request.session['user_handle']=f"{new_user.user_name}"
        return redirect('/home')
    return redirect('/')

def login(request):
    ## loging a user in
    if request.method=='POST':
        ## query for logged user
        logged_user=User.objects.filter(user_name=request.POST['user_name'])
        if logged_user:
            logged_user=logged_user[0]
            request.session['user_id']=logged_user.id
            request.session['user_handle']=f"{logged_user.user_name}"
        return redirect('/home')
    return redirect('/')

def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'index.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'home.html', {'form': form})

def terms_conditions(request):
    return render(request, "terms_conditions.html")