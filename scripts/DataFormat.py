from pdf2image import convert_from_path
import CustomExceptions
import os
import uuid
import shutil
import numpy as np

class DataFormat:

    # OK
    def __init__ (self, source_path: str):
        self.source_path = source_path
    
    # OK
    def rename_files_uuid(self, folder_name):
        if not os.path.exists(self.source_path):
            raise DirectoryError("Directory {} does not exist!".format(self.source_path))

        files = os.listdir(self.source_path)
        for file in files:
            self.__convert_file_uuid(file, folder_name)
    
    # OK
    def rename_files_uuid_all(self, folder_names: list[str]):
        if not os.path.exists(self.source_path):
            raise DirectoryError("Directory {} does not exist!".format(self.source_path))
        
        files = os.listdir(self.source_path)
        partitions = np.array_split(files, len(folder_names))
        for i in range(len(partitions)):
            for file in partitions[i]:
                self.__convert_file_uuid(file, folder_names[i])
    
    # OK
    def __convert_file_uuid(self, file, folder_name):
        if not (file.endswith(".jpg") or file.endswith(".jpeg")):
                raise FileTypeError("Invalid file type. Remove or convert to jpeg.")
        imgnameNew = os.path.join(self.source_path, folder_name, folder_name + '.' + '{}.jpeg'.format(str(uuid.uuid1())))
        imgnameOld = os.path.join(self.source_path, folder_name, file)
        os.rename(imgnameOld, imgnameNew)

    # OK
    def convert_pdf_to_jpeg(self):
        if not os.path.exists(self.source_path):
            raise DirectoryError("Images raw directory {} does not exist!".format(self.source_path))

        if len(os.listdir(self.source_path)) == 0:
            raise DirectoryError("Empty directory {}! Add files to it.".format(self.source_path))
        

        for file in os.listdir(self.source_path):
            if '.pdf' in file:
                filePath = os.path.join(self.source_path, file)
                images = convert_from_path(filePath)
                for i, image in enumerate(images):
                    jpgName = os.path.join(self.source_path, f'page_{i + 1}.jpeg') 
                    image.save(jpgName, 'JPEG')
                os.remove(filePath)
    
    