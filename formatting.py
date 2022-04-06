with open("../noisy/ccmatrix/CCMatrix.en-zh.tmx", encoding='utf8') as fin, open("English.txt", 'w', encoding='utf8') as fOUT_en, open("Chinese.txt", 'w', encoding='utf8') as fOUT_zh:
    for i, sentence in enumerate(fin):
        if i in range(12, 1000000000, 4):
            fOUT_en.write(sentence[30:-13]+'\n')
        if i in range(13, 1000000000, 4):
            fOUT_zh.write(sentence[30:-13]+'\n')
            print(i)