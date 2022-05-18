# import re
# import string
# import sys
# import pycld2 as cld2
# import cld3
# import fasttext

# model_fasttext = fasttext.load_model('../model/lid.176.bin')


# def lang_detect(text_for_lang_detect):
#     original_len=len(text_for_lang_detect)

#     lang_detected = set()

#     text_for_lang_detect = re.sub(
#         "(?i)\w+@\S+\s?|http\S*\s?|www\.\S*\s?|[a-z\.]*\.sg\S*\s?|[0-9]+\s?", "", text_for_lang_detect)
#     text_for_lang_detect = text_for_lang_detect.translate(
#         str.maketrans('-', ' ', string.punctuation.replace('-', ''))).strip().lower()

#     trimmed_len=len(text_for_lang_detect)

#     if text_for_lang_detect:
#         if re.search('[\u4e00-\u9fff]', text_for_lang_detect):
#             lang_detected.add('zh')
#         if re.search('[\u0B80-\u0BFF]', text_for_lang_detect):
#             lang_detected.add('ta')
#         if re.search('[\u0400-\u04FF]', text_for_lang_detect):
#             lang_detected.add('ru')
#         if re.search('[\uac00-\ud7a3]', text_for_lang_detect):
#             lang_detected.add('ko')
#         if re.search('[\u3040-\u30ff\u31f0-\u31ff]', text_for_lang_detect):
#             lang_detected.add('ja')
#         if re.search('[\u0A00-\u0A7F]', text_for_lang_detect):
#             lang_detected.add('pa')
#         if re.search('[àáãạảăắằẳẵặâấầẩẫậèéẹẻẽêềếểễệđìíĩỉịòóõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳỵỷỹýÀÁÃẠẢĂẮẰẲẴẶÂẤẦẨẪẬÈÉẸẺẼÊỀẾỂỄỆĐÌÍĨỈỊÒÓÕỌỎÔỐỒỔỖỘƠỚỜỞỠỢÙÚŨỤỦƯỨỪỬỮỰỲỴỶỸÝ]', text_for_lang_detect):
#             lang_detected.add('vi')

#         try:
#             lang_by_cld2 = cld2.detect(text_for_lang_detect)[2][0][1]
#             lang_by_cld3 = cld3.get_language(text_for_lang_detect)[0]
#             lang_by_fasttext = model_fasttext.predict(
#                 text_for_lang_detect)[0][0][-2:]

#             if {"en"} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
#                 lang_detected.add('en')
#             if {'ms'} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
#                 lang_detected.add('ms')
#             if {'id'} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
#                 lang_detected.add('id')
#             if {'vi'} & {lang_by_cld2, lang_by_cld3, lang_by_fasttext}:
#                 lang_detected.add('vi')
                
#         except BaseException as err:
#             exception_type, exception_object, exception_traceback = sys.exc_info()
#             filename = exception_traceback.tb_frame.f_code.co_filename
#             line_number = exception_traceback.tb_lineno

#             print("Exception type: ", exception_type, flush=True)
#             print("File name: ", filename, flush=True)
#             print("Line number: ", line_number, flush=True)
#             print(err)

#     return lang_detected

# lang_detect('ਜਰਾਈਲੁ ਯਾਰੁ ਬੰਦੇ ਜਿਸੁ ਤੇਰਾ ਆ')


import re

lines=['This platform was launched in response to growing health, and social and emotional wellbeing concerns related to the pandemic\\n\nWe will continue to develop the content and resources made available to encourage self-help and self-management of stress and coping issues faced by the population | 推出此平台是为了应对因大流行病而与日俱增的健康、社会和心理健康问题\n\n我们将继续推出各种服务和资源，以鼓励民众在面对压力和问题时自助及进行自我管理']
for line in lines:
    en_sent = ' '.join(re.sub("(?i)\\\\n", " ", line).strip().split())
    print(' '.join(en_sent.split()))
