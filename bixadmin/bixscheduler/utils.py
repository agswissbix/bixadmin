import inspect
import pkgutil
import importlib

from django.http import HttpResponse
import bixscheduler.tasks as tasks_module
from django_q.models import Schedule
from django.db import connection, connections

def get_available_tasks():
    available = []

    # Funzioni interne di bixscheduler.tasks
    import bixscheduler.tasks as tasks_module
    for name, func in inspect.getmembers(tasks_module, inspect.isfunction):
        if not name.startswith('_'):
            path = f'bixscheduler.tasks.{name}'
            label = name.replace('_', ' ').title()
            available.append((path, label))

    # Recupera cliente_id
    cliente_id = get_cliente_id()
    target_module = f"customapp_{cliente_id}"

    # Funzioni della sola bixengine.customapp_<cliente_id>.script
    import bixengine  # type: ignore
    for finder, module_name, ispkg in pkgutil.iter_modules(bixengine.__path__):
        if module_name == target_module:
            try:
                module = importlib.import_module(f"bixengine.{module_name}.script")
            except ImportError:
                continue  # se non ha script.py, passa al prossimo

            for name, func in inspect.getmembers(module, inspect.isfunction):
                if not name.startswith('_'):
                    path = f"bixengine.{module_name}.script.{name}"
                    label = f"{module_name.upper()}: {name.replace('_', ' ').title()}"
                    available.append((path, label))
            break  # non serve cercare altre customapp

    return available


def is_schedule_active(name):
    return Schedule.objects.filter(name=name).exists()

def get_cliente_id():
    with connection.cursor() as cursor:
        cursor.execute("SELECT value from sys_settings WHERE setting = 'cliente_id'")
        id_cliente = cursor.fetchone()
        id_cliente = id_cliente[0]
    return id_cliente
