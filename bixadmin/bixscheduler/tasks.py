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


