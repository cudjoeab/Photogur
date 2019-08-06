"""photogur URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from photogur import views 

urlpatterns = [
    path('', views.pictures, name='homepage'),
    path('admin/', admin.site.urls),
    path('comments/new', views.create_comment, name='create_comment'),
    path('login/', views.login_view, name="login"), 
    # path('logout/', views.logout_view, name="logout"), 
    path('pictures/', views.pictures), 
    path('pictures/<int:id>', views.picture_show, name='picture_details'),
    path('search', views.picture_search, name='picture_search'),
]

