from docx import Document

wordDoc = Document("demo1.docx")
doc_body = wordDoc.element.xml

with open('file1.xml', 'w') as file:
    file.write(doc_body)
