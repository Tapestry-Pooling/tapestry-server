import re


def check_and_fix_upload_file_name(id, file_name):
    file_name_pattern = "^[\w,\s-]+{}\.xlsx$".format(id)
    if re.search(file_name_pattern, file_name):
        return file_name
    name, ext = file_name.split(".")
    return "{}-{}.{}".format(name, id, ext)