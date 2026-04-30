from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import smtplib
from email.message import EmailMessage
import secrets
import string
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv("data.env")

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

def enviar_email(nombre: str, email: str, mensaje: str):
    msg = EmailMessage()
    msg['Subject'] = 'Nuevo formulario recibido'
    msg['From'] = SMTP_USER
    msg['To'] = EMAIL_TO

    msg.set_content(f"""
Nuevo formulario recibido:

Nombre: {nombre}
Email: {email}
Mensaje: {mensaje}
""")

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
    	smtp.login(SMTP_USER, SMTP_PASS)
    	smtp.send_message(msg)


def filtro_email(email: str) -> bool:
    DOMINIOS_BLOQUEADOS = {
        "gmail",
        "hotmail",
        "outlook",
        "yahoo"
    }

    try:
        dominio_completo = email.split("@")[1].lower()
        proveedor = dominio_completo.split(".")[0]

        return proveedor not in DOMINIOS_BLOQUEADOS

    except IndexError:
        return False
        
def generar_cadena(longitud: int = 43) -> str:
    caracteres = string.ascii_letters + string.digits + "_-"
    random_part = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    return f"klbrs-site-verification={random_part}"

@app.get("/", response_class=HTMLResponse)
def formulario():
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Formulario</title>
</head>

<body style="margin:0;font-family:Arial;background:#0f172a;display:flex;justify-content:center;align-items:center;height:100vh;">

<div style="width:320px;background:#1e293b;padding:28px;border-radius:10px;">
    <h2 style="text-align:center;color:#f1f5f9;">Formulario</h2>

    <form action="/enviar" method="post" style="display:flex;flex-direction:column;gap:12px;">
        <label style="color:#cbd5e1;">Nombre</label>
        <input type="text" name="nombre" required>

        <label style="color:#cbd5e1;">Email</label>
        <input type="email" name="email" required>

        <label style="color:#cbd5e1;">Mensaje</label>
        <textarea name="mensaje" rows="4" required></textarea>

        <button type="submit" style="padding:10px;background:#3b82f6;color:white;border:none;border-radius:6px;">
            Enviar
        </button>
    </form>
</div>

</body>
</html>
"""


@app.post("/enviar", response_class=HTMLResponse)
def enviar(nombre: str = Form(...), email: str = Form(...), mensaje: str = Form(...)):

    if not filtro_email(email):
        return """
        <h2 style="color:red;text-align:center;margin-top:50px;">
            Email no permitido
        </h2>
        """

    codigo = generar_cadena(32)
    cadena = f"/{email}/{codigo}"

    try:
        enviar_email(nombre, email, mensaje + cadena)

        return f"""
        <h2 style="color:green;text-align:center;margin-top:50px;">
            Formulario enviado correctamente
        </h2>
        <p style="text-align:center;">
            Ruta generada:
        </p>
        <p style="text-align:center;"><b>{cadena}</b></p>
        """

    except Exception as e:
        return f"<h2>Error</h2><pre>{str(e)}</pre>"
