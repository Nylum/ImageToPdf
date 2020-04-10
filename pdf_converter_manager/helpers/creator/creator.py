from fpdf import FPDF
from PIL import Image
from os import path
from error_handler.error_handler import log_handler
from utilities import utilities
from sys import exit


def create_pdf_from_image(root_path: str, list_images: list) -> list:
    """
    Since that PyFPDF is not smart enough to allow us to change the format of the PDF after it's instantiation
    we need with this method to generate for each picture one pdf file, in order that in the final one each PDF
    pages will entirely fit the pictures.
    :param root_path: absolute path of the temporary folder.
    :param list_images: list that contain the path of the pictures.
    :return: list that contains the name of each temporary PDF files.
    """
    list_pdf_from_image = list()
    try:
        for i, image in enumerate(list_images):
            with Image.open(image) as img:
                width, height = img.size
            new_width = width * 0.75  # Conversion formula from px to pt for the width and the height
            new_height = height * 0.75
            pdf = FPDF(orientation='L', unit="pt", format=(new_height, new_width))
            pdf.add_page()
            pdf.image(image, x=0, y=0, w=new_width, h=new_height)
            # With the aid of the enumerate we place a counter name for each temporary pdf
            pdf_path = path.join(root_path, "{}.pdf".format(i))
            pdf.output(pdf_path)
            list_pdf_from_image.append(pdf_path)
        return list_pdf_from_image
    except (RuntimeError, OSError, PermissionError) as e:
        with open("pdf_converter_log.txt", "a") as f:
            print(log_handler(e, action="creation mode"), file=f)
        utilities.remove_tmp_folder(root_path)  # We need anyway to delete the temporary folder
        exit(1)
    except Exception as e1:  # For any unknown exception so far
        with open("pdf_converter_log.txt", "a") as f:
            print(log_handler(e1, action="creation mode"), file=f)
        utilities.remove_tmp_folder(root_path)  # We need anyway to delete the temporary folder
        exit(1)
