from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect,render
import random
from django.core.mail import send_mail
from django.contrib.auth import login,authenticate,logout
from django.urls import reverse
from .models import *
import base64
from django.core.files.base import ContentFile
# Create your views here.

def home(request):
    return render(request,'home.html')

def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        AOU = authenticate(username=username,password=password)
        if AOU and AOU.is_superuser:
            login(request,AOU)
            return redirect('employeelist')
    return render(request,'adminlogin.html')

def employeelogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        AOU = authenticate(username=username,password=password)
        if AOU and AOU.is_active and not AOU.is_superuser:
            login(request,AOU)
            return redirect('delivery_status')
        else:
            return HttpResponse('Inavlid Creadentials')
    return render(request,'employeelogin.html')

def employeesignup(request):

    if request.method=='POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p1 = request.POST.get('password')
        p2 = request.POST.get('cpassword')
        if p1==p2:
            try:
                usr = User.objects.create_user(username=u,email=e,password=p1)
                usr.save()
                return redirect('employeelogin')
            except :
                return HttpResponse('Invalid Creadentials')
        else:
            return redirect('employeesignup')
    return render(request,'employeesignup.html')

def customerlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        obj = Customer.objects.filter(name=username,password=password)
        if obj:
            request.session['username']=obj[0].name
            return HttpResponseRedirect(reverse('track'))
        else:
            return HttpResponse('Inavlid Creadentials')
    return render(request,'customerlogin.html')

def customersignup(request):

    if request.method=='POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p1 = request.POST.get('password')
        p2 = request.POST.get('cpassword')
        add = request.POST.get('address')
        if p1==p2:
            try:
                usr = Customer.objects.create(name=u,email=e,password=p1,address=add)
                usr.save()
                return redirect('customerlogin')
            except :
                return HttpResponse('Invalid Creadentials')
        else:
            return redirect('customersignup')
    return render(request,'customersignup.html')

def employeelist(request):
    obj = []
    for i in User.objects.all():
        if not i.is_superuser:
            obj.append(i)
    return render(request,'employeelist.html',{'All':obj})

def customerlist(request):
    obj = Customer.objects.all()
    return render(request,'customerlist.html',{'All':obj})

def order_create(request):
    obj = []
    for i in User.objects.all():
        if not i.is_superuser:
            obj.append(i)
    cobj = Customer.objects.all()
    print(request.POST,request.FILES)
    if request.method == 'POST':
        cnameid = request.POST.get('cname')
        name = request.POST.get('name')
        image = request.FILES.get('image')
        price = request.POST.get('price')
        details = request.POST.get('boydetails')
        cus = Customer.objects.get(pk=cnameid)
        boy = User.objects.get(pk=details)
        Order.objects.create(customer_name=cus,product_name=name,product_img=image,product_price=price,delivery_boy=boy)
    return render(request,'order.html',{'emp':obj,'cus':cobj})

def delivery_status(request):

    if request.user.is_superuser:
        obj = Order.objects.all()
    else:
        obj = Order.objects.filter(delivery_boy=request.user)
    state = {'Order Confirm':'Order Confirm','Dispatch':'Dispatch','Delivered':'Delivered'}
    return render(request,'deliverystatus.html',{'feed':obj,'state':state})

def camera(request,id,n):
    if request.method == 'POST':
        data = request.POST.get('image')
        data = data[data.index(',')+1:]
        bytdecode = base64.b64decode(data)
        image = ContentFile(bytdecode,'items.png')
        if n == 1:
            obj = Order.objects.get(id=id)
            obj.delivered_img = image
            obj.save()
            return redirect('deliver_status')
        else:
            obj = Order.objects.get(id=id)
            obj.invoice_img = image
            obj.save()
            return redirect('deliver_status')
        
    return render(request,'camera.html',{'id':id,'n':n})

def success(request,id):
    obj = Order.objects.get(id=id)
    if request.method == 'POST':
        obj.status = request.POST.get('state')
    obj.save()
    return redirect('delivery_status')

def track(request):
    d={'hide':False}
    if request.session.get('username'):
        user=request.session.get('username')
        cus = Customer.objects.get(name=user)
        detail = Order.objects.filter(customer_name=cus)
        d['detail']=detail
        d['hide']=True
        
    return render(request,'track.html',d)

def logoutall(request):
    logout(request)
    return redirect('home')

def forget(request):
    global otp,obj
    
    if request.method == 'POST':
        un = request.POST.get('username')
        uo = Customer.objects.filter(name=un)
        
        if uo:
            obj = uo[0]
            name = obj.name
            email = obj.email
            subject = 'Forget Password'
            otp = random.randint(1000,9999)
            
        else:
            return HttpResponse(f'{un} user does not exist')
        
        send_mail(
            subject,
            f'Delivery System \n OTP: {otp} \n Username:{name}',
            'darksimmon1@gmail.com',
            [email],
            fail_silently=True,
        )
        return redirect('otp')
        
    return render(request,'forget.html')

def otp_p(request):
    
    if request.method == 'POST':
        sotp = request.POST.get('OTP')
        if otp == int(sotp):
            return redirect('change_password')
        else:
            return HttpResponse('Inavlid OTP')
            
    return render(request,'otp.html')

def change_password(request):
    if request.method == 'POST':
        pass1=request.POST.get('password')
        pass2=request.POST.get('cpassword')
        if pass1 == pass2:
            obj.password = pass1
            obj.save()
            send_mail(
            'From : Delivery System',
            f'Your Password has been changed Successfully',
            'darksimmon1@gmail.com',
            [obj.email],
            fail_silently=True,
            )
            return redirect('home')
        else:
            return HttpResponse('Password is not match!!')
        
    return render(request,'change_password.html')


def pic(request,id,n):
    obj = Order.objects.get(id=id)
    d={"order":obj}
    if n==1:
        d['img']=True
    else:
        d['img']=False
    return render(request,'pic.html',d)