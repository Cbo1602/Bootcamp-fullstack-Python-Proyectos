# api.py
import json
import urllib.request
from exepciones import EmailInvalidoError


class ServicioExternoAPI:
    """Clase para la integración con servicios/APIs externas."""

    @staticmethod
    def validar_email_api(email):
        """Simula o consulta un servicio público para verificar que el email es válido."""
        if "@" not in email or "." not in email:
            raise EmailInvalidoError(email)

        try:
            url = "https://jsonplaceholder.typicode.com/users"
            req = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status == 200:
                    print(
                        f"[API Externo] Conexión exitosa. Email '{email}' validado."
                    )
                    return True
        except Exception as e:
            print(f"[API Warning] No se pudo conectar al servicio externo: {e}")
            return True

    @staticmethod
    def enviar_email_bienvenida(nombre, email):
        """Simula el envío de una notificación HTTP POST de bienvenida al cliente."""
        url = "https://jsonplaceholder.typicode.com/posts"
        payload = json.dumps(
            {
                "title": f"Bienvenido/a {nombre}",
                "body": f"Hola {nombre}, tu registro ha sido exitoso.",
                "userId": email,
            }
        ).encode("utf-8")

        try:
            req = urllib.request.Request(
                url,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status in [200, 201]:
                    print(
                        f"[API Notificación] Email de bienvenida enviado a {email}."
                    )
                    return True
        except Exception as e:
            print(
                f"[API Warning] Error al enviar notificación automatizada: {e}"
            )
            return False