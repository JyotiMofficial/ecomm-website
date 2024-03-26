from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from products.models import Product, SizeVariant
from .models import Profile, Cart, cartItems, Coupon, banner
from django.conf import settings
import razorpay



# Create your views here.



# Create your views here.
def login_page(request):
     if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        userobj=User.objects.filter(username=email)
        
        if not userobj.exists():
            messages.warning(request,'account not found')
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request,'account is not verified')
            return HttpResponseRedirect(request.path_info)
            
            
            
        
        user_obj=authenticate(request,username=email, password=password)
        if user_obj :
            login(request , user_obj)
            return redirect('/')
    
        
        messages.warning(request,'invaild credentials')
        return HttpResponseRedirect(request.path_info)
     return render(request, 'accounts/login.html')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        userobj=User.objects.filter(username=email)
        
        if userobj.exists():
            messages.warning(request,'email is already registered.')
            return HttpResponseRedirect(request.path_info)
        print(email)
    
        user_obj =User.objects.create(first_name=first_name,last_name=last_name, email=email, password=password, username=email)
        user_obj.set_password(password)
        user_obj.save()
        
        messages.success(request,'account is created successfully')
        return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/register.html')


def activate_email(request , email_token):
    try:
        user = Profile.objects.get(email_token= email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid Email token')


def add_to_cart(request, uid):
    variant= request.GET.get("variant")
    product=Product.objects.get(uid=uid)
    user= request.user
    cart , _ =Cart.objects.get_or_create(user=user, is_paid=False)
    cart_item=cartItems.objects.create(cart=cart, product=product)
    if variant:
        variant = request.GET.get('variant')

        size_variant= SizeVariant.objects.get(size_name=variant)
        cart_item.size_variant= size_variant
        cart_item.save()
            
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
def remove_cart(request, cart_item_uid):
    try:
         cart_item=cartItems.objects.get(uid=cart_item_uid)
         cart_item.delete()
        
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        
   

def cart(request):
   try:
       cart_obj=None 
       cart_obj=Cart.objects.get(is_paid=False, user =request.user)
   except Exception as e:
       print(e)
   
   
   if request.method=='POST':
       coupon=request.POST.get('coupon')
      
       coupon_obj=Coupon.objects.filter(coupon_code__icontains = coupon)
       
       if not coupon_obj.exists():
           messages.warning(request,'invalid Coupon. ')
           return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
       
       if cart_obj.coupon:
           messages.warning(request,"coupon already exist")    
           return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
       if cart_obj.get_cart_total() < coupon_obj[0].minimum_amount:
            messages.warning(request,f'amount should be grater than{ coupon_obj[0].minimum_amount}' )
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
        
       if coupon_obj[0].is_expired:
             messages.warning(request,f'coupon is expired' )
             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
        
       cart_obj.coupon=coupon_obj[0]
       cart_obj.save() 
       
       messages.success(request,'applied ')
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
       
       
   if cart_obj:
        client= razorpay.Client(auth=('rzp_test_Xwt94kP54nVmzV' , 'cDX6WT0oM4Fmi9i70AerzEpJ'))
        payment= client.order.create({'amount':cart_obj.get_cart_total()*100,'currency':'INR', 'payment_capture':1})
        cart_obj.razor_pay_order_id=payment['id']
        cart_obj.save()
        
        print("*********")
        print(payment)
        print("*********")
    
   

   payment=None
   context={'cart':cart_obj,'payment':payment}
   return render(request,"accounts/cart.html",context )


def remove_coupon(request, cart_id):
    cart=Cart.objects.get(uid=cart_id)
    cart.coupon=None
    cart.save()
    
    messages.success(request,'coupon removed ')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def success(request):
    order_id=request.GET.get('order_id')
    cart=Cart.objects.get(razor_pay_order_id=order_id)
    cart.is_paid=True
    cart.save()
    return HttpResponse('payment success')

def home(request):
     slider=banner.objects.all()
     context={
         'slider':slider
     }
     return render(request,'index.html', context)
     
     
