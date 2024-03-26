from django.contrib import admin
from .models import Profile, Cart, cartItems, logos, banner

# Register your models here.
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(cartItems)
admin.site.register(logos)
admin.site.register(banner)
