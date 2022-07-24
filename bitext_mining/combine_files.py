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
                inject_from_file(os.path.join(root, file), rootdir+'.en-ta')
                file_combined+=1
            if file.endswith('.en-ms') or file.endswith('.EN-MS'):
                inject_from_file(os.path.join(root, file), rootdir+'.en-ms')
                file_combined+=1
            if file.endswith('.en-zh') or file.endswith('.EN-ZH'):
                inject_from_file(os.path.join(root, file), rootdir+'.en-zh')
                file_combined+=1
            if file.endswith('.ta-en') or file.endswith('.TA-EN'):
                inject_from_file(os.path.join(root, file), rootdir+'.ta-en')
                file_combined+=1
            if file.endswith('.ms-en') or file.endswith('.MS-EN'):
                inject_from_file(os.path.join(root, file), rootdir+'.ms-en')
                file_combined+=1
            if file.endswith('.zh-en') or file.endswith('.ZH-EN'):
                inject_from_file(os.path.join(root, file), rootdir+'.zh-en')
                file_combined+=1
            if file.endswith('.en') or file.endswith('.EN'):
                inject_from_file(os.path.join(root, file), rootdir+'.en')
                file_combined+=1
            if file.endswith('.id') or file.endswith('.ID'):
                inject_from_file(os.path.join(root, file), rootdir+'.id')
                file_combined+=1
    print("Done. {} file combined".format(file_combined),flush=True)

if __name__ == '__main__':
    rootdir='/home/xuanlong/dataclean/data/500K sentences'
    combine_files_in_dir(rootdir)
