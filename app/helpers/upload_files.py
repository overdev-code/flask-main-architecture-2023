from config import Config
import os
import datetime
import uuid
import string
import random
from PIL import Image
import mimetypes

class UploadFiles:
    
    def __init__(self):
        # Directorio base para guardar archivos
        self.base_path = os.path.join(os.path.dirname(__file__), '..', 'views', 'static')
        
        # Extensiones permitidas por tipo de archivo
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.svg'}
        self.video_extensions = {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v'}
        self.audio_extensions = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'}
        self.doc_extensions = {'.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'}

    def _generate_unique_filename(self, original_filename, extension=None):
        """Genera un nombre de archivo único"""
        if extension is None:
            extension = os.path.splitext(original_filename)[1].lower()
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        unique_id = str(uuid.uuid4())[:8]
        
        return f"{timestamp}_{random_string}_{unique_id}{extension}"

    def _ensure_directory_exists(self, path):
        """Crea el directorio si no existe"""
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating directory {path}: {e}")
            return False

    def _validate_file_type(self, filename, allowed_extensions):
        """Valida si el archivo tiene una extensión permitida"""
        extension = os.path.splitext(filename)[1].lower()
        return extension in allowed_extensions

    def _convert_to_webp(self, image_path, quality=60):
        """Convierte imagen a WebP con compresión"""
        try:
            with Image.open(image_path) as img:
                # Convertir a RGB si es necesario
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Generar nuevo nombre con extensión .webp
                webp_path = os.path.splitext(image_path)[0] + '.webp'
                
                # Guardar como WebP con compresión
                img.save(webp_path, 'WebP', quality=quality, optimize=True)
                
                # Eliminar archivo original
                os.remove(image_path)
                
                return webp_path
        except Exception as e:
            print(f"Error converting to WebP: {e}")
            return image_path

    def _save_single_file(self, file, path, allowed_extensions, convert_to_webp=False):
        """Guarda un archivo individual"""
        try:
            if not file or not file.filename:
                return None
            
            # Validar tipo de archivo
            if not self._validate_file_type(file.filename, allowed_extensions):
                return None
            
            # Generar nombre único
            filename = self._generate_unique_filename(file.filename)
            file_path = os.path.join(path, filename)
            
            # Guardar archivo
            file.save(file_path)
            
            # Convertir a WebP si es necesario (solo para imágenes)
            if convert_to_webp and allowed_extensions == self.image_extensions:
                file_path = self._convert_to_webp(file_path)
                filename = os.path.basename(file_path)
            
            # Retornar path relativo
            return os.path.join(path, filename).replace('\\', '/')
            
        except Exception as e:
            print(f"Error saving file: {e}")
            return None

    def _process_files(self, files, path, allowed_extensions, convert_to_webp=False):
        """Procesa archivos (individual o múltiple)"""
        # Asegurar que el directorio existe
        if not self._ensure_directory_exists(path):
            return {"saved": False, "paths": [], "error": "Could not create directory"}
        
        saved_paths = []
        
        # Manejar archivos múltiples o individuales
        if isinstance(files, list):
            for file in files:
                file_path = self._save_single_file(file, path, allowed_extensions, convert_to_webp)
                if file_path:
                    saved_paths.append(file_path)
        else:
            file_path = self._save_single_file(files, path, allowed_extensions, convert_to_webp)
            if file_path:
                saved_paths.append(file_path)
        
        return {
            "saved": len(saved_paths) > 0,
            "paths": saved_paths
        }

    def uploadImages(self, files, subfolder="images", convert_to_webp=False):
        """
        Sube archivos de imagen
        
        Args:
            files: Archivo o lista de archivos de imagen
            subfolder: Subcarpeta dentro de views/static/ (default: "images")
            convert_to_webp: Si True, convierte a WebP con 60% de calidad
        
        Returns:
            dict: {"saved": bool, "paths": [list_of_paths]}
        """
        full_path = os.path.join(self.base_path, subfolder)
        return self._process_files(files, full_path, self.image_extensions, convert_to_webp)

    def uploadVideos(self, files, path):
        """
        Sube archivos de video
        
        Args:
            files: Archivo o lista de archivos de video
            path: Ruta donde guardar los archivos
        
        Returns:
            dict: {"saved": bool, "paths": [list_of_paths]}
        """
        return self._process_files(files, path, self.video_extensions)

    def uploadAudios(self, files, path):
        """
        Sube archivos de audio
        
        Args:
            files: Archivo o lista de archivos de audio
            path: Ruta donde guardar los archivos
        
        Returns:
            dict: {"saved": bool, "paths": [list_of_paths]}
        """
        return self._process_files(files, path, self.audio_extensions)

    def uploadDocs(self, files, path):
        """
        Sube archivos de documentos
        
        Args:
            files: Archivo o lista de archivos de documento
            path: Ruta donde guardar los archivos
        
        Returns:
            dict: {"saved": bool, "paths": [list_of_paths]}
        """
        return self._process_files(files, path, self.doc_extensions)

    def uploadAny(self, files, path):
        """
        Sube cualquier tipo de archivo
        
        Args:
            files: Archivo o lista de archivos
            path: Ruta donde guardar los archivos
        
        Returns:
            dict: {"saved": bool, "paths": [list_of_paths]}
        """
        # Combinar todas las extensiones permitidas
        all_extensions = (self.image_extensions | self.video_extensions | 
                         self.audio_extensions | self.doc_extensions)
        return self._process_files(files, path, all_extensions)

    def cloudinarySend(self, path_image, public_id):
        """Sube archivo a Cloudinary (método legacy)"""
        try:
            import cloudinary
            import cloudinary.uploader
            from cloudinary.utils import cloudinary_url
            
            cloudinary.config( 
                cloud_name = Config.CLOUDINARY_CLOUD_NAME, 
                api_key = Config.CLOUDINARY_API_KEY, 
                api_secret = Config.CLOUDINARY_API_SECRET,
                secure=True,
            )
            upload_result = cloudinary.uploader.upload(path_image, public_id=public_id)
            return upload_result["secure_url"]
        except Exception as e:
            print(f"Error uploading to Cloudinary: {e}")
            return None

    def deleteFile(self, path, filename):
        """Elimina un archivo"""
        try:
            file_path = os.path.join(path, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
