

with open('/home/xuanlong/dataclean/data/three_body_new', 'r', encoding='utf8') as f_in, \
        open('/home/xuanlong/dataclean/data/three_body_en', 'w', encoding='utf8') as f_out_en, \
        open('/home/xuanlong/dataclean/data/three_body_zh', 'w', encoding='utf8') as f_out_zh:
    for i, line in enumerate(f_in):
        if i%2==0 and line.strip():
            f_out_zh.write(line.strip()+'\n')
        elif i%2==1 and line.strip(): 
            f_out_en.write(line.strip()+'\n')
