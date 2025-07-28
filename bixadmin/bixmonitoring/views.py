from django.http import HttpResponse

def get_output(func, output, run_at):
    print(f"[{run_at}] Funzione: {func} Output: {output}")
    # Qui puoi poi salvare su DB o file, ora solo print

#def print_dashboard(request):

import bixengine #type: ignore
from bixengine.commonapp.bixmodels.user_record import UserRecord #type: ignore
def save_monitoring(request):
    record = UserRecord('monitoring')
    record.values['funzione'] = 'test classe'   
    record.save()
    return HttpResponse('ok')

