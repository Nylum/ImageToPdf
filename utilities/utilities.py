from error_handler.error_handler import log_handler
from tempfile import mkdtemp
import shutil


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
    except Exception as e1:  # For any unknown exception so far
        with open("pdf_converter_log.txt", "a") as f:
            print(log_handler(e1, action="deleting tmp_folder"), file=f)
