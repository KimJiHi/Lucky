from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage),
    path('register/', views.register),
    path('checkuserid/', views.checkuserid),
    path('login/', views.login),
    path('checklogin/', views.checklogin),
    path('home/', views.home),
    path('homelist/', views.homelist),
    path('dslist/', views.dslist),
    path('jrlist/', views.jrlist),
    path('fhlist/', views.fhlist),
    path('sjlist/', views.sjlist),
    path('djlist/', views.djlist),
    # path('home/type/<int:num>', views.hometype),
    # path('home/guess/', views.homeguess),
    path('release/',views.release),
    path('logout/', views.quit),
    path('prize/<int:num>/', views.prize),
    path('checkPrize/', views.checkPrize),
    path('mine/', views.mine),
    path('mine/<int:num>/', views.mine2)
]
