import time
import csv
import json
start_time = time.time()

with open("../data/data/noisy_cleaned.en-zh") as file, open("../data/data/noisy_0_85_sorted.en-zh", 'w', encoding='utf8') as fOUT:
    list=[]
    for line in file:
        list.append(line)
    list.sort(reverse=True)
    
    fOUT.write(''.join(list))


# with open("../data/sentence_pair.csv", encoding='utf8') as fIN,\
#         open("../data/clean_sorted.en-zh", 'w', encoding='utf8') as fOUT:
#     for line in
#     for sentence_pair in sentence_pairs:
#         fOUT.write("{:.4f} | {} | {}\n".format(
#             sentence_pair['cos'], sentence_pair['sentence_en'], sentence_pair['sentence_zh']))


print("--- %s seconds ---" % (time.time() - start_time))
