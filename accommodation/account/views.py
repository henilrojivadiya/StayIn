from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.views import PasswordChangeView
from .forms import PasswordChangeingForm
from django import forms
from django.core.validators import validate_email
from django.urls import reverse_lazy
# from pro.models import House
from django.contrib import messages
from .models import User


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')    
    else:
        context = {}
        return render(request, 'login.html', context)

def registration(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if  User.objects.filter(phone_number=phone_number).exists() and User.objects.filter(email=email).exists():
                messages.info(request,'Phone Number and Email are alredy exists') 
                return redirect('user_registration')  
            elif User.objects.filter(phone_number=phone_number).exists():
                messages.info(request,'Phone Number is alredy exists') 
                return redirect('user_registration')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email is alreay exists')
                return redirect('user_registration')
            else:   
                user = User.objects.create_user(
                                first_name=first_name,
                                last_name=last_name,
                                phone_number=phone_number,
                                email=email,
                                password=password,
                )
                user.save()
                print('user created')
                return redirect('login')
        
        else:
            messages.info(request,'Password not matching')
            return redirect('user_registration')        

        return redirect('login')
    else:
        context = {}
        return render(request, 'registration.html', context)

class PasswordsChangeView(PasswordChangeView):
    template_name = 'password_change.html'
    form_class = PasswordChangeingForm
    success_url = reverse_lazy('index')
    # success_url = reverse_lazy('password_success')



# def user_settings_view(request):
#     context = { }
#     return render(request, 'user_settings.html', context)