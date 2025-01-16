from config import Config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendEmail(sender, password, destinatario, asunto, cuerpo = ""):
    try:
        #definir las credenciales
        remitente = sender if sender else Config.EMAIL_MESSAGE_USER
        password = password if password else Config.EMAIL_MESSAGE_PASSWORD

        #crear mensaje
        mensaje = MIMEMultipart()
        mensaje["From"] = remitente
        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto

        mensaje.attach(MIMEText(cuerpo, "html"))
        
        #Iniciar session en servidor SMTP de gmail
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(remitente, password)

        #enviar correo
        texto = mensaje.as_string()
        server.sendmail(remitente, destinatario, texto)
        server.quit()
    
        return True
    
    except Exception as error:
        print("Error Send Email: ", error)

        return False
