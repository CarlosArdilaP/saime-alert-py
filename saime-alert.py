import smtplib
from email.mime.text import MIMEText
import requests
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import schedule
import datetime

cred = credentials.Certificate('./saime-alert-firebase-adminsdk-yriht-20630a8f59')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://saime-alert-default-rtdb.firebaseio.com/'})

app_password = "la contraseña de applicacion que puede generar en gmail"

def check_website_status():
    url = "https://siic.saime.gob.ve/"
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

async def check_and_update():
    
    previousState = await db.reference("saime-status/isSaimeAlive").get()
    newStatus = check_website_status()
    db.reference("saime-status/lastVerify").set(datetime.datetime.now().strftime("%d/%M/%Y - %H:%M:%S"))
    if newStatus:
        if previousState != newStatus:
            print("¡La pagina del Saime se encuentra en linea!")
            db.reference("saime-status/isSaimeAlive").set(True)
            db.reference("saime-status/lastUpdate").set(datetime.datetime.now().strftime("%d/%M/%Y - %H:%M:%S"))
    else:
        if previousState != newStatus:
            print("¡La página del Saime dejo de estar en linea!")        
            db.reference("saime-status/isSaimeAlive").set(False)
            db.reference("saime-status/lastUpdate").set(datetime.datetime.now().strftime("%d/%M/%Y - %H:%M:%S"))
        else:
            print("La página no está en línea. Reintentando en 1 minuto.")

if __name__ == '__main__':

    print("===========\t  SAIME-ALERT APP ===========")
    print("===========\t  Creado por Carlos Ardila (ArdilaVene)  ===========")
    print("=======================================================\n")
    
    schedule.every().minute.do(check_and_update())

    while True:
        schedule.run_pending()
        time.sleep(1)
    