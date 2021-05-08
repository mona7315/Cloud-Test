from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import redirect, render
from user.models import Booking, Room
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def my_login(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password'
            return render(request, 'guest/login.html', context=context)
    
    return render(request, 'guest/login.html', context=context)


def my_logout(request):
    logout(request)
    return redirect('login')
  
    
def register(request):
    context = {}

    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        email = request.POST.get('email')

        try:
            user = User.objects.get(username=request.POST.get('username'))
            
        except ObjectDoesNotExist:
            user = None

        if user:
            context = {
                'error_user' : "username ซ้ำ"
            }
            return render(request, 'guest/register.html', context)

        if password == repassword:
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            group = Group.objects.get(name='myUser')
            user.groups.add(group)
            user.save
            return redirect('login')
        else:
            context['error'] = 'Password ซ้ำ'
            return render(request, 'guest/register.html', context=context)
     
    return render(request, 'guest/register.html')


