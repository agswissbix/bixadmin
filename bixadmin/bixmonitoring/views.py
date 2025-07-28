from django.http import HttpResponse, JsonResponse
import sys
import importlib
from datetime import datetime
from django.db import connection
from django.shortcuts import redirect, render

# Crea un alias del modulo "commonapp" verso "bixengine.commonapp"
if 'commonapp' not in sys.modules:
    sys.modules['commonapp'] = importlib.import_module('bixengine.commonapp')

# Ora l'import di UserRecord funziona
from bixengine.commonapp.bixmodels.user_record import UserRecord #type: ignore



def lista_monitoring(request):
    cliente_id = request.GET.get('cliente_id', 'all')
    tipo = request.GET.get('tipo', 'all')
    parametro = request.GET.get('parametro', 'all')

    print("Dati ricevuti dal frontend:")
    print("cliente_id:", cliente_id)
    print("tipo:", tipo)
    print("parametro:", parametro)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        parametri = get_filtered_values(cliente_id, tipo, parametro)
        data = {
            'parametri': [{'nome': p[0], 'valore': p[1], 'data' : p[2], 'ora' : p[3] } for p in parametri],  # converto lista tuple in lista dict
            'tipo': tipo,
        }
        print(data)
        return JsonResponse(data)

    cliente_ids, tipi, parametri = get_distinct_values()
    context = {
        'cliente_ids': cliente_ids,
        'tipi': tipi,
        'parametri': parametri,
    }
    return render(request, 'lista_monitoring.html', context)

def get_output(func, output, run_at, cliente_id):
    print(f"DEBUG - Tipo output: {type(output)}; Valore output: {output}")

    if not isinstance(output, dict):
        output = {
            'status': 'success',
            'value': {'result': output},
            'type': 'unknown'
        }

    # output è un dict, estraiamo i valori
    status = output.get('status', '')
    output_type = output.get('type', '')
    values = output.get('value', {})

    # Se value è un dict o altro, converti in stringa JSON per salvarlo come testo
    import json
    valore_num = json.dumps(values)

    # run_at è un datetime? Se no converti
    if not isinstance(run_at, datetime):
        run_at = datetime.now()

    # Salvataggio su sys_monitoring
    salva_sys_monitoring(run_at, func, output_type, output, cliente_id)

    # Salvataggio su user_monitoring
    salva_user_monitoring(status, run_at, func, output_type, values, cliente_id)

def salva_user_monitoring(status, run_at, func, output_type, values, cliente_id):
    for parametro, valore in values.items():
        record = UserRecord('monitoring')
        record.values['recordstatus_'] = status
        record.values['data'] = run_at.date().isoformat()
        record.values['ora'] = run_at.strftime("%H:%M:%S")
        record.values['funzione'] = func
        record.values['tipo'] = output_type
        record.values['client_id'] = cliente_id
        record.values['parametro'] = parametro

        # Salvataggio dinamico in base al tipo
        if output_type in ['counters', 'folders']:
            record.values['valore_num'] = valore
            # Assicuriamoci di non salvare nelle altre colonne
            record.values.pop('valore_data', None)
            record.values.pop('valore_stringa', None)
        elif output_type == 'dates':
            record.values['valore_data'] = valore
            record.values.pop('valore_num', None)
            record.values.pop('valore_stringa', None)
        elif output_type == 'services':
            record.values['valore_stringa'] = valore
            record.values.pop('valore_num', None)
            record.values.pop('valore_data', None)
        else:
            # Default: salviamo come stringa
            record.values['valore_stringa'] = str(valore)
            record.values.pop('valore_num', None)
            record.values.pop('valore_data', None)

        record.save()

def salva_sys_monitoring(run_at, func, output_type, output, cliente_id):
    data = run_at.date().isoformat()  
    ora = run_at.strftime("%H:%M:%S") 

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO sys_monitoring (data, ora, client_id, funzione, tipo, output)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, [data, ora, cliente_id, func, output_type, output])

def get_distinct_values():
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT client_id FROM user_monitoring")
        cliente_ids = [row[0].capitalize() if row[0] else '' for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT tipo FROM user_monitoring")
        tipi = [row[0].capitalize() if row[0] else '' for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT parametro FROM user_monitoring")
        parametri = [row[0] for row in cursor.fetchall()]

    return cliente_ids, tipi, parametri


def get_filtered_values(client_id, tipo, parametro):
    print(tipo)
    with connection.cursor() as cursor:
        tipo_lower = tipo.lower()
        if tipo_lower in ['folders', 'counters']:
            value_column = 'valore_num'
        else:
            value_column = 'valore_stringa'

        sql = f"""
        SELECT parametro, {value_column}, data, ora 
        FROM user_monitoring
        WHERE (%s = 'all' OR client_id = %s)
          AND (%s = 'all' OR tipo = %s)
          AND (%s = 'all' OR parametro = %s)
        ORDER BY data DESC
        """
        params = [client_id, client_id, tipo, tipo, parametro, parametro]
        
        cursor.execute(sql, params)
        results = cursor.fetchall()
        

    return results


