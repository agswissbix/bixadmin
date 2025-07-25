import datetime
import traceback

def on_task_success(task):
    try:
        print("HOOK ATTIVATO - TASK RICEVUTO")
        print("TASK:", task)

        output = getattr(task, 'result', None)
        func = getattr(task, 'func', 'unknown')
        run_at = datetime.datetime.now()

        from bixmonitoring.views import get_output

        get_output(func=func, output=output, run_at=run_at)
    except Exception:
        print("ERRORE NELL'HOOK:")
        traceback.print_exc()
