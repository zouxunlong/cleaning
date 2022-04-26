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

# import pycld2 as cld2
# import cld3
# import fasttext
# from googletrans import Translator

# translator = Translator()
# model_fasttext = fasttext.load_model('../model/lid.176.bin')

# text_for_lang_detect = "领取ர் 21, 2020, "

# lang_by_cld2 = cld2.detect(text_for_lang_detect)[2][0][1]
# lang_by_cld3 = cld3.get_language(text_for_lang_detect)[0]
# lang_by_fasttext = model_fasttext.predict(
#     text_for_lang_detect)[0][0]
# lang_by_google = translator.detect(text_for_lang_detect)

# print(lang_by_cld2)
# print(lang_by_cld3)
# print(lang_by_fasttext)
# print(lang_by_google)
# if re.search('[\u4e00-\u9fff]', text_for_lang_detect):
#     print('chinese detect')
# if re.search('[\u0B80-\u0BFF]', text_for_lang_detect):
#     print('tamil detect')


s = sum([True,True,True,False])

print(s)

