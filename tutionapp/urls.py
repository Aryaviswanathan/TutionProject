from django.urls import path,include
from .import views


urlpatterns=[

    path('',views.home,name="home"),
    path('loginpage',views.loginpage,name="loginpage"),
    path('tsignup',views.tsignup,name="tsignup"),
    path('stsignup',views.stsignup,name="stsignup"),

    path('adminhome',views.adminhome,name="adminhome"),
    path('teacherhome',views.teacherhome,name="teacherhome"),
    path('studenthome',views.studenthome,name="studenthome"),

    path('add_techer',views.add_techer,name="add_techer"),
    path('add_student',views.add_student,name="add_student"),

    path('login1',views.login1,name="login1"),
    path('admin_view',views.admin_view,name="admin_view"),
    path('apv_dpv',views.apv_dpv,name="apv_dpv"),
    path('approve/<int:k>',views.approve,name="approve"),
    path('disapprove/<int:k>',views.disapprove,name="disapprove"),
    path('reset_pwd',views.reset_pwd,name="reset_pwd"),
    path('reset',views.reset,name="reset"),



    path('logout',views.logout,name="logout"),




]