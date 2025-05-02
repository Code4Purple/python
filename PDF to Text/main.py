import PyPDF2

def extract_text_from_pdf(pdf_file: str) -> [str]:
	with open(pdf_file, 'rb') as pdf:
		reader = PyPDF2.PdReader(pdf)
		pdf_text = []

		for page in reader.pages:
			content = page.extract_text()
			pdf_text.append(content)

		return pdf_text

def main():
	extracted_text = extract_text_from_pdf('dummy.pdf')
	for text in extracted_text:
		# split_message = re.split(r'\s+|[,;?!.-]\s*', text.lower()0)
		print(text)

if __name__ == '__main__':
	main()

