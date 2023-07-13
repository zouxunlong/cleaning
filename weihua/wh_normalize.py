

import math


def normalize(file_path_in, file_path_out):
    with open(file_path_in, encoding='utf8') as file_in:

        new_lines = ["{:.4f}{}".format(float(line[:7])*math.log(2),line[7:])for line in file_in]
   
    with open(file_path_out, 'a', encoding='utf8') as f_out:
        for k in new_lines:
            f_out.write(k)

    print("finished " + file_path_out, flush=True)


def main():

    normalize('/home/xuanlong/dataclean/data/translation_perplexity.txt',
               '/home/xuanlong/dataclean/data/translation_perplexity_normalized.txt',)


if __name__ == '__main__':
    main()
