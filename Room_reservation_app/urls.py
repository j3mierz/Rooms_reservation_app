"""
URL configuration for Room_reservation_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.HomePage.as_view(), name='home'),
    path('home/add_room/', views.AddRoom.as_view(), name='add_room'),
    path('home/edit_room/<int:pk>/', views.EditRoom.as_view(), name='edit_room'),
    path('home/delete_room/<int:pk>/', views.DeleteRoom.as_view(), name='delete_room'),
    path('home/room/<int:pk>/', views.RoomsView.as_view(), name='room'),
]
