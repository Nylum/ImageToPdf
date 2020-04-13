from error_handler.error_handler import log_handler
from tempfile import mkdtemp
from os import listdir
import shutil


def check_mandatory_dependencies(list_images: list, main_root_path: str, compression: bool) -> bool:
    """
    This checks returns False or True according to the required conditions
    :param list_images: list that contains the path of the pictures.
    :param main_root_path: absolute path of the application folder.
    :param compression: flag for the compression mode.
    :return: False or True
    """
    if not list_images:  # If no picture was retrieved it means that we cannot proceed any further
        print("Please select at least one valid image in order to proceed with the conversion!")
        return False

    # Temporary implementation to skip PDF creation if there is already a file with the same name
    for file in listdir(main_root_path):
        if (not compression and "mypdf.pdf" == file) or (compression and "compressed_mypdf.pdf" == file):
            print("The file with that name already exist! Skipping Pdf creation")
            return False

    return True


def generate_tmp_folder(root_path=None) -> str:
    """
    This method create a temporary folder where all the temporary files will be stored.
    :param root_path: path where the folder is going to be created if specified.
    :return: string that contain the absolute path of the temporary folder.
    """
    try:
        if not root_path:
            # The folder will be placed in the Temp directory e.g. on Windows C:\users\<user>\AppData\Local\Temp
            folder_path = mkdtemp()
        else:
            folder_path = mkdtemp(dir=root_path)
        return folder_path
    except (OSError, TypeError, PermissionError) as e:
        with open("pdf_converter_log.txt", "a") as f:
            print(log_handler(e, action="creating tmp_folder"), file=f)
        if root_path:
            remove_tmp_folder(root_path)
        exit(1)
    except Exception as e1:  # For any unknown exception so far
        with open("pdf_converter_log.txt", "a") as f:
            print(log_handler(e1, action="creating tmp_folder"), file=f)
        if root_path:
            remove_tmp_folder(root_path)
        exit(1)


def remove_tmp_folder(root_path: str) -> None:
    """
    Method that deletes the temporary folder.
    :param root_path: Folder that contain all the temporary files.
    :return: None
    """
    try:
        shutil.rmtree(root_path)
    except (OSError, FileNotFoundError, TypeError, PermissionError) as e:
        with open("pdf_converter_log.txt", "a") as f:
            print(log_handler(e, action="deleting tmp_folder"), file=f)
            # TODO: Try to find a case of PermissionError and provide a fix to force the deletion of the folder
    except Exception as e1:  # For any unknown exception so far
        with open("pdf_converter_log.txt", "a") as f:
            print(log_handler(e1, action="deleting tmp_folder"), file=f)
            # TODO: Apply the same fix here
