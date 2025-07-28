from django.http import HttpResponse
import sys
import importlib

# Crea un alias del modulo "commonapp" verso "bixengine.commonapp"
if 'commonapp' not in sys.modules:
    sys.modules['commonapp'] = importlib.import_module('bixengine.commonapp')

# Ora l'import di UserRecord funziona
from bixengine.commonapp.bixmodels.user_record import UserRecord


def get_output(func, output, run_at):
    print(f"[{run_at}] Funzione: {func} Output: {output}")
    # Qui puoi salvare su DB o file, per ora solo print


def save_monitoring(request):
    record = UserRecord('monitoring')
    record.values['funzione'] = 'test classe'
    record.save()
    return HttpResponse('ok')
