import PyPDF2

def extract_text_from_pdf(pdf_file: str) -> [str]:
	with open(pdf_file, 'rb') as pdf:
		reader = PyPDF2.pdfFileReader(pdf, strict=False)
		pdf_text = []

		for page in reader.pages:
			content = page.extract_text()
			pdf_text.append(content)

		return pdf_text

if __name__ == '__main__':
	extracted_text = extract_text_from_pdf('Simple-1Pager.pdf')
	for text in extracted_text:
		print(text)
