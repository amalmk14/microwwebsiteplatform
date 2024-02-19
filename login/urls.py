from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    path("signin", views.signin, name="signin"),
    path("signup",views.signup,name="signup"),
    path('logout', views.logout, name='logout'),
    path("profile",views.profile,name="profile"),
    path("profile_password",views.profile_password,name="profile_password"),
    path("bill",views.bill,name="bill"),
    path("security",views.security,name="security"),

    # path('forget',views.forgot_password,name='forget'),
]