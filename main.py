from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import requests
import dns.resolver
import smtplib
from email.message import EmailMessage
import secrets
import string
import os
from dotenv import load_dotenv

app = FastAPI()

# Static + templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# ENV
load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

#telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# UTIL
# =========================

def generar_token():
    chars = string.ascii_letters + string.digits + "-_"
    rand = ''.join(secrets.choice(chars) for _ in range(43))
    return f"klbrs-site-verification={rand}"


def enviar_email(asunto: str, contenido: str):
    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = SMTP_USER
    msg["To"] = EMAIL_TO
    msg.set_content(contenido)

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)
    except Exception as e:
        print("SMTP ERROR:", e)
        
        return False

    return True

def enviar_telegram(mensaje: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "HTML"
    }

    requests.post(url, data=payload)
# =========================
# FRONT
# =========================

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


# =========================
# ENVIAR FORM
# =========================

@app.post("/enviar")
def enviar(nombre: str = Form(...), email: str = Form(...)):

    if "@" not in email:
        return JSONResponse({"ok": False, "error": "email inválido"})

    token = generar_token()

    mensaje = f"""
Nombre: {nombre}
Email: {email}

Añada este código a su DNS:

{token}
"""

    enviar_email("Verificación DNS", mensaje)

    return JSONResponse({
        "ok": True,
        "email": email,
        "token": token
    })


# =========================
# 2. VERIFICAR DNS
# =========================
@app.post("/verificar-dns")
def verificar_dns(token: str = Form(...)):

    # dominio = EMAIL_TO.split("@")[1].strip().lower()

    # url = f"https://{dominio}/{token}.txt"

    dominio = "klbrs.es"


    # token fijo de prueba (el que sabes que está en el archivo)
    token_esperado = "asiNGORJGNFa_SDOGMJr94-ASITJNENTOsdinrtW5sO"

    try:
        
        respuestas = dns.resolver.resolve(dominio, "TXT")
        
        print("\nDNS TXT encontrados:")

        for r in respuestas:
            txt = r.to_text().strip('"')
            print(" -", txt)

            # lógica de verificación
            if txt.startswith("klbrs-site-verification="):
                valor = txt.split("=", 1)[1].strip()

                print("valor extraído:", valor)

                # comparación contra mock
                if valor == token_esperado:
                    return {
                        "ok": True,
                        "mode": "dns-mock",
                        "domain": dominio,
                        "token": valor
                    }

        return {
            "ok": False,
            "error": "token no encontrado en DNS",
            "mode": "dns-mock"
        }

    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "mode": "dns-mock-error"
        }


    
# =========================
# 3. PAGO
# =========================

MOCK_PAYMENT = True

@app.post("/pago")
def pago():

    if MOCK_PAYMENT:
        ok = True
    else:
        ok = False  # aquí iría Stripe / PayPal / etc

    if ok:
        enviar_email("Pago realizado", "Pago: 30€ Estado: OK")
        enviar_telegram("Pago realizado: 30€\nEstado: OK")
        return {"ok": True}
    
    enviar_telegram("Pago rechazado: 30€\nEstado: Rechazado")

    return {"ok": False, "error": "pago rechazado"}
