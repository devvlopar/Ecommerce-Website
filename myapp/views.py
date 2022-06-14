from random import randrange
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.core.mail import send_mail
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
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


def cart(request):
    userobj= User.objects.get(email=request.session['email'])
    cart_data = Cart.objects.filter(userid=userobj)
    return render(request,'cart.html',{'cartdata':cart_data})


def delete_cart(request,pk):
    cart_item = Cart.objects.get(id=pk)
    cart_item.delete()
    userobj= User.objects.get(email=request.session['email'])
    cart_data = Cart.objects.filter(userid=userobj)
    return render(request, 'cart.html',{'cartdata':cart_data})

def add_to_cart(request,pk):
    product_obj = Product.objects.get(id=pk)
    userobj= User.objects.get(email=request.session['email'])
    Cart.objects.create(
        productid = product_obj,
        userid = userobj,
    )
    return redirect('products')



# Razorpay Integration

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def homepage(request):
    currency = 'INR'
    userobj= User.objects.get(email=request.session['email'])
    cart_data = Cart.objects.filter(userid=userobj)
    tamount = 0
    for i in cart_data:
        tamount += i.productid.price 


    amount = tamount*100  # Rs. 200
    
    global g_amount
    g_amount = amount
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['totalamount'] = amount/100
 
    return render(request, 'index1.html', context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            # verify the payment signature.
            # result = razorpay_client.utility.verify_payment_signature(
            #     params_dict)
            # if result is None:
            amount = g_amount  
            try:

                # capture the payemt
                razorpay_client.payment.capture(payment_id, amount)

                # render success page on successful caputre of payment
                return render(request, 'paymentsuccess.html')

            except:

                # if there is an error while capturing payment.
                return render(request, 'paymentfail.html')
            # else:
 
            #     # if signature verification fails.
            #     return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()