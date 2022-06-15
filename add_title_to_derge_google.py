import os
import re
import yaml
import logging
from pathlib import Path
from diff_match_patch import diff_match_patch
from openpecha.utils import load_yaml

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




def get_correctd_text(heading, title, tibetan_text, remaining_texts):
    string = heading
    # if text_id not in string:
    #     string += string+f"{text_id}"
    string += title+"\n"
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
    if re.search(r"{[A-Z][0-9]+[a-z]?\}", target_text):
        match = re.match(r"(.*?)(\n\{[A-Z][0-9]+[a-z]?\})(.*?)", target_text)
        heading = match.group(1)
        middle = match.group(2)
        tibetan_text = target_text.replace(heading, "")
        tibetan_text = tibetan_text.replace(middle, "")
        heading += middle
        return heading, tibetan_text
    else:
        return None, None
    # tibetan_text = target_text.replace(heading, "")
    # tibetan_text = tibetan_text.replace(middle, "")
    # heading += middle
    # return heading, tibetan_text

def clean_text(text):
    text = re.sub(r"\n", "", text)
    text = re.sub(r"\#", "", text)
    return text

def get_the_first_page_only(vol_text):
    result = []
    pg_text = ""
    pages = re.split(r"(\〔[𰵀-󴉱]?[0-9]+\〕)", vol_text)
    for i, page in enumerate(pages[1:]):
        if i == 0:
            first_text = page
        elif i == 1:
            first_text += page
        else:
            pg_text += page
            result.append(pg_text)
            pg_text = ""

    return first_text, result

def check_title(tibetan_text,title):
    if re.search(fr"༄༅། །{title}", tibetan_text):
        return None
    else:
        return f"༄༅། །{title}"

def add_title(hfml_name, title):
    target_pecha = Path(f"./hfml/derge_google_pedurma/{hfml_name}").read_text(encoding='utf-8')
    target_text, remaining_text = get_the_first_page_only(target_pecha)
    heading, tibetan_text = seperate_text_at_first_tibetan(target_text)
    title = check_title(tibetan_text,title)
    if title:
        corrected_text = get_correctd_text(heading, title, tibetan_text, remaining_text)
        Path(f"./titled_hfml/{hfml_name}").write_text(corrected_text, encoding='utf-8')

def get_text_id_and_title(pedurma_outline, hfml_name):
    pecha_name = hfml_name[:-4]
    map = re.match(r"([A-Z][0-9]+[a-z]?)\_(v[0-9]+)",pecha_name)
    text_id = map.group(1)
    
    for _, outline_info in pedurma_outline.items():
            if outline_info['rkts_id'] == text_id:
                title = outline_info['text_title']
                return text_id, title


def copy_hfml(hfml_name):
    from_path = Path(f"./hfml/derge_google_pedurma/{hfml_name}")
    to_path = Path(f"./titled_hfml/{hfml_name}")
    os.system(f"cp -R {from_path} {to_path}")

if __name__ == "__main__":
    pedurma_outline_path = Path(f"./pedurma_outline.yml")
    pedurma_outline = load_yaml(pedurma_outline_path)
    hfml_names = os.listdir(Path(f"./hfml/derge_google_pedurma"))
    hfml_names.sort()
    for hfml_name in hfml_names:
            text_id, title = get_text_id_and_title(pedurma_outline, hfml_name)
            add_title(hfml_name, title)