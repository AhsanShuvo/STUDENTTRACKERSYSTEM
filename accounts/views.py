
from django.shortcuts import render,redirect
from .models import Profile
from django.contrib.auth import login,authenticate,logout 
from .forms import UserForm
from django.contrib.auth.models import User
import requests
from django.contrib.auth.decorators import login_required

def index(request):
    
    if request.user.is_authenticated:
        return redirect('app/')

    return render(request,'signup.html')

def Login(request):
    if request.user.is_authenticated:
        print("it going here")
        return redirect('/')
    if request.method== "POST":
        username= request.POST['username']
        password= request.POST['password']
        print("or Here")
        print(username, password)
        user=authenticate(username=username, password= password)
        if user is not None:
            print("Then Here")
            if user.is_active:
                print("then .... ")
                login(request,user)
                if user.is_authenticated:
                    print("Yes It works")
                    return redirect('/')
        return render(request,'login.html',{'msg':"Invalid Login"})
    else:
        print("GET REQEUST!")
        return render(request,'login.html')

def signup(request):

    if request.user.is_authenticated:
        return render(request,'/',{})

    form = UserForm(request.POST or None)
    if request.method == 'POST':
        print("step 2")
        if form.is_valid():
            user = form.save(commit= False)
            username= form.cleaned_data['username']
            password= form.cleaned_data['password']
            user.set_password(password)
            user.save()
            authenticate(username= username, password= password)
            Profile.objects.create(
                user=  user,
                full_name=form.cleaned_data['full_name'],
                codeforces_id= form.cleaned_data['codeforces_id'],
                Uva_Id = form.cleaned_data['Uva_Id'],
                points = 0,
                department= form.cleaned_data['department'],
                red_mark =False
            )
            
            return render(request, 'login.html',{'msg':'Works'})
        else:
            error = form.errors
            print("error step")
            return render(request, 'signup.html',{'msg':error})

    
    else:
        return render(request,'signup.html',{})
@login_required
def Logout(request):
    logout(request)
    return redirect('/login') 
   