from django.urls import path
from .views import *

urlpatterns = [
    path('', register, name="register-page"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path('update/', edit_profile, name="update")
]
