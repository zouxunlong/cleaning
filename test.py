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


# def get_dp(M):
#     m = len(M)
#     n = len(M[0])
#     dp = [[0]*n for i in range(m)]
#     dp[0] = [sum(M[0][:i+1]) for i in range(n)]
#     for i in range(1, m):
#         dp[i][0] = dp[i-1][0] + M[i][0]

#     for i in range(1, m):
#         for j in range(1, n):
#             dp[i][j] = max(dp[i-1][j], dp[i][j-1]) + M[i][j]
#     return dp



# def yield_coordinate(dp,coordinate):

#     if coordinate[0] == 0:
#         return (coordinate[0], coordinate[1]-1)
#     elif coordinate[1] == 0:
#         return (coordinate[0]-1, coordinate[1])
#     elif dp[coordinate[0]-1][coordinate[1]] >= dp[coordinate[0]][coordinate[1]-1]:
#         return (coordinate[0]-1, coordinate[1])
#     else:
#         return (coordinate[0], coordinate[1]-1)



# M = [[3, 2, 1], [5, 2, 1], [4, 12, 2], [10, 9, 3]]

# def get_path(M):

#     coordinate=(len(M)-1,len(M[0])-1)
#     path=[coordinate]
#     dp=get_dp(M)

#     while coordinate!=(0,0):
#         coordinate=yield_coordinate(dp,coordinate)
#         path.append(coordinate)
#     return path


# print(get_path(M))



# import re
# import string
# import pycld2 as cld2
# import cld3
# import fasttext
# model_fasttext = fasttext.load_model('../model/lid.176.bin')

# def lang_detect(text_for_lang_detect):

#     lang_detected = set()

#     text_for_lang_detect = re.sub(
#         "(?i)\w+@\S+\s?|http\S*\s?|www\.\S*\s?|[a-z\.]*\.sg\S*\s?|[0-9]+\s?", "", text_for_lang_detect)
#     text_for_lang_detect = text_for_lang_detect.translate(
#         str.maketrans('-', ' ', string.punctuation.replace('-', ''))).strip().lower()

#     if text_for_lang_detect:
#         if re.search('[\u4e00-\u9fff]', text_for_lang_detect):
#             lang_detected.add('zh')
#         if re.search('[\u0B80-\u0BFF]', text_for_lang_detect):
#             lang_detected.add('ta')
#         if re.search('[àáãạảăắằẳẵặâấầẩẫậèéẹẻẽêềếểễệđìíĩỉịòóõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳỵỷỹýÀÁÃẠẢĂẮẰẲẴẶÂẤẦẨẪẬÈÉẸẺẼÊỀẾỂỄỆĐÌÍĨỈỊÒÓÕỌỎÔỐỒỔỖỘƠỚỜỞỠỢÙÚŨỤỦƯỨỪỬỮỰỲỴỶỸÝ]', text_for_lang_detect):
#             lang_detected.add('vi')

#         try:
#             lang_by_cld2 = cld2.detect(text_for_lang_detect)[2][0][1]
#             lang_by_cld3 = cld3.get_language(text_for_lang_detect)[0]
#             lang_by_fasttext = model_fasttext.predict(
#                 text_for_lang_detect)[0][0][-2:]

#             if {"en"} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
#                 lang_detected.add('en')
#             if {'ms', 'id'} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
#                 lang_detected.add('ms')
#                 lang_detected.add('id')
#             if {'vi'} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
#                 lang_detected.add('vi')
#         except Exception as err:
#             print(err)

#     return lang_detected


# lang_detect('Pseudoryx nghetinhensis')

if (True) and ((True and False) or (True and False)):
    print('hello')