

import math


def average(file_path_labse,file_path_perplexity, file_path_average):
    with open(file_path_labse, encoding='utf8') as file_labse,\
        open(file_path_perplexity, encoding='utf8') as file_perplexity:
        labse_score=[]
        sentences=[]
        for line in file_labse:
            labse_score.append(float(line.split("|||")[0].strip()))
            sentences.append("|||".join(line.split("|||")[1:]))
        perplexity_score = [float(line.split("|||")[0].strip()) for line in file_perplexity]
        average_score=[labse_score[i]+perplexity_score[i] for i in range(len(labse_score))]

        new_lines = ["{:.4f} ||| {:.4f} ||| {:.4f} |||{}".format(average_score[i],labse_score[i],perplexity_score[i], sentences[i]) for i in range(len(labse_score))]
   
    with open(file_path_average, 'a', encoding='utf8') as f_out:
        for k in new_lines:
            f_out.write(k)

    print("finished " + file_path_average, flush=True)


def main():

    average('/home/xuanlong/dataclean/data/translation_labse.txt',
            '/home/xuanlong/dataclean/data/translation_perplexity_normalized.txt',
            '/home/xuanlong/dataclean/data/translation_average.txt',)


if __name__ == '__main__':
    main()
