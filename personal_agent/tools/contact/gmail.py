
import os
import smtplib
from email.mime.text import MIMEText


def send_contact_email(name: str, sender_email: str, message: str) -> str:
    """
    Sends a contact email to Sergio's personal email address.

    Args:
        name: The name of the person sending the email.
        sender_email: The email address of the person sending the message.
        message: The content of the message.

    Returns:
        A confirmation message indicating the email was sent successfully or an error message.
    """
    # --- Configuración de Email --- #
    # Se obtienen de variables de entorno para no exponerlas en el código.
    # ¡IMPORTANTE! Usa una "App Password" de Google, no tu contraseña principal.
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    recipient_email = os.getenv("GMAIL_USER")  # Enviarse a sí mismo

    if not all([gmail_user, gmail_password, recipient_email]):
        return "Error: La configuración del servidor de correo está incompleta. El administrador debe configurar las variables GMAIL_USER y GMAIL_APP_PASSWORD."

    # --- Creación del Mensaje --- #
    subject = f"Nuevo Mensaje de Contacto de {name}"
    body = f"""
    Has recibido un nuevo mensaje a través de tu agente personal:

    De: {name}
    Email: {sender_email}

    Mensaje:
    --------------------------------------------------
    {message}
    --------------------------------------------------
    """

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = recipient_email

    # --- Envío del Correo --- #
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
        
        print(f"DEBUG: Correo de contacto enviado exitosamente de {sender_email} a {recipient_email}")
        return "¡Gracias por tu mensaje! Le he enviado el correo a Sergio. Se pondrá en contacto contigo pronto."

    except smtplib.SMTPAuthenticationError:
        print("ERROR: Falló la autenticación con Gmail. Revisa GMAIL_USER y GMAIL_APP_PASSWORD.")
        return "Error del servidor: No se pudo autenticar con el servicio de correo. El administrador ha sido notificado."
    except Exception as e:
        print(f"ERROR: Ocurrió un error inesperado al enviar el correo: {e}")
        return f"Error del servidor: No se pudo enviar el correo. Por favor, intenta de nuevo más tarde."
