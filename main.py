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
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# ENV
load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

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
        raise


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

    try:
        dominio = EMAIL_TO.split("@")[1].strip().lower()

        # url = f"https://{dominio}/{token}.txt"

        url = "https://klbrs.es/asiNGORJGNFa_SDOGMJr94-ASITJNENTOsdinrtW5sO.txt"

        # token fijo de prueba (el que sabes que está en el archivo)
        token_esperado = "asiNGORJGNFa_SDOGMJr94-ASITJNENTOsdinrtW5sO"


        response = requests.get(url, timeout=5)

        print(response.status_code)
        print(response.headers.get("content-type"))
        print(repr(response.text[:200]))


        if response.status_code == 200:
            contenido = response.text.strip()

            # if token in contenido:
            #     return {"ok": True}

            if token_esperado in contenido:
                return {"ok": True}



        return {
            "ok": False,
            "error": "token no encontrado en archivo"
        }

    except requests.RequestException as e:
        return {
            "ok": False,
            "error": str(e)
        }

#------------------------------

# @app.post("/verificar-dns")
# def verificar_dns(email: str = Form(...), token: str = Form(...)):
 
    # try:
    #     dominio = email.split("@")[1].strip().lower()
    #     respuestas = dns.resolver.resolve(dominio, "TXT")

    #     registros = []

    #     for r in respuestas:
    #         txt = r.to_text().strip('"')
    #         txt = txt.replace('"', "").strip()
    #         registros.append(txt)

    #     for registro in registros:
    #         if token in registro:
    #             return {"ok": True}

    #     return {
    #         "ok": False,
    #         "error": "token no encontrado en DNS",
    #         "debug": registros
    #     }

    # except dns.resolver.NXDOMAIN:
    #     return {"ok": False, "error": "dominio no existe"}

    # except dns.resolver.NoAnswer:
    #     return {"ok": False, "error": "no hay registros TXT"}

    # except Exception as e:
    #     return {"ok": False, "error": str(e)}
    
# =========================
# 3. PAGO
# =========================

@app.post("/pago")
def pago(pagoRealizado: bool = Form(...)):
    if not pagoRealizado:
        enviar_email("Pago fallido", "El pago no se ha realizado correctamente.")
        return {"ok": False, "error": "pago no realizado"}
    
    contenido = f"""
                    Pago realizado correctamente

                    Pago:30€
                    Estado: OK
                """

    enviar_email("Pago realizado", contenido)
 
    return {"ok": True}