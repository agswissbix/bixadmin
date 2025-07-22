from datetime import datetime
from django_q.models import Schedule, Task
from django.db import connection

def default_task(*args, **kwargs):
    print("Default task called - stub.")


#DA LASCIARE SENNO DA TANTI ERRORI!
def aggiorna_cache():
    print("Cache aggiornata!")


def stampa_messaggio():
    print(f"[{datetime.now()}] Ciao! Sono uno scheduler eseguito con Django-Q.")

def fix_repeats_and_clear_failed_tasks():
    # Correggi repeats minori di -1
    schedules = Schedule.objects.filter(repeats__lt=-1)
    for s in schedules:
        s.repeats = -1
        s.save()

    # Elimina tutti i task falliti
    failed_tasks = Task.objects.filter(success=False)
    failed_tasks.delete()
