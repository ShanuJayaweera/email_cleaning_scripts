import os
import sys
import re
import pandas as pd


def create_folder(folder_name):
    output_folder = os.path.dirname(str(os.path.abspath(sys.argv[0]))) + r"/" + str(folder_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder


def email_syntax_validate(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def chunks(email_arr, n):
    return [email_arr[i:i + n] for i in range(0, len(email_arr), n)]


def remove_duplicates(email_arr):
    return list(dict.fromkeys(email_arr))


def read_folder_txt(dir_path):
    arr = os.listdir(dir_path)
    validated_email_arr = []

    for file_name in arr:
        with open(str(dir_path) + "/" + file_name) as f:
            lines = f.readlines()
            for line in lines:
                if email_syntax_validate(str(line).strip()):
                    validated_email_arr.append(str(line).strip())
        break

    duplicate_removed_arr = remove_duplicates(validated_email_arr)
    chunk_email_arr = chunks(duplicate_removed_arr, 200)
    folder_path = create_folder("output")
    create_csv(chunk_email_arr, folder_path, "adult")


def create_csv(chunk_email_arr, folder_path, file_pre):
    for i, ch in enumerate(chunk_email_arr):
        file_path = folder_path + "/" +str(file_pre) + str(i) + ".csv"
        df = pd.DataFrame(ch)
        df.to_csv(file_path, index=False, header=None)


read_folder_txt("Adult")
