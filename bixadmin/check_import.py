import sys

print("=== Controllo ambiente Python ===")
print("Percorsi in sys.path:")
for p in sys.path:
    print(" -", p)

print("\n=== Controllo Django ===")
try:
    import django
    print("Django importato con successo, versione:", django.get_version())
except ImportError as e:
    print("ERRORE: Django non è installato o non è accessibile:", e)

print("\n=== Controllo bixengine e UserRecord ===")
try:
    import bixengine
    print("Pacchetto bixengine trovato:", bixengine.__file__)
    from bixengine.commonapp.bixmodels.user_record import UserRecord
    print("Classe UserRecord importata con successo:", UserRecord)
except ModuleNotFoundError as e:
    print("ERRORE: Modulo non trovato:", e)
except ImportError as e:
    print("ERRORE: Impossibile importare UserRecord:", e)
