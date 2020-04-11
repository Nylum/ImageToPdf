from PyPDF2 import PdfFileMerger
from error_handler.error_handler import log_handler


def merge_pdf(pdf_to_be_merged: list, compression: bool) -> None:
    """
    Method that merges each temporary pdf file created from the requested pictures.
    :param pdf_to_be_merged: list that contains the names of each temporary pdf.
    :param compression: flag for the compression mode.
    :return: None
    """
    try:
        merger = PdfFileMerger()
        for pdf in pdf_to_be_merged:
            merger.append(pdf)
        merger.write("compressed_mypdf.pdf" if compression else "mypdf.pdf")
        merger.close()
    except (RuntimeError, OSError, PermissionError) as e:
        with open("pdf_converter_log.txt", "a") as f:
            print(log_handler(e, action="merging mode"), file=f)
    except Exception as e1:  # For any unknown exception so far
        with open("pdf_converter_log.txt", "a") as f:
            print(log_handler(e1, action="merging mode"), file=f)
