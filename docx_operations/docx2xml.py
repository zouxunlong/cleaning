from docx import Document

wordDoc = Document("demo.docx")
doc_body = wordDoc.element.xml

with open('demo.xml', 'w') as file:
    file.write(doc_body)
