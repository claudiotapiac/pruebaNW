
from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from bson import json_util
from datetime import datetime, timezone, timedelta
import pandas as pd
import pytz
import os


app = Flask(__name__)
CORS(app)

connection_string = """mongodb://deliryum-mongodb:Z50r80Z1WKtYhEd2hvt5vcGwDFCgF50GiYaPOOyIEpO8y2cXeODMqRTiz47hek5PG0ja4KjC4hwVACDbFJv2GQ==@deliryum-mongodb.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@deliryum-mongodb@"""

client = MongoClient(connection_string)
conn = client.get_database("Deliryum")

timeZ_AS = pytz.timezone('America/Santiago')

@app.route('/real-time/', methods=["GET"])
def real_time():
    
    now = datetime.now(timeZ_AS) 
    now_delta = now - timedelta(minutes=60)
    
    fecha_actual =  datetime(now.year, now.month, now.day, now.hour, now.minute, now.second, tzinfo=pytz.timezone('America/Santiago'))
    fecha_actual_delta =  datetime(now_delta.year, now_delta.month, now_delta.day, now_delta.hour, now_delta.minute, now_delta.second, tzinfo=pytz.timezone('America/Santiago'))

    collection_conn = conn["TPS"]
    buffer =  list(collection_conn.find({"fecha":{"$gte": str(fecha_actual_delta),"$lt": str(fecha_actual)}, "funcionalidad": { "$eq": "epp" }},{"info":1}))
    if buffer!=[]:
        buffer = pd.DataFrame(buffer)
        buffer = buffer.drop('_id', axis=1)
        buffer = buffer.reset_index()
        buffer = buffer.to_dict('records')
        
    return jsonify(buffer)
    

@app.route('/epp/<int:days>', methods=["GET"])
def all_day(days):
    
    now = datetime.now(timeZ_AS)
    now_delta = now - timedelta(days=days)
    
    fecha_actual =  datetime(now.year, now.month, now.day, now.hour, now.minute, now.second, tzinfo=pytz.timezone('America/Santiago'))
    fecha_actual_delta =  datetime(now_delta.year, now_delta.month, now_delta.day, now_delta.hour, now_delta.minute, now_delta.second, tzinfo=pytz.timezone('America/Santiago'))

    collection_conn = conn["TPS"]
    buffer =  list(collection_conn.find({"fecha":{"$gte": str(fecha_actual_delta),"$lt": str(fecha_actual)}, "funcionalidad": { "$eq": "epp" }}, {"info":1}))
    out_data = list()
    
    if buffer!=[]:
        buffer = {key: [i[key] for i in buffer] for key in buffer[0]}
        buffer = pd.DataFrame(buffer['info'])
        persona_ids = buffer['id_persona'].unique()
        camara_ids = buffer['camara_id'].unique()

        for camara_id in camara_ids:
            for persona_id in persona_ids:
                person_buffer_df = buffer.query(f'{persona_id}==id_persona and {camara_id}==camara_id')
                if person_buffer_df.empty == False: 
                    primer_registro = person_buffer_df.sort_values(by='fecha',ascending=False).tail(n=1).to_dict('records')
                    ultimo_registro = person_buffer_df.sort_values(by='fecha',ascending=True).tail(n=1).to_dict('records')
                    count_sitrans = person_buffer_df['sitrans'].value_counts().to_dict()
                    count_casco = person_buffer_df['casco'].value_counts().to_dict()

                    if ('si' in count_sitrans.keys()) and ('no' not in count_sitrans.keys()):
                        sitrans_credibilidad = 100
                        sitrans = 'si'
                        texto_estado = "SINTRANS (AUTORIZADO)"
                    
                    elif ('no' in count_sitrans.keys()) and ('si' not in count_sitrans.keys()):
                        sitrans_credibilidad = 100
                        sitrans = 'no'
                        texto_estado = "PERSONA NO AUTORIZADA"

                    elif ('no' in count_sitrans) and ('si' in count_sitrans):
                        if count_sitrans['si']>=count_sitrans['no']:
                            sitrans_credibilidad = 100*count_sitrans['si']/(count_sitrans['no']+count_sitrans['si'])
                            sitrans = 'si'
                            texto_estado = "SINTRANS (AUTORIZADO)"
                        else:
                            sitrans_credibilidad = 100*count_sitrans['no']/(count_sitrans['no']+count_sitrans['si'])
                            sitrans = 'no'
                            texto_estado = "PERSONA NO AUTORIZADA"

                    if ('si' in count_casco.keys()) and ('no' not in count_casco.keys()):
                        casco_credibilidad = 100
                        casco = 'si'

                    elif ('no' in count_casco.keys()) and ('si' not in count_casco.keys()):
                        casco_credibilidad = 100
                        casco = 'no'

                    elif ('no' in count_casco) and ('si' in count_casco):
                        if count_casco['si']>=count_casco['no']:
                            casco_credibilidad = 100*count_casco['si']/(count_casco['no']+count_casco['si'])
                            casco = 'si'
                        else:
                            casco_credibilidad = 100*count_casco['no']/(count_casco['no']+count_casco['si'])
                            casco = 'no'

                    primera_fecha = datetime.strptime(primer_registro[0]['fecha'], '%Y-%m-%d %H:%M:%S%z')
                    ultima_fecha = datetime.strptime(ultimo_registro[0]['fecha'], '%Y-%m-%d %H:%M:%S%z')

                    delta = ultima_fecha-primera_fecha

                    segundos_zona = delta.total_seconds()
                    row = {"casco": casco,
                           "casco_credibilidad": str(casco_credibilidad),
                           "sitrans": sitrans,
                           "sitrans_credibilidad": str(sitrans_credibilidad), 
                           "conteo": str(ultimo_registro[0]['conteo']), 
                           "id_persona": str(persona_id),
                           "fecha entrada": primer_registro[0]['fecha'], 
                           "fecha salida": ultimo_registro[0]['fecha'],
                           "segundos_dentro_zona": segundos_zona,
                           "camara_id": str(camara_id), 
                           "alerta": texto_estado
                          }   

                    out_data.append(row)
                    
    return jsonify(out_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
