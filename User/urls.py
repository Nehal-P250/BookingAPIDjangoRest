from django.contrib import admin
from django.urls import path,include

from User.views import (AdvisorView,
                        MyUserView,
                        LoginView,
                        GetAdvisorView,
                        BookAdvisorView,
                        GetBookingsView)

urlpatterns = [
    path('register',MyUserView.as_view()),
    path('login',LoginView.as_view()),
    path('<int:userID>/advisor/<int:advisorID>',BookAdvisorView.as_view()),
    path('<int:userID>/advisor/booking',GetBookingsView.as_view()),
    path('<int:userID>/advisor',GetAdvisorView.as_view())
    
]
 
