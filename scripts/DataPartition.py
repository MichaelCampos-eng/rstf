import CustomExceptions

class DataPartition:

    # OK
    def __init__ (self, source_path: str, *args):
        if not os.path.exists(source_path):
            raise DirectoryError("Directory {} does not exist!".format(source_path))
        for part_path in args:
            if not os.path.exists(part_path):
                raise DirectoryError("Directory {} does not exist!".format(part_path))
        
        self.source_path = source_path
        self.partitions = args

    # OK
    def clear_partition_by_index(self, index: int):
        self.__clear_directory(self.partitions[i])
    
    # OK
    def clear_partitions(self):
        for i in range(len(self.partitions)):
            self.clear_partition_by_index(i)
    
    # OK
    def clear_source(self):
        self.__clear_directory(self.source_path)
    
    # OK
    def __clear_directory(self, dir_path):
        if not os.path.exists(dir_path):
            raise DirectoryError("Directory {} does not exist!".format(self.image_collected_path))

        for file in os.listdir(dir_path):
            os.remove(os.path.join(dir_path, file))

    # OK    
    def move_to_partition(self, part_path: str):
        if not os.path.exists(self.source_path):
            raise DirectoryError("Directory {} does not exist!".format(self.source_path))
        if not os.path.exists(self.part_path_1):
            raise DirectoryError("Directory {} does not exist!".format(self.part_path_1))

        self.__move_to_partition(self.part_path_1)
    
    def move_to_partition(self, index: int):
        if not os.path.exists(self.source_path):
            raise DirectoryError("Directory {} does not exist!".format(self.source_path))
        if not os.path.exists(self.part_path_1):
            raise DirectoryError("Directory {} does not exist!".format(self.part_path_1))

        self.__move_to_partition(self.partitions[index])

    # OK
    def __move_to_partition(self, dest_folder_path: str):
        for file in os.listdir(self.source_path):
            destination = os.path.join(dest_folder_path, file)
            source_copy = os.path.join(self.source_path, f'copy_{file}') # FIX THIS
            shutil.copy(os.path.join(self.source_path, file), source_copy)
            shutil.move(source_copy, destination)

    # OK
    def partition_split_two(self, ratio_one_two: int):

        if ratio_one_two < 0 or ratio_one_two > 1:
            raise InputSizeError(f"Ratio {ratio_one_two} outside range [0, 1]")
        if len(self.partitions) != 2:
            raise InputSizeError(f"No. of partitions {len(self.partitions)} is not 2.")

        if not os.path.exists(self.source_path):
            raise DirectoryError("Directory {} does not exist!".format(self.source_path))
        if not os.path.exists(self.partitions[0]):
            raise DirectoryError("Directory {} does not exist!".format(self.partitions[0]))
        if not os.path.exists(self.partitions[1]):
            raise DirectoryError("Directory {} does not exist!".format(self.partitions[1]))

        # Clears old folders
        self.__delete_contents(self.partitions[0])
        self.__delete_contents(self.partitions[1])

        for label in os.listdir(self.source_path):

            label_path = os.path.join(self.source_path, label)
            if not os.path.exists(label_path):
                raise DirectoryError("Directory {} does not exist!".format(label_path))

            files = os.listdir(label_path)
            count = len(files) * ratio
            for file in files:
                file_path = os.path.join(source_path, label, file)
                if file.endswith('.jpg'):
                    if count == 0:
                        self.__move_to(file_path, self.partitions[1])
                    else:
                        self.__move_to(file_path, self.partitions[0])
                        count -= 1
    
    # OK
    def __move_to(self, img_path, location_path):
        xml_path = img_path.replace(".jpeg", ".xml") if img_path.endswith(".jpeg") else img_path.replace(".jpg", ".xml")

        if not os.path.exists(img_path):
            raise DirectoryError("Image File {} does not exist!".format(img_path))

        if not os.path.exists(xml_path):
            raise DirectoryError("Label file {} does not exist! Format data first.".format(xml_path))
        
        if not os.path.exists(location_path):
            raise DirectoryError("Destination folder {} does not exist!".format(location_path))

        shutil.move(img_path, location_path)
        shutil.move(xml_path, location_path)

    # OK    
    def __delete_contents(self, p):
        for file in os.listdir(p):
            os.remove(os.path.join(p, file))