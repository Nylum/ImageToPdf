from os import path, walk
from PIL import Image, ExifTags
from error_handler.error_handler import log_handler
from utilities import utilities
from sys import exit


def retrieve_images(main_root_path: str) -> list:
    """
    This method is used to store in a list the absolute path of each valid picture that will represent the PDF.
    :param main_root_path: absolute path of the application.
    :return: list that contains the path of all the valid pictures.
    """
    list_valid_format_images = [".jpg", ".png"]

    return [path.join(root, file) for root, _, files in walk(main_root_path) for file in files
            if path.splitext(file)[1] and path.splitext(file)[1].lower() in list_valid_format_images]


def create_and_retrieve_rotated_images(root_path: str, list_images: list) -> None:
    """
    From each original picture we need to check if we need to change it's orientation and then update the path
    of the rotated image.
    :param root_path: absolute path of the temporary folder.
    :param list_images: list that contains the path of the original pictures.
    :return: None
    """
    # Creation of the temporary folder that will contain all the files necessary for the computation
    rotated_folder_path = utilities.generate_tmp_folder(root_path)
    try:
        for i, image in enumerate(list_images):
            img = Image.open(image)  # We don't use with statement otherwise the Image object won't be closed
            # Let's retrieve the picture tags
            exif = dict((ExifTags.TAGS[k], v) for k, v in img.getexif().items() if k in ExifTags.TAGS)
            if "Orientation" not in exif:
                continue  # No need to rotate the image, we proceed with the next iteration
            if exif["Orientation"] == 3:
                rotated_img = img.rotate(180, expand=True)
            elif exif["Orientation"] == 6:
                rotated_img = img.rotate(270, expand=True)
            elif exif["Orientation"] == 8:
                rotated_img = img.rotate(90, expand=True)
            else:
                continue  # No need to rotate the image, we proceed with the next iteration
            img.close()
            rotated_img_path = path.join(rotated_folder_path, path.split(image)[-1])
            rotated_img.save(rotated_img_path)  # Saving the new rotated image in the path required
            rotated_img.close()
            list_images[i] = rotated_img_path  # Finally we update the path of the picture that has been rotated
    except (RuntimeError, OSError, PermissionError) as e:
        with open("pdf_converter_log.txt", "a") as f:
            print(log_handler(e, action="rotation mode"), file=f)
        utilities.remove_tmp_folder(root_path)  # We need anyway to delete the temporary folder
        exit(1)
    except Exception as e1:  # For any unknown exception so far
        with open("pdf_converter_log.txt", "a") as f:
            print(log_handler(e1, action="rotation mode"), file=f)
        utilities.remove_tmp_folder(root_path)  # We need anyway to delete the temporary folder
        exit(1)


def create_and_retrieve_compressed_images(root_path: str, list_images: list) -> None:
    """
    Since that PyPDF is not supporting the PDF compression, from each original picture and then finally rewrite
    list_images with the path of the compressed pictures.
    :param root_path: absolute path of the temporary folder.
    :param list_images: list that contains the path of the original pictures.
    :return: None
    """
    # Creation of the temporary folder that will contain all the files necessary for the computation
    compressed_folder_path = utilities.generate_tmp_folder(root_path)
    try:
        for i, image in enumerate(list_images):
            img = Image.open(image)  # We don't use with statement otherwise the Image object won't be closed
            width, height = img.size
            # In order to proceed with the compression we need to recalculate width and height of the image
            resized_width = int(width / 2)
            resized_height = int(height / 2)
            # Resizing original pictures and creating for each the new compressed one
            compressed_img = img.resize((resized_width, resized_height), Image.ANTIALIAS)
            img.close()
            compressed_img_path = path.join(compressed_folder_path, path.split(image)[-1])
            compressed_img.save(compressed_img_path, quality=90, optimize=True)
            compressed_img.close()
            list_images[i] = compressed_img_path  # Finally we update the path of the picture that has been compressed
    except (RuntimeError, OSError, PermissionError) as e:
        with open("pdf_converter_log.txt", "a") as f:
            print(log_handler(e, action="compression mode"), file=f)
        utilities.remove_tmp_folder(root_path)  # We need anyway to delete the temporary folder
        exit(1)
    except Exception as e1:  # For any unknown exception so far
        with open("pdf_converter_log.txt", "a") as f:
            print(log_handler(e1, action="compression mode"), file=f)
        utilities.remove_tmp_folder(root_path)  # We need anyway to delete the temporary folder
        exit(1)


def create_and_retrieve_de_interlaced_images(root_path: str, list_images: list) -> None:
    """
    From each original picture we need to check if we need to create a new image in order to get rid of the interlace
    property, update then the path of the de-interlaced image.
    :param root_path: absolute path of the temporary folder.
    :param list_images: list that contains the path of the original pictures.
    :return: None
    """
    # Creation of the temporary folder that will contain all the files necessary for the computation
    de_interlace_folder_path = utilities.generate_tmp_folder(root_path)
    try:
        for i, image in enumerate(list_images):
            img = Image.open(image)  # We don't use with statement otherwise the Image object won't be closed
            if "interlace" not in img.info:
                continue  # No need to de-interlace the image, we proceed with the next iteration
            de_interlaced_img_path = path.join(de_interlace_folder_path, path.split(image)[-1])
            img.save(de_interlaced_img_path)
            img.close()
            # Finally we update the path of the picture that has been de-interlaced
            list_images[i] = de_interlaced_img_path
    except (RuntimeError, OSError, PermissionError) as e:
        with open("pdf_converter_log.txt", "a") as f:
            print(log_handler(e, action="de-interlacing mode"), file=f)
        utilities.remove_tmp_folder(root_path)  # We need anyway to delete the temporary folder
        exit(1)
    except Exception as e1:  # For any unknown exception so far
        with open("pdf_converter_log.txt", "a") as f:
            print(log_handler(e1, action="de-interlacing mode"), file=f)
        utilities.remove_tmp_folder(root_path)  # We need anyway to delete the temporary folder
        exit(1)
