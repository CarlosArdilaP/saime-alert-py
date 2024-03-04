import requests
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import schedule
from datetime import datetime, timezone
import functools
import os
from dotenv import load_dotenv
load_dotenv()


cred = credentials.Certificate('./saime-alert-firebase-adminsdk-yriht-20630a8f59.json')
firebase_admin.initialize_app(cred, {'databaseURL': os.getenv('FIREBASEDB')})

def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except:
                import traceback
                print(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob
        return wrapper
    return catch_exceptions_decorator

def check_website_status():
    url = "https://siic.saime.gob.ve/"
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

@catch_exceptions()
def check_and_update():
    
    previousState = db.reference("saime-status/isSaimeAlive").get()
    newStatus = check_website_status()
    db.reference("saime-status/lastVerify").set(datetime.now(timezone.utc).timestamp())
    if newStatus:
        if previousState != newStatus:
            print("¡La pagina del Saime se encuentra en linea!")
            db.reference("saime-status/isSaimeAlive").set(True)
            db.reference("saime-status/lastUpdate").set(datetime.now(timezone.utc).timestamp())
            #datetime.datetime.now(vzlaTz).strftime("%d/%M/%Y - %H:%M:%S")
        else:
            print("La página se mantiene en línea. Volviendo a comprobar en un 1 minuto.")
    else:
        if previousState != newStatus:
            print("¡La página del Saime dejo de estar en linea!")        
            db.reference("saime-status/isSaimeAlive").set(False)
            #datetime.datetime.now(vzlaTz).strftime("%d/%M/%Y - %H:%M:%S")
            db.reference("saime-status/lastUpdate").set(datetime.now(timezone.utc).timestamp())
        else:
            print("La página no está en línea. Reintentando en 1 minuto.")

if __name__ == '__main__':

    print("===========\t  SAIME-ALERT APP ===========")
    print("Creado por Carlos Ardila (ArdilaVene)")
    print("=======================================================\n")
    check_and_update()
    schedule.every().minute.do(check_and_update).tag('saimecheck')
    while True:
        schedule.run_pending()
        time.sleep(1)

    