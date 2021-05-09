from django.contrib import admin

from .models import MyUser,Advisor,Booking
# Register your models here.
admin.site.register(MyUser)
admin.site.register(Advisor)
admin.site.register(Booking)