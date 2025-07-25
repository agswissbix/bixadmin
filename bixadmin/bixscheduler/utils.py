import inspect
import pkgutil
import importlib
import bixscheduler.tasks as tasks_module
from django_q.models import Schedule

def get_available_tasks():
    available = []

    # Funzioni interne di bixscheduler.tasks
    for name, func in inspect.getmembers(tasks_module, inspect.isfunction):
        if not name.startswith('_'):
            path = f'bixscheduler.tasks.{name}'
            label = name.replace('_', ' ').title()
            available.append((path, label))

    # Funzioni di tutti i bixengine.customapp_*.script
    import bixengine
    for finder, module_name, ispkg in pkgutil.iter_modules(bixengine.__path__):
        if module_name.startswith("customapp_"):
            try:
                module = importlib.import_module(f"bixengine.{module_name}.script")
            except ImportError:
                continue  # Se non ha "script.py", salta

            for name, func in inspect.getmembers(module, inspect.isfunction):
                if not name.startswith('_'):
                    path = f"bixengine.{module_name}.script.{name}"
                    label = f"{module_name.upper()}: {name.replace('_', ' ').title()}"
                    available.append((path, label))

    return available


def is_schedule_active(name):
    return Schedule.objects.filter(name=name).exists()
