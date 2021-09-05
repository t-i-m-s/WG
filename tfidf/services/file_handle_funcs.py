from django.core.files.uploadedfile import UploadedFile
import re


def get_words(uploaded_file: UploadedFile) -> list['str']:
    word_regex = r'[^\s\n\t]+'
    _bytes: bytes = uploaded_file.read()
    text: str = _bytes.decode('utf-8')
    return re.findall(word_regex, text)


def name_valid(filename: str) -> bool:
    accept_formats = {'.txt', }
    for f in accept_formats:
        filename_regex = rf'^.+\{f}$'
        if re.match(filename_regex, filename):
            return True
    return False
