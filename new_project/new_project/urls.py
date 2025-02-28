"""
URL configuration for new_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from newapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/', views.create_post, name ='create_post'),
    path('getall/', views.get_all, name ='get_all'),
    path('get/', views.get_one_data, name ='get_one_data'),
    path('edit/', views.update_data, name ='update_data'),
    path('deleteone/', views.delete_one, name ='delete_one'),
    path('deleteall/', views.delete_all_data, name ='delete_all_data'),
]
