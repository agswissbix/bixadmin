from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from django_q.models import Schedule
from django_q.tasks import async_task
from bixscheduler.utils import get_available_tasks
import importlib


HOOK_PATH = 'bixscheduler.hooks.on_task_success'
FUNC_PATH = 'bixscheduler.tasks.'
# Create your views here.
# require admin role
@login_required(login_url='/login/')
def index(request):
    return render(request, 'lista_schedule.html')

def toggle_scheduler(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    if schedule.next_run is None:
        now = timezone.now()
        next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
        schedule.next_run = next_minute
    else:
        schedule.next_run = None
    schedule.save()
    return redirect(lista_schedule)


def run_scheduler_now(request, schedule_id):
    if request.method == 'POST':
        schedule = get_object_or_404(Schedule, id=schedule_id)
        try:
            async_task(
                schedule.func,
                hook='bixscheduler.hooks.on_task_success',  # forziamo lo stesso hook
            )
        except Exception as e:
            print(f"Errore lanciando {schedule.func} con async_task: {e}")
    return redirect('lista_schedule')


def delete_scheduler(request, schedule_id):
    if request.method == 'POST':
        schedule = get_object_or_404(Schedule, id=schedule_id)
        schedule.delete()
    return redirect('lista_schedule')


def lista_schedule(request):
    if request.method == 'POST':
        schedule_id = request.POST.get('id')
        schedule = get_object_or_404(Schedule, id=schedule_id)

        schedule.name = request.POST.get('name')
        schedule.func = request.POST.get('func')
        schedule.schedule_type = request.POST.get('schedule_type')

        # Imposta l'hook dal valore della variabile
        schedule.hook = HOOK_PATH

        # Salva minutes SOLO se schedule_type è 'I', altrimenti None
        if schedule.schedule_type == 'I':
            minutes = request.POST.get('minutes')
            schedule.minutes = int(minutes) if minutes else None
        else:
            schedule.minutes = None

        # Salva repeats solo se schedule_type NON è 'O', altrimenti None
        if schedule.schedule_type != 'O':
            infinite_checked = request.POST.get('infinite') == 'on'
            if infinite_checked:
                schedule.repeats = -1
            else:
                repeats = request.POST.get('repeats')
                try:
                    schedule.repeats = int(repeats)
                except (TypeError, ValueError):
                    schedule.repeats = 1
        else:
            schedule.repeats = 1

        next_run_str = request.POST.get('next_run')
        if next_run_str:
            try:
                user_time = timezone.make_aware(datetime.strptime(next_run_str, "%Y-%m-%dT%H:%M"))
                schedule.next_run = user_time - timedelta(hours=2)
            except Exception as e:
                print("Errore nel parsing di next_run:", e)

        schedule.save()
        return redirect('lista_schedule')

    schedules = Schedule.objects.all().order_by('id')
    now = timezone.now()

    for s in schedules:
        if s.next_run:
            if s.next_run <= now:
                if s.repeats != 0:  # solo se repeats non è 0
                    # aggiorna al prossimo minuto pieno
                    next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
                    s.next_run = next_minute
                    s.save(update_fields=['next_run'])
                    s.display_next_run = next_minute + timedelta(hours=2)
                else:
                    # repeats = 0 => disattiva
                    s.next_run = None
                    s.save(update_fields=['next_run'])
                    s.display_next_run = None
            else:
                s.display_next_run = s.next_run + timedelta(hours=2)
        else:
            s.display_next_run = None

    available_tasks = get_available_tasks()
    return render(request, 'lista_schedule.html', {
        'schedules': schedules,
        'available_tasks': available_tasks
    })




def aggiungi_scheduler(request):
    if request.method == 'POST':
        now = timezone.now()
        next_run_default = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)

        Schedule.objects.create(
            name='Nuovo Scheduler',
            func=f"{FUNC_PATH}aggiorna_cache",
            hook=HOOK_PATH,               # <-- imposta qui l'hook
            schedule_type='O',
            minutes=None,
            next_run=next_run_default,
            repeats=1,
        )
    return redirect('lista_schedule')