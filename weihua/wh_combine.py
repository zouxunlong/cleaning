

def combine_wh(file_path_src, file_path_tgt, file_path_perplexity, file_path_out):
    with open(file_path_src, encoding='utf8') as file_src, \
            open(file_path_tgt, encoding='utf8') as file_tgt, \
            open(file_path_perplexity, encoding='utf8') as file_perplexity:


        perplexity_score = [line.split()[1][:7] for line in file_perplexity]
        sentences_src = file_src.readlines()
        sentences_tgt = file_tgt.readlines()
   
    assert len(sentences_src) == len(
        sentences_tgt), "length of src and target don't match"
    assert len(perplexity_score) == len(
        sentences_tgt), "length of perplexity_score and target don't match"

    with open(file_path_out, 'a', encoding='utf8') as f_out:
        for k in range(len(sentences_src)):
            f_out.write("{:.4f} ||| {} ||| {}\n".format(
                float(perplexity_score[k]), sentences_src[k].replace("|", " ").strip(), sentences_tgt[k].replace("|", " ").strip()))

    print("finished " + file_path_out, flush=True)


def main():

    combine_wh('/home/xuanlong/dataclean/data/Eng_Long_Sentence.txt',
               '/home/xuanlong/dataclean/data/translation_modified.txt',
               '/home/xuanlong/dataclean/data/translation.txt',
               '/home/xuanlong/dataclean/data/translation_perplexity.txt',)


if __name__ == '__main__':
    main()
