from config import Config
import os
import datetime
from application.helpers.gestor_restaurant import ManagerData

# EXAMPLE
# uploadFiles.uploadFile(request.files.get("company_image"), PATH_UPLOAD_IMAGES_USERS)

class UploadFiles:
    managerData = ManagerData()
    def cloudinarySend(self, path_image, public_id):
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

    def uploadFile(self, file, path, filename=False):
        
        if (file):
            if isinstance(file, list):
                saved_files = []
                if len(file) > 0:
                    for fl in file:
                        try:
                            if(fl.name != ""):
                                name_image = fl.filename
                                extension = name_image.split(".")[-1]
                                if name_image and extension:    
                                    current_date_hour = datetime.datetime.now()
                                    date_hour_formatted = current_date_hour.strftime('%Y-%m-%d_%H_%M_%S')
                                    random_letter = self.managerData.generate_random_letter()
                                    filename = str(date_hour_formatted) + str(random_letter)+"."+ str(extension)
                                    name_all = os.path.join(path, filename)
                                    fl.save(name_all)
                                    if Config.CLOUDINARY:
                                        new_filename = self.cloudinarySend(name_all, str(date_hour_formatted) + str(random_letter))
                                        self.deleteFile(path, filename)
                                        name_all = new_filename
                                    else:
                                        name_all = "/"+name_all.split("/", 2)[-1]
                                    saved_files.append(name_all)
                        except Exception as err:
                            print("Error list when trying to save the image")
                            print("[ERROR] ", err)

                    return saved_files
                else:
                    return False
            else:
                try:
                    if(file.name != ""):
                        name_image = file.filename
                        extension = name_image.split(".")[-1]
                        if (filename):
                            pass
                        else:
                            current_date_hour = datetime.datetime.now()
                            date_hour_formatted = current_date_hour.strftime('%Y-%m-%d_%H_%M_%S')
                            random_letter = self.managerData.generate_random_letter()
                            filename = str(date_hour_formatted) + str(random_letter)+"."+ str(extension)
                        name_all = os.path.join(path, filename)
                        file.save(name_all)
                        if Config.CLOUDINARY:
                            try:
                                new_filename = self.cloudinarySend(name_all, str(date_hour_formatted) + str(random_letter))
                            except Exception as err:
                                print("Error when trying to save the image in cloudinary")
                                print("[ERROR] ", err)            
                                return ""
                            self.deleteFile(path, filename)
                            name_all = new_filename
                        else:
                            name_all = "/"+name_all.split("/", 2)[-1]
                        return name_all
                    else:
                        return False
                except Exception as err:
                    print("Error unique when trying to save the image")
                    print("[ERROR] ", err)
                    return False
        else:
            return False
    
    def deleteFile(self, path, filename):
        try:
            if os.path.exists(os.path.join(path, filename)):
                os.remove(os.path.join(path, filename))
                return "ok"
            else:
                return "ok"
        except Exception as err:
            print("Error when trying to delete the image")
            print("[ERROR] ", err)
            return False