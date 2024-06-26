import uuid
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver 
from base.models import BaseModel
from django.db.models.signals import post_save
from base.email import send_account_activation_email
from products.models import Product, ColorVariant,  SizeVariant , Coupon


# Create your models here.
class Profile(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name="profile")
    is_email_verified=models.BooleanField(default=False)
    email_token=models.CharField(max_length=100, null=True, blank=True)
    profile_image=models.ImageField(upload_to='profile')
     
    def __str__(self) -> str:
        return f'{self.user} '

    
    def get_cart_count(self):
        return cartItems.objects.filter(cart__is_paid=False , cart__user=self.user).count()
    
    
 
class Cart(BaseModel):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    coupon=models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True,blank=True)
    is_paid=models.BooleanField(default=False)
    razor_pay_order_id=models.CharField(max_length=100,null=True, blank=True)
    razor_pay_payment_id=models.CharField(max_length=100,null=True, blank=True)
    razor_pay_payment_signature=models.CharField(max_length=100,null=True, blank=True)


    
    def __str__(self) -> str:
        return f'{self.user} '
    
    def get_cart_total(self):
        cart_items=self.cart_items.all()
        price=[]
        for cart_item in cart_items:
            price.append(cart_item.product.price)
            if cart_item.color_variant:
                color_variant_price=cart_item.color_variant.price 
                price.append(color_variant_price)
            if cart_item.size_variant:
                size_variant_price=cart_item.size_variant.price
                price.append(size_variant_price)
        
        if self.coupon:
            if self.coupon.minimum_amount< sum(price):
                return sum(price)-self.coupon.discount_price
        return sum(price)
        
    
    
class cartItems(BaseModel):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    color_variant = models.ForeignKey(ColorVariant,on_delete=models.SET_NULL, null=True, blank=True)
    size_variant =models.ForeignKey(SizeVariant,on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.product} '
    
    def get_product_price(self):
        price=[self.product.price]
        
        if self.color_variant:
            color_variant_price=self.color_variant.price
            price.append(color_variant_price)
        if self.size_variant:
            size_variant_price=self.size_variant.price
            price.append(size_variant_price)
        return sum(price)
        
    

    
    
@receiver(post_save, sender=User)
def send_email_token(sender, instance, created ,**kwargs):
    try:
        if created:
            email_token=str(uuid.uuid4())
            Profile.objects.create(user = instance , email_token = email_token)
            email=instance.email
            send_account_activation_email(email, email_token)
            
    except Exception as e:
        print(e)
class logos(BaseModel):
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    image = models.ImageField(max_length=255, upload_to='images')
    
    def __str__(self):
        return self.name
    
class banner(BaseModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(max_length=255, upload_to='images')
    desription = models.TextField()
    
    