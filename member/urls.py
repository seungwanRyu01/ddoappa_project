from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('check_id/', views.check_id, name='check_id'),
    path('mypage/', views.myPage, name = 'mypage'),
    path('updateuserPage/', views.updateUserPage, name='updateuserPage'),
    path('updateuser/', views.updateUser, name='updateuser'),
    path('deleteuserPage/', views.deleteUserPage, name='deleteuserPage'),
    path('deleteuser/', views.deleteUser, name='deleteuser')
    ]
