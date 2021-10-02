from django.urls import path, re_path
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
    path('deleteuser/', views.deleteUser, name='deleteuser'),
    path('boardlist/', views.board_list, name='boardlist'),
    path('boardwrite/', views.board_write, name='boardwrite'),
    # re_path(r'^boarddetail/(?P<pk>[0-9]+)/$', views.board_detail, name='boarddetail'),
    path('boarddetail/<int:pk>/', views.board_detail, name='boarddetail'),
    path('boarddetail/<int:pk>/boarddelete/', views.board_delete, name='boarddelete'),
    path('boarddetail/<int:pk>/boardedit/', views.board_edit, name='boardedit')
    ]
