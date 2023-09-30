import DataPartition
import DataFormat
import CustomExceptions

class DataCollection:

    # OK
    def __init__(self, image_path: str, collect_name: str, raw_name: str, train_name: str, test_name: str, labels: str):
        self.staging_area = os.path.join(image_path, raw_name)
        self.labels = labels
        self.data_format = DataFormat(os.path.join(image_path, collect_name))
        self.train_test_partition = DataPartition(os.path.join(image_path, train_name), os.path.join(image_path, test_name))

    # OK
    def format_files(self, label_name:str):
        if not label_name in self.labels:
            raise ObjectExistError(f"Label {label_name} is not an existing label.")
        self.data_format.convert_pdf_to_jpeg()
        self.data_format.rename_files_uuid(label_name)
    
    # OK
    def format_all_labels_files(self):
        self.data_format.convert_pdf_to_jpeg()
        self.data_format.rename_files_uuid_all(self.labels)
        
    def move_to_labels(self):
        for label in self.labels:
            label_path = os.path.join(os.path.dirname(self.collected_partition.source_path), label_name)


            #####???????


            partition = DataPartition(self.staging_area, label_path, None)
    
    # OK
    def move_to_label(self, label_name: str):
        if not label in self.labels:
            raise ObjectExistError(f"Label does not not exist in labels: {self.labels}")
        
        label_path = os.path.join(os.path.dirname(self.collected_partition.source_path), label_name)
        partition = DataPartition(self.staging_area, label_path, None)
        partition.move_to_partition_1()

    # OK
    def split_train_test(train_to_test_ratio: int):
        self.train_test_partition.partition_split_two(train_to_test_ratio)

    # OK
    def clear_staging_area(self):
        partition = DataPartition(self.staging_area)
        partition.clear_source()