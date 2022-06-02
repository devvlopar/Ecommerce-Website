from django.shortcuts import redirect, render

from seller.models import *

# Create your views here.

def dashboard(request):
    return render(request,'dashboard.html')

def seller_login(request):
    if request.method=='POST':
        try:            
            sellerobj = SellerUser.objects.get(email=request.POST['email'])
            if request.POST['password']==sellerobj.password:
                request.session['email']=request.POST['email']
                request.session['name']=sellerobj.name
                return redirect(dashboard)
            else:
                return render(request,"seller-login.html",{'msg':'Invalid password'})
        except:
            return render(request,"seller-login.html",{'msg':'email not registered'})
    return render(request,"seller-login.html")

def add_product(request):
    if request.method=='POST':
        sellerobj=SellerUser.objects.get(email=request.session['email'])
        if 'pic' in request.FILES:
            Product.objects.create(
                name=request.POST['name'],
                des=request.POST['des'],
                price=request.POST['price'],
                quantity=request.POST['quantity'],
                discount=request.POST['dis'],
                seller=sellerobj,            
                pic = request.FILES['pic']
            )
        else:
            Product.objects.create(
                name=request.POST['name'],
                des=request.POST['des'],
                price=request.POST['price'],
                quantity=request.POST['quantity'],
                discount=request.POST['dis'],
                seller=sellerobj
                #pic = request.FILES['pic']
            )
    return render(request,'add-product.html')

def manage_products(request):
    plist = Product.objects.all()
    return render(request,'manage-products.html',{'productlist':plist})

def delete_product(request,pid):
    pobj = Product.objects.get(id=pid)
    pobj.delete()
    return redirect('manage-products')

def edit_product(request,pid):
    pobj = Product.objects.get(id=pid)    
    if request.method == 'POST':
        pobj.name = request.POST['name']
        pobj.des = request.POST['des']
        pobj.price = request.POST['price']
        pobj.quantity = request.POST['quantity']
        pobj.discount = request.POST['dis']
        pobj.save()
        return redirect('manage-products')
    return render(request,'edit-product.html',{'item':pobj})