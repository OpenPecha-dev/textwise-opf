from pathlib import Path
import os
import json
import re

def write_list(list, filename):
    final_list = ""
    for item in list:
        final_list += item+"\n"
    Path(f"{filename}").write_text(final_list, encoding='utf-8')

def check_text_ids_in_dic(text_ids, filename):
    not_present_list = []
    json_list = Path(f"{filename}").read_text(encoding='utf-8')
    list = json.loads(json_list)
    for text_id in text_ids:
        if text_id in list.keys():
            pass
        else:
            not_present_list.append(text_id)
    return not_present_list

def check_text_ids_in_list(list, filename):
    not_present_list = []
    text_ids = Path(f"{filename}").read_text(encoding='utf-8')
    text_ids = text_ids.splitlines()
    for item in list:
        if item in text_ids:
            pass
        else:
            not_present_list.append(item)
    return not_present_list

def get_text_ids(filename):
    text_ids = Path(f"{filename}").read_text(encoding='utf-8')
    return text_ids.splitlines()

if __name__ =="__main__":
    # text_ids = get_text_ids("./final_nalanda_list.txt")
    # list = check_text_ids_in_list(text_ids, "./t_text_list.json")
    # list = check_text_ids_in_list(list, "./no_note_ref.json")
    text_ids = get_text_ids("./need_to_prepare_nalanda_text_list.txt")
    list = check_text_ids_in_dic(text_ids, "./t_text_list.json")
    list = check_text_ids_in_dic(list, "./no_note_ref.json")
    final_list = check_text_ids_in_list(list, "./in_index_but_opf_not_made.txt")
    write_list(final_list, "./text_not_in_index.txt")