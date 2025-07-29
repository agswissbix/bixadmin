# bixadmin/core/admin.py

from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect


class CustomAdminSite(AdminSite):
    site_header = "BixAdmin"
    site_title = "BixAdmin Portal"
    index_title = "Benvenuto in BixAdmin"

    def index(self, request, extra_context=None):
        """
        Redirect dalla pagina principale dell'admin a /scheduler/
        """
        if request.user.is_authenticated:
            return redirect('/settings/tables')
        return super().index(request, extra_context=extra_context)
    
    def logout(self, request, extra_context=None):
        """
        Gestisce il logout e redirect diretto alla pagina di login
        """
        from django.contrib.auth import logout
        from django.contrib.admin.sites import AdminSite
        
        # Eseguiamo il logout manualmente
        logout(request)
        
        # Redirect diretto senza passare per altri metodi
        return redirect('/login/')


# Istanza del custom admin
custom_admin_site = CustomAdminSite(name='custom_admin')

# Registra i modelli che vuoi mostrare nell'admin
custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Group, GroupAdmin)