import os
import re
import yaml
import logging
from pathlib import Path
from diff_match_patch import diff_match_patch

def clean_tibetan_text(tibetan_text):
    lines = re.split(r"\n", tibetan_text)
    page = ""
    clean = False
    for line in lines:
        if clean == False:
            if re.search(r"[།རྒྱ་གར་སྐད་དུ།]", line):
                page += line
                page += "\n"
                clean = True
            elif re.search(r":", line):
                continue
            elif line == '':
                continue
            else:
                page += line
                page += "\n"
                clean = True
        else:
            page += line
            page += "\n"
    return page




def get_correctd_text(heading, diff,tibetan_text, remaining_texts):
    string = heading
    string += "\n"
    string += diff
    string += tibetan_text
    for text in remaining_texts:
        string += text
    return string

def get_only_first_text_diff(diffs):
    new_diffs = []
    for diff in diffs:
        if diff[0] == -1:
            if re.search(r"།རྒྱ་གར་སྐད་དུ།", diff[1]):
                return diff[1]
            if re.search(r"[0-9]+", diff[1]):
                continue
            elif re.search(r"\s", diff[1]):
                continue
            else:
                new_diffs.append(diff)
                print(diff[1])
    if len(new_diffs) == 1:
        if re.search(r"[༄༅|༄༅༅|༄]", new_diffs[0][1]):
            return new_diffs[0][1]
    elif len(new_diffs) >= 2:
        return new_diffs[0][1]
    else:
        return None

def get_the_diffs(source_text, target_text):
    dmp = diff_match_patch()
    diffs = dmp.diff_main(source_text, target_text)
    return diffs

def seperate_text_at_first_tibetan(target_text):
    match = re.match(r"(.*?)(\n\{\D[0-9]+\})(.*?)", target_text)
    heading = match.group(1)
    middle = match.group(2)
    tibetan_text = target_text.replace(heading, "")
    tibetan_text = tibetan_text.replace(middle, "")
    heading += middle
    return heading, tibetan_text

def clean_text(text):
    text = re.sub(r"\n", "", text)
    text = re.sub(r"\#", "", text)
    return text

def get_the_first_page_only(vol_text, type):
    result = []
    pg_text = ""
    pages = re.split(r"(\[[𰵀-󴉱]?[0-9]+[a-z]{1}\])", vol_text)
    if type == "target":
        for i, page in enumerate(pages[1:]):
            if i == 0:
                first_text = page
            elif i == 1:
                first_text += page
            else:
                pg_text += page
                result.append(pg_text)
                pg_text = ""
    else:
        for i, page in enumerate(pages[1:]):
            if i % 2 == 0:
                pg_text += page
            elif i == 1:
                first_text = page
                result = None

    return first_text, result

def correct_google_text(pecha_name):
    file_info_yml = Path(f"./text_id_and_vol_num.yml").read_text(encoding='utf-8')
    file_info = yaml.safe_load(file_info_yml)
    if len(pecha_name) == 10:
        pecha_id = pecha_name[:-5]
    elif len(pecha_name) == 11:
        pecha_id = pecha_name[:-6]
    vol_num = file_info[pecha_id]['vol']
    source_pecha = Path(f"./hfmls/derge/{pecha_id}.txt").read_text(encoding='utf-8')
    target_pecha = Path(f"./hfmls/derge_google_pedurma/{pecha_id}_{vol_num}.txt").read_text(encoding='utf-8')
    target_text, remaining_text = get_the_first_page_only(target_pecha, "target")
    source_text, _ = get_the_first_page_only(source_pecha,"source")
    source_text = clean_text(source_text)
    heading, tibetan_text = seperate_text_at_first_tibetan(target_text)
    target_text = clean_text(target_text)
    diffs = get_the_diffs(source_text, target_text)
    diff = get_only_first_text_diff(diffs)
    if diff != None:
        tibetan_text = clean_tibetan_text(tibetan_text)
        corrected_text = get_correctd_text(heading, diff, tibetan_text, remaining_text)
        Path(f"./after_clean/derge_google_pedurma/{pecha_id}_{vol_num}.txt").write_text(corrected_text, encoding='utf-8')

if __name__=="__main__":
    Path()
