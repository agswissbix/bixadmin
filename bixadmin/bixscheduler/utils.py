import inspect
import bixscheduler.tasks as tasks_module
from django_q.models import Schedule

def get_available_tasks():
    functions = inspect.getmembers(tasks_module, inspect.isfunction)
    available = []
    for name, func in functions:
        if not name.startswith('_'):
            path = f'bixscheduler.tasks.{name}'
            label = name.replace('_', ' ').title()
            available.append((path, label))
    return available

def is_schedule_active(name):
    return Schedule.objects.filter(name=name).exists()
