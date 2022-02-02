from tokenize import group
from django.http import HttpResponseRedirect
from django.shortcuts import render,HttpResponsePermanentRedirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import SignUpForm,LoginForm,PostForm
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group

# Create your views here.
def home(request):
    posts = Post.objects.all()
    return render(request,'storeapp/home.html',{'posts':posts})

def about(request):
    return render(request,'storeapp/about.html')    

def dashboard(request):
    if request.user.is_authenticated:
        posts =Post.objects.all()
        user = request.user
        full_name=user.get_full_name()
        groups = user.groups.all()
        return render(request,'storeapp/dashboard.html',{'posts':posts,'full_name':full_name,'groups':groups})
    else:    
        return render(request,'storeapp/dashboard.html')

def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name="Author")
            user.groups.add(group)
    else:        
        form = SignUpForm()
    return render(request,'storeapp/signup.html',{'form':form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/dashboard/')
        else:            
            form = LoginForm()
        return render(request,'storeapp/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')  


def update_post(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            pi=Post.objects.get(pk=id)   
            form=PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi=Post.objects.get(pk=id)
            form=PostForm(instance=pi)  
        return render(request, 'storeapp/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')              


def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                book_name = form.cleaned_data['book_name']
                book_desc = form.cleaned_data['book_desc']
                pst=Post(book_name=book_name, book_desc=book_desc)
                pst.save()
                form=PostForm()
        else:
            form=PostForm()
        return render(request,'storeapp/addpost.html',{'form':form}) 
    else:
        return HttpResponseRedirect('/login/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi=Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:        
        return HttpResponseRedirect('/login/')