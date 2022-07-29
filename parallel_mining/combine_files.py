import os


def inject_from_file(file, output_filepath):
    with open(file, encoding='utf8') as fIN, open(output_filepath, 'a', encoding='utf8') as fOUT:
        for i, sentence in enumerate(fIN):
            if sentence.strip():
                fOUT.write(sentence.strip()+'\n')


def combine_files_in_dir(rootdir):

    file_combined=0

    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith('.en-ta') or file.endswith('.EN-TA'):
                inject_from_file(os.path.join(root, file), str(rootdir)+'_combined.en-ta')
                file_combined+=1
            if file.endswith('.en-ms') or file.endswith('.EN-MS'):
                inject_from_file(os.path.join(root, file), str(rootdir)+'_combined.en-ms')
                file_combined+=1
            if file.endswith('.en-zh') or file.endswith('.EN-ZH'):
                inject_from_file(os.path.join(root, file), str(rootdir)+'_combined.en-zh')
                file_combined+=1

    print("Done. {} file combined".format(file_combined),flush=True)


# combine_files_in_dir('/home/xuanlong/dataclean/data/Batch_15_extracted')