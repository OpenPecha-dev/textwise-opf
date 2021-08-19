
import os
import re
import logging
from pathlib import Path
from diff_match_patch import diff_match_patch


logging.basicConfig(
    filename="derge_google_correction.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
)

def notifier(msg):
    logging.info(msg)

def clean_tibetan_text(tibetan_text):
    lines = re.split(r"\n", tibetan_text)
    page = ""
    clean = False
    for line in lines:
        if clean == False:
            if re.search(r"[U+0F68-U+0F60]", line):
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

def get_only_first_text_diff(diffs, text_id):
    new_diffs = []
    for diff in diffs:
        if diff[0] == -1:
            if re.search(r"[0-9]+", diff[1]):
                continue
            else:
                new_diffs.append(diff)
                print(diff[1])
    if len(new_diffs) == 1:
        notifier(f"{text_id} has only one diff")
        return None
    elif len(new_diffs) != 0:
        return new_diffs[0]
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

if __name__=="__main__":
    target_path = Path(f"./hfmls/derge_google_pedurma/")
    for file in os.listdir(target_path):
        if file.endswith(".txt"):
            file_name = file[:-4]
            text_id = file_name[:-5]
            source_pecha = Path(f"./hfmls/derge/{text_id}.txt").read_text(encoding='utf-8')
            target_pecha = Path(f"./hfmls/derge_google_pedurma/{file_name}.txt").read_text(encoding='utf-8')
            target_text, remaining_text = get_the_first_page_only(target_pecha, "target")
            if source_pecha != '':
                source_text, _ = get_the_first_page_only(source_pecha,"source")
                source_text = clean_text(source_text)
                heading, tibetan_text = seperate_text_at_first_tibetan(target_text)
                diffs = get_the_diffs(source_text, target_text)
                diff = get_only_first_text_diff(diffs, text_id)
                if diff != None:
                    tibetan_text = clean_tibetan_text(tibetan_text)
                    corrected_text = get_correctd_text(heading, diff[1], tibetan_text, remaining_text)
                    Path(f"./test/{file_name}.txt").write_text(corrected_text, encoding='utf-8')
                    notifier(f"{file_name[:-5]} is corrected")
                else:
                    notifier(f"{file_name[:-5]} no diff")
            else:
                notifier(f"{file_name[:-5]}'s source is empty")