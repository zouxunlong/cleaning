with open("./noisy/ccmatrix/Chinese.txt", encoding='utf8') as fin, open("./noisy/ccmatrix/Chinese_0_to_10m.txt", 'w', encoding='utf8') as fOUT_1,open("./noisy/ccmatrix/Chinese_10m_to_20m.txt", 'w', encoding='utf8') as fOUT_2, open("./noisy/ccmatrix/Chinese_20m_to_30m.txt", 'w', encoding='utf8') as fOUT_3, open("./noisy/ccmatrix/Chinese_30m_to_40m.txt", 'w', encoding='utf8') as fOUT_4, open("./noisy/ccmatrix/Chinese_40m_to_50m.txt", 'w', encoding='utf8') as fOUT_5, open("./noisy/ccmatrix/Chinese_50m_to_60m.txt", 'w', encoding='utf8') as fOUT_6, open("./noisy/ccmatrix/Chinese_60m_to_70m.txt", 'w', encoding='utf8') as fOUT_7, open("./noisy/ccmatrix/Chinese_70m_to_80m.txt", 'w', encoding='utf8') as fOUT_8, open("./noisy/ccmatrix/Chinese_80m_to_90m.txt", 'w', encoding='utf8') as fOUT_9, open("./noisy/ccmatrix/Chinese_90m_to_100m.txt", 'w', encoding='utf8') as fOUT_10:
    for i, sentence in enumerate(fin):
        if i in range(10000000):
            fOUT_1.write(sentence)
            print(i)
        if i in range(10000000, 20000000):
            fOUT_2.write(sentence)
            print(i)
        if i in range(20000000, 30000000):
            fOUT_3.write(sentence)
            print(i)
        if i in range(30000000, 40000000):
            fOUT_4.write(sentence)
            print(i)
        if i in range(40000000, 50000000):
            fOUT_5.write(sentence)
            print(i)
        if i in range(50000000, 60000000):
            fOUT_6.write(sentence)
            print(i)
        if i in range(60000000, 70000000):
            fOUT_7.write(sentence)
            print(i)
        if i in range(70000000, 80000000):
            fOUT_8.write(sentence)
            print(i)
        if i in range(80000000, 90000000):
            fOUT_9.write(sentence)
            print(i)
        if i in range(90000000, 100000000):
            fOUT_10.write(sentence)
            print(i)