# bixadmin/core/admin.py

from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.shortcuts import redirect


class CustomAdminSite(AdminSite):
    site_header = "BixAdmin"
    site_title = "BixAdmin Portal"
    index_title = "Benvenuto in BixAdmin"

    def login(self, request, extra_context=None):
        if request.user.is_authenticated:
            return redirect('/scheduler/')  # cambia l'URL se vuoi un altro redirect
        return super().login(request, extra_context=extra_context)
    
    def logout(self, request):
        response = super().logout(request)
        return redirect('/login/')

# Istanza del custom admin<
custom_admin_site = CustomAdminSite(name='custom_admin')

# Registra i modelli che vuoi mostrare nell'admin
custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Group, GroupAdmin)
