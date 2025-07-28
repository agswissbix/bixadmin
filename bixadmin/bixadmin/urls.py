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
from bixsettings.views import settings_view as settings_views
from bixmonitoring import views as monitoring_views

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('login/', custom_admin_site.login, name='admin_login'),
    path('logout/', custom_admin_site.logout, name='admin_logout'),
    path('loading/', scheduler_views.get_render_loading, name='loading'),

    path('scheduler/', scheduler_views.lista_schedule, name='lista_schedule'),
    path('scheduler/aggiungi/', scheduler_views.aggiungi_scheduler, name='aggiungi_scheduler'),
    path('scheduler/delete/<int:schedule_id>/', scheduler_views.delete_scheduler, name='delete_scheduler'),
    path('scheduler/run/<int:schedule_id>/', scheduler_views.run_scheduler_now, name='run_scheduler_now'),
    path('scheduler/toggle/<int:schedule_id>/', scheduler_views.toggle_scheduler, name='toggle_scheduler'),

    path('monitoring/', monitoring_views.lista_monitoring, name='lista_monitoring'),

    path('settings/tables', settings_views.settings_table, name='settings_table'),
    path('settings/users', settings_views.settings_user, name='settings_users'),
    
    path('settings/charts', settings_views.settings_charts, name='settings_charts'),
    path('save_users_dashboards/', settings_views.save_users_dashboards, name='save_users_dashboards'),
    path('new_chart_block/', settings_views.new_chart_block, name='new_chart_block'),
    path('new_report/', settings_views.new_report, name='new_report'),
    path('new_view/', settings_views.new_view, name='new_view'),
    path('save_dashboard_table/', settings_views.save_dashboard_table, name='save_dashboard_table'),

    path('new_dashboard/', settings_views.new_dashboard, name='new_dashboard'),
    path('settings_table/', settings_views.settings_table, name='settings_table'),
    path('settings_table_usertables/', settings_views.settings_table_usertables, name='settings_table_usertables'),
    path('settings_table_usertables_save/', settings_views.settings_table_usertables_save, name='settings_table_usertables_save'),
    path('settings_table_admin/', settings_views.settings_table_admin, name='settings_table_admin'),
    path('settings_table_tablefields/', settings_views.settings_table_tablefields, name='settings_table_tablefields'),
    path('settings_table_tablefields_save/', settings_views.settings_table_tablefields_save, name='settings_table_tablefields_save'),
    path('settings_table_fieldsettings/', settings_views.settings_table_fieldsettings, name='settings_table_fieldsettings'),
    path('settings_table_columnlinked/', settings_views.settings_table_columnlinked, name='settings_table_columnlinked'),
    path('settings_table_columnlinked_save/', settings_views.settings_table_columnlinked_save, name='settings_table_columnlinked_save'),
    path('settings_table_fields/', settings_views.settings_table_fields, name='settings_table_fields'),
    path('settings_table_fields_settings_save/', settings_views.settings_table_fields_settings_save, name='settings_table_fields_settings_save'),
    path('load_table_settings_menu/', settings_views.load_table_settings_menu, name='load_table_settings_menu'),
    path('settings_table_settings/', settings_views.settings_table_settings, name='settings_table_settings'),
    path('settings_table_fields_settings_block/', settings_views.settings_table_fields_settings_block, name='settings_table_fields_settings_block'),
    path('settings_table_fields_settings_fields_save/', settings_views.settings_table_fields_settings_fields_save, name='settings_table_fields_settings_fields_save'),
    path('settings_table_fields_new_field/', settings_views.settings_table_fields_new_field, name='settings_table_fields_new_field'),
    path('settings_table_fields_linked_table/', settings_views.settings_table_fields_linked_table, name='settings_table_fields_linked_table'),
    path('master_columns/', settings_views.master_columns, name='master_columns'),
    path('settings_table_kanbanfields/', settings_views.settings_table_kanbanfields, name='settings_table_kanbanfields'),
    path('settings_table_kanbanfields_save/', settings_views.settings_table_kanbanfields_save, name='settings_table_kanbanfields_save'),
    path('load_category_fields/', settings_views.load_category_fields, name='load_category_fields'),
    path('settings_table_linkedtables/', settings_views.settings_table_linkedtables, name='settings_table_linkedtables'),
    path('settings_table_linkedtables_save/', settings_views.settings_table_linkedtables_save, name='settings_table_linkedtables_save'),
    path('settings_table_newtable/', settings_views.settings_table_newtable, name='settings_table_newtable'),
    path('save_newtable/', settings_views.save_newtable, name='save_newtable'),
    path('settings_user/', settings_views.settings_user, name='settings_user'),
    path('settings_user_newuser/', settings_views.settings_user_newuser, name='settings_user_newuser'),
    path('save_newuser/', settings_views.save_newuser, name='save_newuser'),
    path('settings_user_newgroup/', settings_views.settings_user_newgroup, name='settings_user_newgroup'),
    path('save_newgroup/', settings_views.save_newgroup, name='save_newgroup'),
    path('get_group_settings/', settings_views.get_group_settings, name='get_group_settings'),
    path('save_group_users/', settings_views.save_group_users, name='save_group_users'),
    path('get_user_settings_admin', settings_views.get_user_settings_admin, name='get_user_settings_admin'),
    path('save_theme_setting/', settings_views.save_theme_setting, name='save_theme_setting'),
    path('get_workspaces/', settings_views.get_workspaces, name='get_workspaces'),
    path('save_workspace_settings/', settings_views.save_workspace_settings, name='save_workspace_settings'),
    path('get_script_page/', settings_views.get_script_page, name='get_script_page'),
    path('get_scheduler_page/', settings_views.get_scheduler_page, name='get_scheduler_page'),
    path('test_function', settings_views.test_function, name='test_function'),

]

