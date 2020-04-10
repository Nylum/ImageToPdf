from os import path
from utilities import utilities
from error_handler.error_handler import log_handler
from .helpers.merger import merger
from .helpers.retriever import retriever
from .helpers.creator import creator


class PdfConverterManager:
    """
    This class allowed to transform images .jpg or .png into a PDF where every pages contains the images.
    """
    def __init__(self, compression):
        self.flag_compression = compression
        self.main_root_path = None
        self.root_path = None
        self.list_images = list()
        self.list_pdf = list()

    def create_pdf_from_images(self) -> None:
        """
        Method that builds the final PDF from the pictures, it is handling the compression mode as well.
        :return: None
        """
        try:
            # Let's retrieve the path of the application folder
            self.main_root_path = path.dirname(path.abspath(__package__))
            # Storing in a list the path of the images
            self.list_images = retriever.retrieve_images(self.main_root_path)
            # If no picture was retrieved we just go out from this method
            if not self.list_images:
                print("Please select at least one valid image in order to proceed with the conversion!")
                return
            # Creation of the temporary folder that will contain all the files necessary for the computation
            self.root_path = utilities.generate_tmp_folder()
            # Recomputing list_images with the path of the rotated pictures if any
            retriever.create_and_retrieve_rotated_images(self.root_path, self.list_images)
            if self.flag_compression:
                # Recomputing list_images with the path of the compressed pictures
                retriever.create_and_retrieve_compressed_images(self.root_path, self.list_images)
            else:
                # Recomputing list_images with the path of the de-interlaced pictures if any
                retriever.create_and_retrieve_de_interlaced_images(self.root_path, self.list_images)
            # Creating a pdf file for each picture stored
            self.list_pdf = creator.create_pdf_from_image(self.root_path, self.list_images)
            # Let's create the final pdf that will be returned to the user
            merger.merge_pdf(self.root_path, self.list_pdf, self.flag_compression)
        except Exception as e:  # For any unknown exception so far
            with open("pdf_converter_log.txt", "a") as f:
                print(log_handler(e, action="execution of the main module"), file=f)
            if self.root_path:
                utilities.remove_tmp_folder(self.root_path)
