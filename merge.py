import PyPDF2
import os

def mergePDF(filename, dirname):
    if not filename:
        return

    if not dirname:
        return

    output_path = os.path.join(dirname, "mergedPDF.pdf")

    pdf_writer = PyPDF2.PdfWriter()

    for path in filename:
        pdf_reader = PyPDF2.PdfReader(path)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

    with open(output_path, 'wb') as out:
        pdf_writer.write(out)