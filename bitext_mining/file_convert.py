import subprocess
import os


def doc_to_docx(doc_file_path):
    output_dir = os.path.dirname(doc_file_path)
    returncode = subprocess.call(
        ['soffice', '--headless', '--convert-to', 'docx', '--outdir', output_dir, doc_file_path])
    return returncode


def rtf_to_docx(rtf_file_path):
    output_dir = os.path.dirname(rtf_file_path)
    returncode = subprocess.call(
        ['soffice', '--headless', '--convert-to', 'docx', '--outdir', output_dir, rtf_file_path])
    return returncode