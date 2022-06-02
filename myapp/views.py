from random import randrange
from django.shortcuts import redirect, render
from django.conf import settings
from django.core.mail import send_mail


from seller.models import *
from .models import *

# Create your views here.
def index(request):
    try:
        userobj= User.objects.get(email=request.session['email'])
        return render(request,'index.html',{'session_user':userobj})
    except:
        return render(request, 'index.html')
    

def about(request):
    
    return render(request,'about.html')

def logout(request):
    try:
        request.session['email']
        del request.session['email']
        return render(request, 'login.html')
    except:
        return render(request, 'login.html')

def login(request):
    if request.method=='POST':
        try:
            userobj= User.objects.get(email=request.POST['email'])
            if request.POST['password']==userobj.password:
                request.session['email'] = request.POST['email']
                return render(request, 'index.html',{'session_user':userobj})
            else:
                return render(request,'login.html',{'msg':'Invalid password'})
        except:
            return render(request,'login.html',{'msg':'email not found'})
    return render(request,'login.html')

def register(request):
    if request.method=='POST':
        # Email already
        if request.POST['password']==request.POST['cnfpassword']:
            global otp
            otp = randrange(1000,9999)
            subject = 'welcome to GFG world'
            message = f'Hi this is your otp {otp}, thank you for registering in geeksforgeeks.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'], ]
            send_mail( subject, message, email_from, recipient_list )
            return render(request, 'otp.html')
            # User.objects.create(
            #     name=request.POST['name'],
            #     email=request.POST['email'],
            #     password=request.POST['password']
            # )
            # return redirect('login')
        else:
            return render(request,'register.html',{'msg':'passwords do not match'})
    return render(request,'register.html')

def otp(request):
    if request.method == 'POST':
        if otp == request.POST['otp']:
            return render(request,'login.html')
        else:
            return render(request,'otp.html', {'otp':'Wrong otp'})


def products(request):
    plist = Product.objects.all()
    return render(request,'products.html',{'productlist':plist})