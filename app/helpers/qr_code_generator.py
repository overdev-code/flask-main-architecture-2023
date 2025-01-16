from config import Config
from application.helpers.upload_files import UploadFiles
from application.helpers.gestor_restaurant import ManagerData
import qrcode
import os
import datetime
managerData = ManagerData()
uploadFiles = UploadFiles()
def qr_code_generator(value, name_image, path):
    try:

        qr = qrcode.QRCode(version=2, box_size=7, border=1)
        qr.add_data(value)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white")
        
        current_date_hour = datetime.datetime.now()
        random_letter = managerData.generate_random_letter()
        date_hour_formatted = current_date_hour.strftime('%Y-%m-%d_%H_%M_%S')
        name_all = ""
        name_image = name_image
        if name_image.endswith(".png"):
            name_all = os.path.join(path, name_image)
        else:
            name_all = os.path.join(path, name_image+".png")
            name_image = name_image + ".png"

        img.save(name_all)
        if Config.CLOUDINARY:
            new_filename = uploadFiles.cloudinarySend(name_all, str(date_hour_formatted) + str(random_letter))
            name_all = new_filename
            uploadFiles.deleteFile(path, name_image)
        else:
            name_all = "/"+name_all.split("/", 2)[-1]
        return name_all
    
    except Exception as error:
        return error
    
# qr_code_generator("somos libres", "imagen-qr.png", "/ruta/carpeta")