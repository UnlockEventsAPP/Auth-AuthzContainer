import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException


def send_registration_email(to_email: str, name: str, URL: str):
    """
    Envía un correo electrónico de registro con un enlace al login.

    :param to_email: Dirección de correo del destinatario.
    :param name: Nombre del usuario registrado.
    """
    gmail_user = os.getenv('GMAIL_USER')
    gmail_password = os.getenv('GMAIL_PASSWORD')

    subject = "Bienvenido a nuestra plataforma"
    content = f"""
    <html>
        <body>
            <h1>Hola, {name}!</h1>
            <p>Gracias por registrarte en nuestra plataforma.</p>
            <p>Puedes iniciar sesión haciendo clic en el siguiente enlace:</p>
            <a href="{URL}">Ir a la pantalla de Login</a>
        </body>
    </html>
    """

    try:
        # Crear el mensaje de correo
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = to_email
        msg['Subject'] = subject

        # Adjuntar el contenido del correo en HTML
        msg.attach(MIMEText(content, 'html'))

        # Conectar al servidor SMTP de Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)

        # Enviar el correo
        server.sendmail(gmail_user, to_email, msg.as_string())
        server.quit()

        print(f"Correo enviado a {to_email}")
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")
        raise HTTPException(status_code=500, detail="No se pudo enviar el correo.")