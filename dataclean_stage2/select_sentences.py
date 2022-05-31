

with open('/home/xuanlong/dataclean/data/parallel_combined/parallel.en-ms', encoding='utf8') as f_in, \
    open('/home/xuanlong/dataclean/data/parallel_combined/parallel_4m.en-ms', 'w', encoding='utf8') as f_out:
    for i,line in enumerate(f_in):
        if i<200000:
            continue
        if i >= 4200000:
            break
        f_out.write(line)

