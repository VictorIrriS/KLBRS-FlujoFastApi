import dns.resolver
import requests
import sys


# =========================
# VERIFICACIÓN DNS
# =========================
def verificar_dns(dominio: str, token: str) -> bool:
    try:
        respuestas = dns.resolver.resolve(dominio, "TXT")

        print("\n📡 TXT records DNS:")
        for r in respuestas:
            txt = r.to_text().strip('"')
            print(" -", txt)

            if txt.startswith("klbrs-site-verification="):
                valor = txt.split("=", 1)[1].strip()

                if valor == token:
                    return True

        return False

    except Exception as e:
        print(f"❌ Error DNS: {e}")
        return False

# =========================
# VERIFICACIÓN URL
# =========================
def verificar_url(dominio: str, token: str) -> bool:
    url = f"https://{dominio}/.well-known/klbrs-site-verification.txt"

    print(f"\n🌐 Consultando URL: {url}")

    try:
        r = requests.get(url, timeout=5)

        print(f"HTTP Status: {r.status_code}")

        if r.status_code != 200:
            return False

        contenido = r.text.strip()

        print("\n📄 Contenido URL:")
        print(contenido)

        return token in contenido

    except requests.RequestException as e:
        print(f"❌ Error URL: {e}")
        return False


# =========================
# MAIN
# =========================
if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Uso: python verificar.py <dominio> <token> <dns|url|ambos>")
        sys.exit(1)

    dominio = sys.argv[1]
    token = sys.argv[2]
    modo = sys.argv[3].lower()

    print("\n🔎 INICIANDO VERIFICACIÓN")
    print(f"🌍 Dominio: {dominio}")
    print(f"🔑 Token: {token}")
    print(f"⚙️ Modo: {modo}")

    dns_ok = False
    url_ok = False

    # =========================
    # EJECUCIÓN SEGÚN MODO
    # =========================
    if modo == "dns":
        dns_ok = verificar_dns(dominio, token)

    elif modo == "url":
        url_ok = verificar_url(dominio, token)

    elif modo == "ambos":
        dns_ok = verificar_dns(dominio, token)
        url_ok = verificar_url(dominio, token)

    else:
        print("❌ Modo inválido. Usa: dns | url | ambos")
        sys.exit(1)

    # =========================
    # RESULTADO FINAL
    # =========================
    print("\n=========================")

    if dns_ok:
        print("✅ VERIFICADO POR DNS")

    if url_ok:
        print("✅ VERIFICADO POR URL")

    if dns_ok or url_ok:
        print("\n🎉 DOMINIO VERIFICADO")
    else:
        print("\n❌ DOMINIO NO VERIFICADO")
