import os
from dotenv import load_dotenv  # Instalar con pip install python-dotenv
from cryptography.fernet import Fernet

load_dotenv()  # Carga todo el contenido de .env en variables de entorno


class Config:
    SERVER_NAME = "localhost:7001"
    DEBUG = True

    DATABASE_PATH = "app/database/contact_book.db"
    # Clave Fernet válida por defecto (32 bytes base64 URL-safe)
    _default_key = "u3Uc-qAi9K0HlVwKkewJXyPS1_3pkYAsxycVtJ_u5Eg="
    
    # Validar que DB_TOKEN sea una clave Fernet válida
    _env_token = os.environ.get("DB_TOKEN")
    if _env_token:
        try:
            # Verificar que la clave del .env sea válida
            Fernet(_env_token.encode() if isinstance(_env_token, str) else _env_token)
            DB_TOKEN = _env_token
        except (ValueError, TypeError):
            print(f"⚠️  DB_TOKEN en .env no es válido, usando clave por defecto")
            DB_TOKEN = _default_key
    else:
        DB_TOKEN = _default_key
    
    ENCRYPT_DB = True

    TEMPLATE_FOLDER = "views/templates/"
    STATIC_FOLDER = "views/static/"

    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/rest_db" 
    
    # correo para pruebas
    EMAIL_MESSAGE_USER = "neeva.message@gmail.com"
    EMAIL_MESSAGE_PASSWORD = "aenh yglo sojv bfqf"

    CLOUDINARY = False # poner en True solo si completas los datos de abajo
    CLOUDINARY_CLOUD_NAME = ""
    CLOUDINARY_API_KEY = ""
    CLOUDINARY_API_SECRET = ""