from pdf_converter_manager.pdf_converter_manager import PdfConverterManager


def main():
    pdf_converter = PdfConverterManager(compression=False)
    pdf_converter.create_pdf_from_images()


if __name__ == "__main__":
    main()
