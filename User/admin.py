from django.contrib import admin

from .models import MyUser,Advisor
# Register your models here.
admin.site.register(MyUser)
admin.site.register(Advisor)