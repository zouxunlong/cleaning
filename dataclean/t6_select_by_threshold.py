import time


def sort(file_path):
    start_time = time.time()

    with open(file_path, encoding='utf8') as f_in, \
        open(file_path+'.seleted', 'w', encoding='utf8') as f_out:
        for line in f_in:
            sentences=line.split('|')
            if len(sentences)!=3:
                continue
            if float(sentences[0]) > 0.8191:
                f_out.write(line)
            else:
                break

    print("finished " + file_path)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':

    sort('/home/xuanlong/dataclean/data/Total/train.filtered.LaBSE.en-id')
