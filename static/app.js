let token = "";

function setStatus(msg) {
    document.getElementById("status").innerText = msg;
}

async function enviar() {

    const nombre = document.getElementById("nombre").value.trim();
    const email = document.getElementById("email").value.trim();

    if (!nombre || !email) {
        setStatus("Completa todos los campos");
        return;
    }

    const formData = new FormData();
    formData.append("nombre", nombre);
    formData.append("email", email);

    const res = await fetch("/enviar", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    if (data.ok) {
        token = data.token;

        setStatus("Código enviado. Añádelo al DNS.");

        document.getElementById("btnDns").style.display = "block";
    } else {
        setStatus(data.error || "Error enviando formulario");
    }
}


async function verificarDNS() {

    if (!token) {
        setStatus("Primero debes enviar el formulario");
        return;
    }

    const formData = new FormData();
    formData.append("token", token);

    const res = await fetch("/verificar-dns", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    if (data.ok) {
        setStatus("DNS verificado correctamente");

        document.getElementById("btnPago").style.display = "block";
    } else {
        setStatus(data.error || "DNS no verificado");
    }
}


async function pagar() {

    if (!token) {
        setStatus("No hay verificación activa");
        return;
    }

    const formData = new FormData();
    formData.append("token", token);

    const res = await fetch("/pago", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    if (data.ok) {
        setStatus("Pago realizado con éxito");
    } else {
        setStatus(data.error || "Error en pago");
    }
}