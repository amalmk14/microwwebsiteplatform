from django.urls import path
from . import views

app_name = 'customadmin'

urlpatterns = [
    path("",views.adminLogin,name="adminlogin"),
    path("adminhomel",views.adminLogout,name="adminlogout"),
    path("adminhome", views.adminHome, name="adminhome"),
    path("adminwidget",views.adminWidget,name="adminwidget"),
    path('adminprofile,',views.adminProfile,name='adminprofile'),
    path("admintable",views.adminTable,name="admintable"),
    path("admintable/<int:normal_id>/",views.delete_normal_temp,name="delete_normal_temp"),
    path('update_normal/<int:card_id>/',views.update_normal,name='update_normal'),
    path("admintablep",views.adminTableP,name="admintablep"),
    path("admintablep/<int:premium_id>/",views.delete_premium_temp,name="delete_premium_temp"),
    path('update_premium/<int:card_id>/',views.update_premium,name='update_premium'),
    path("adminform",views.adminForm,name="adminform"),
    path("adminformp",views.adminFormP,name="adminformp"),
    path('admincoupen',views.adminCoupen,name='admincoupen'),
    path('admincoupen/<int:c_id>/',views.deleteCoupen,name='deletecoupen'),
]