
from django.shortcuts import render,redirect
from .models import Users
from django.contrib.auth import login

def index(request):
    return render(request, 'signup.html')

def signup(request):
    if request.method == 'POST':
        if request.POST['password'] != request.POST['repassword']:
            context = {'msg': 'Password does not match!!'}
            return render(request, 'signup.html', context)
        user = Users(firstName=request.POST['firstname'], lastName=request.POST['lastname'], email=request.POST['email'], userName=request.POST['username'], password=request.POST['password'], uvaHandle=request.POST['uvahandle'], phone=request.POST['phone'],codeforcesHandle=request.POST['codeforceshandle'],lightOJ=request.POST['lightoj'])
        user.save()
        context = {'msg': 'Registration Successfull!!'}
        return redirect('/login', context)
    else:
        context = {'msg': 'Registration Failed'}
        return render(request, 'signup.html', context)

def login(request):
    return render(request, 'login.html')

def home(request):
    try:
        if request.method == 'POST':
            if Users.objects.filter(email=request.POST['email'], password=request.POST['password']).exists():
                user = Users.objects.get(email=request.POST['email'], password=request.POST['password'])
                request.session['user']=user.id
                login(request)
                context = {'msg': ''}
                return render(request, 'home.html', context)
            else:
                context = {'msg': 'Invalid username or password'}
                return render(request, 'login.html', context)
    except:
        context = {'msg': 'Invalid username or password'}
        return render(request, 'login.html', context)