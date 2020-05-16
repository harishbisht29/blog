from django.urls import path, include
from .views import signinView, signupView, signoutView
urlpatterns = [
    path('signin/', signinView,name='signin-url'),
    path('signup/', signupView, name='signup-url'),
    path('signout/', signoutView, name='signout-url'),

]