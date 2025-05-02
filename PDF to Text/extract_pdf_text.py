import PyPDF2

def extract_text_from_pdf(pdf_file: str) -> [str]:
    """
    Extracts text from a PDF file.

    Args:
        pdf_file (str): The path to the PDF file.

    Returns:
        list of str: A list containing the text content of each page in the PDF.
    """
    try:
        with open(pdf_file, 'rb') as pdf:
            reader = PyPDF2.PdfReader(pdf)  # Updated to use PdfReader
            pdf_text = []

            for page in reader.pages:
                content = page.extract_text()
                pdf_text.append(content)

            return pdf_text
    except FileNotFoundError:
        print(f"Error: File '{pdf_file}' not found.")
        return []
    except Exception as e:
        print(f"Error while reading the PDF: {e}")
        return []

def main():
    """
    The main function to extract and display text from a sample PDF file.
    """
    extracted_text = extract_text_from_pdf('dummy.pdf')  # Replace with your PDF file path
    for text in extracted_text:
        if text.strip():  # Skip blank pages
            print(text)

if __name__ == '__main__':
    main()