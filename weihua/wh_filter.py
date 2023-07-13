import time

def to_excel(file_path):

    import pandas as pd
    with open(file_path) as f_in:

        dicts = [{'average': float(line.split("|||")[0].strip()), 
                  'LaBSE': float(line.split("|||")[1].strip()),
                  'Perplexity': float(line.split("|||")[2].strip()),
                  'English': line.split("|||")[3].strip(),
                  'Tamil': line.split("|||")[4].strip()} for line in f_in]

    df = pd.DataFrame.from_dict(dicts)
    print (df)
    df.to_excel('filtered_10k.xlsx')

def filter(file_path, file_path_filtered):
    start_time = time.time()
    with open(file_path) as f_in:
        list = f_in.readlines()
    with open(file_path_filtered, 'w', encoding='utf8') as f_out:
        i=0
        for sentence in list:
            i+=1
            f_out.write(sentence)
            if i==10000:
                break
    list.clear()
    print("finished " + file_path)
    print("--- {} seconds ---".format(time.time() - start_time))


def get_average_score(line):
    return float(line.split("|||")[0].strip())


def sort(file_path,file_path_sorted):
    start_time = time.time()
    with open(file_path) as f_in:
        list = f_in.readlines()
        list.sort(key=get_average_score)
    with open(file_path_sorted, 'w', encoding='utf8') as f_out:
        for sentence in list:
            f_out.write(sentence)
    list.clear()
    print("finished " + file_path)
    print("--- {} seconds ---".format(time.time() - start_time))


if __name__ == '__main__':

    to_excel(
         '/home/xuanlong/dataclean/data/translation_average_sorted_10k.txt',
         )
