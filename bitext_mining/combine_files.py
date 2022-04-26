import os


def inject_from_file(file, output_filepath):
    with open(file, encoding='utf8') as fIN, open(output_filepath, 'a', encoding='utf8') as fOUT:
        for i, sentence in enumerate(fIN):
            fOUT.write(sentence)


def combine_files_in_dir(rootdir):

    file_combined=0

    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith('.en-ta'):
                inject_from_file(os.path.join(root, file), rootdir+'.en-ta')
                file_combined+=1
            if file.endswith('.en-ms'):
                inject_from_file(os.path.join(root, file), rootdir+'.en-ms')
                file_combined+=1
            if file.endswith('.en-zh'):
                inject_from_file(os.path.join(root, file), rootdir+'.en-zh')
                file_combined+=1

    print("Done. {} file combined".format(file_combined))
