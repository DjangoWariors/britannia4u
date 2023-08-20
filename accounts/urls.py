from django.urls import path, include

from . import views

urlpatterns = [
    # path('', views.myAccount),
    path('user-master/', views.userMaster, name='user-master'),
    path('register-user/', views.registerUser, name='register-user'),
    path('upload-csv/', views.upload_csv, name='upload-csv'),
    path('', views.send_otp, name='send-otp'),
    path('accounts/send-otp/', views.send_otp, name='send-otp'),
    path('login', views.send_otp, name='send-otp'),
    path('accounts/otp-verification/', views.otp_verification, name='otp-verification'),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('admin-dashboard/', views.adminDashboard, name='admin-dashboard'),

    path('upload-user/', views.upload_user, name='upload-user'),

    path('user-profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('update-user/<str:pk>/', views.updateUser, name='update-user'),
    path('delete-user/<str:pk>/', views.delete_user, name='delete-user'),
    path('reset-password/<str:pk>', views.reset_password, name='reset-password'),

]