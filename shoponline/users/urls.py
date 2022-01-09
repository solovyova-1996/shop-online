from django.urls import path

from .views import LoginLoginView, Register, Logout, Profile, verify

app_name = 'users'
urlpatterns = [path('login/', LoginLoginView.as_view(), name='login'),
               path('register/', Register.as_view(), name='register'),
               path('logout/', Logout.as_view(), name='logout'),
               path('profile/', Profile.as_view(), name='profile'),
               path('verify/<str:email>/<str:activation_key>/', verify,
                    name='verify'),]
