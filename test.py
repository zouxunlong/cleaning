# from docx import Document
# import re

# wordDoc = Document("2021MGPLetterTopupETCM1.docx")
# # s=wordDoc.element.xml
# # with open('file.xml', 'w') as file:
# #     file.write(s)

# def GetTag(element):
#     return "%s:%s" % (element.prefix, re.match("{.*}(.*)", element.tag).group(1))


# e=wordDoc.element
# p_elements = e.xpath('.//w:drawing//w:txbxContent')
# sentences=[]
# for p_element in p_elements:
#     print(GetTag(p_element))
#     print(p_element.tag)
#     # print(p_element.name())
#     t = " ".join(" ".join(p_element.xpath(".//text()").extract()).split())
#     sentences.append(t)
# print('dsa')
