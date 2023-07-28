from pdf2image import convert_from_path
import os
import uuid
import shutil

class DirectoryError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class FileTypeError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class DataFormat:

    def __init__ (self, image_path: str, labels: str):
        self.image_path = image_path
        self.labels = labels
        self.labels
    
    def rename_files_uuid(self):

        if not os.path.exists(self.image_path):
            raise DirectoryError("Directory {} does not exist!".format(self.image_path))

        for label in self.labels:                                                         
            files = os.listdir(os.path.join(self.image_path, label))
            for file in files:
                if not (".jpg" in file) or not (".xml" in file):
                    raise FileTypeError("Invalid file type. Remove or convert to jpg.")
                if ".jpg" in file:
                    imgnameNew = os.path.join(self.image_path,label,label+'_'+'{}.jpg'.format(str(uuid.uuid1())))
                    imgnameOld = os.path.join(self.image_path,label,file)
                    os.rename(imgnameOld, imgnameNew)
    
    def convert_files_jpeg(self):

        if not os.path.exists(self.image_path):
            raise DirectoryError("Images directory {} does not exist!".format(self.image_path))

        for dir in os.listdir(self.image_path):
            files = os.listdir(dir)
            for file in files:
                if '.pdf' in file:
                    filePath = os.path.join(dir, file)
                    images = convert_from_path(filePath)
                    for i, image in enumerate(images):
                        jpgName = os.path.join(dir, f'page_{i + 1}.jpg') 
                        image.save(jpgName, 'JPEG')
                    os.remove(filePath)

class DataPartition:

    def __init__ (self, testing_path: str, training_path: str, no_training_data: int):
        self.testing_path = testing_path
        self.training_path = training_path
        self.no_training_data = no_training_data

    
    def __move_to(img_path, location_path):
        xml_path = img_path.replace(".jpg", ".xml")

        if not os.path.exists(img_path):
            raise DirectoryError("Image File {} does not exist!".format(img_path))

        if not os.path.exists(xml_path):
            raise DirectoryError("Label file {} does not exist! Format data first.".format(xml_path))
        
        if not os.path.exists(location_path):
            raise DirectoryError("Destination folder {} does not exist!".format(location_path))


        shutil.move(img_path, location_path)
        shutil.move(xml_path, location_path)
    
    def __delete_contents(p):
        for file in os.listdir(p):
            os.remove(os.path.join(p, file))
    

    def partition_training_from(self, source_path: str):

        if not os.path.exists(source_path):
            raise DirectoryError("Directory {} does not exist!".format(source_path))

        if not os.path.exists(self.testing_path):
            raise DirectoryError("Testing folder {} does not exist!".format(self.testing_path))
        
        if not os.path.exists(self.training_path):
            raise DirectoryError("Training folder {} does not exist!".format(self.training_path))

        # Clears old training and testing folders
        self.__delete_contents(self.testing_path)
        self.__delete_contents(self.training_path)

        threshold = 2 * self.no_training_data
        for label in os.listdir(source_path):
            files = os.listdir(os.path.join(source_path, label))
            numFiles = len(files)
            for file in files:
                file_path = os.path.join(source_path, label, file)
                if file.endswith('.jpg'):
                    if numFiles <= threshold:
                        self.__move_to(file_path, self.testing_path)
                    else:
                        self.__move_to(file_path, self.training_path)
                    numFiles = len(os.listdir(os.path.join(source_path, label)))
