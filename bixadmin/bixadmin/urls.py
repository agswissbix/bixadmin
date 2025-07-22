"""
URL configuration for bixadmin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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


# bixadmin/urls.py
from django.urls import path, include
from bixadmin.core.admin import custom_admin_site
from bixscheduler import views as scheduler_views
from bixsettings import views as settings_views

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('login/', custom_admin_site.login, name='admin_login'),
    path('logout/', custom_admin_site.logout, name='admin_logout'),
    path('scheduler/', scheduler_views.index, name='scheduler_index'),
    path('settings/', settings_views.index, name='settings_index'),
]

