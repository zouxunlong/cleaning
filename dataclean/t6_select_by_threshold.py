import time


def select(file_path):
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

    select('/home/xuanlong/dataclean/data/500K sentences/combined/500K sentences.labse.en-id')
