# from translate.storage.tmx import tmxfile

# with open("../WORK/noisy/ccmatrix/CCMatrix.en-zh.tmx", encoding='utf8') as fin:
#     tmx_file = tmxfile(fin, 'en', 'zh')

# with open("../WORK/noisy/ccmatrix/Chinese.txt", 'w', encoding='utf8') as chinese_file, open("../WORK/noisy/ccmatrix/English.txt", 'w', encoding='utf8') as english_file:
#     n = 0
#     for node in tmx_file.unit_iter():
#         english_file.write(node.source+"\n")
#         chinese_file.write(node.target+"\n")
#         n += 1
#         print(n)

with open("../WORK/noisy/ccmatrix/CCMatrix.en-zh.tmx", encoding='utf8') as fin, open("CCMatrix.en-zh.tmx", 'w', encoding='utf8') as fOUT:
    for i, sentence_zh in enumerate(fin):
        if i in range(11,1000000):
            fOUT.write(sentence_zh)
            print(i)