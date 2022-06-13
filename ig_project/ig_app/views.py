from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
import bcrypt
from django.core.files.storage import FileSystemStorage

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

def upload(request):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        return render(request, 'home.html', {'file_url': file_url})
    return render(request, 'home.html')

def like_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = Like.object.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value == 'Unlike'
            else:
                like.value = 'Like'
        like.save()
    return redirect (request, "home.html")

def terms_conditions(request):
    return render(request, "terms_conditions.html")

