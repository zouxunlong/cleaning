with open("../data/noisy_cleaned.en-zh", encoding='utf8') as fin, \
        open("../data/noisy_1.en-zh", 'w', encoding='utf8') as fOUT_1, \
        open("../data/noisy_2.en-zh", 'w', encoding='utf8') as fOUT_2, \
        open("../data/noisy_3.en-zh", 'w', encoding='utf8') as fOUT_3, \
        open("../data/noisy_4.en-zh", 'w', encoding='utf8') as fOUT_4,\
        open("../data/noisy_5.en-zh", 'w', encoding='utf8') as fOUT_5, \
        open("../data/noisy_6.en-zh", 'w', encoding='utf8') as fOUT_6, \
        open("../data/noisy_7.en-zh", 'w', encoding='utf8') as fOUT_7, \
        open("../data/noisy_8.en-zh", 'w', encoding='utf8') as fOUT_8,\
        open("../data/noisy_9.en-zh", 'w', encoding='utf8') as fOUT_9,\
        open("../data/noisy_10.en-zh", 'w', encoding='utf8') as fOUT_10:
    for i, sentence in enumerate(fin):
        if i in range(10000000):
            fOUT_1.write(sentence)
        elif i in range(10000000, 20000000):
            fOUT_2.write(sentence)
        elif i in range(20000000, 30000000):
            fOUT_3.write(sentence)
        elif i in range(30000000, 40000000):
            fOUT_4.write(sentence)
        elif i in range(40000000, 50000000):
            fOUT_5.write(sentence)
        elif i in range(50000000, 60000000):
            fOUT_6.write(sentence)
        elif i in range(60000000, 70000000):
            fOUT_7.write(sentence)
        elif i in range(70000000, 80000000):
            fOUT_8.write(sentence)
        elif i in range(80000000, 90000000):
            fOUT_9.write(sentence)
        elif i in range(90000000, 100000000):
            fOUT_10.write(sentence)
