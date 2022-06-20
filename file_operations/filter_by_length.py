

def keep_only_en(file):
    with open(file, encoding='utf8') as f_in, open(file+'.seleted','w',encoding='utf8') as f_out:
        for line in f_in:
            en_sent=line.split('|')[1].strip()
            if en_sent:
                f_out.write(en_sent+'\n')

def main():
    file_path='/home/xuanlong/dataclean/data/parallel_seleted/parallel.en-zh.seleted'
    keep_only_en(file_path)

if __name__=="__main__":
    main()