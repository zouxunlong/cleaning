# import re

# pattern_punctuation = r"""[!?,.:;"#$£€%&'()+-_/<≤=≠≥>@[\]^{|}，。、—‘’“”：；【】￥…《》？！（）]"""
# pattern_arabic = r"[\u0600-\u06FF]"
# pattern_chinese = r"[\u4e00-\u9fff]"
# pattern_tamil = r"[\u0B80-\u0BFF]"
# pattern_russian = r"[\u0400-\u04FF]"
# pattern_korean = r"[\uac00-\ud7a3]"
# pattern_japanese = r"[\u3040-\u30ff\u31f0-\u31ff]"
# pattern_vietnamese = r"[àáãạảăắằẳẵặâấầẩẫậèéẹẻẽêềếểễệđìíĩỉịòóõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳỵỷỹýÀÁÃẠẢĂẮẰẲẴẶÂẤẦẨẪẬÈÉẸẺẼÊỀẾỂỄỆĐÌÍĨỈỊÒÓÕỌỎÔỐỒỔỖỘƠỚỜỞỠỢÙÚŨỤỦƯỨỪỬỮỰỲỴỶỸÝ]"
# pattern_emoji = r'[\U0001F1E0-\U0001F1FF\U0001F300-\U0001F64F\U0001F680-\U0001FAFF\U00002702-\U000027B0]'

# text='•	Facilitating crew change（进行海员换班）and ensuring that our maritime frontline workers were vaccinated （海员也都能接种疫苗）'
# text=re.sub(
#             r'[^a-zA-Z0-9\s\n\t{}{}{}{}{}{}{}{}{}]'.format(
#                 pattern_punctuation[1:-1],
#                 pattern_arabic[1:-1],
#                 pattern_chinese[1:-1],
#                 pattern_tamil[1:-1],
#                 pattern_russian[1:-1],
#                 pattern_korean[1:-1],
#                 pattern_japanese[1:-1],
#                 pattern_vietnamese[1:-1],
#                 pattern_emoji[1:-1],
#             ), ' ', text.strip()).strip()
# results = re.findall(
#     r'(?=((\s[^\s】）\]\)]+){2,7})\s?[\(\[（【](.+?)[】）\]\)])', text)
# results2 = re.findall(
#     r'(?=(^[^\(\[（【】）\]\)]+)\s?[\(\[（【](.+?)[】）\]\)])', text)
# print(results2)
# print(results)


a={1,2}
b={1,3}
print(a-b)