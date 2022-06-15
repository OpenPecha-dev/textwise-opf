from pathlib import Path
import re
import os

def write_text(text_list, hfml_name):
    new_text = ""
    for text in text_list:
        new_text += text
    Path(f"./hfml/derge_google_pedurma/corrected.txt").write_text(new_text, encoding='utf-8')


def correct_page_num(page_num):
    symbol = page_num[0]
    num = int(page_num[1]) + 1
    page = f"〔{symbol}{num}〕"
    return page


def get_new_text(text):
    result = []
    pg_text = ""
    pages = re.split(r"(\〔[𰵀-󴉱]?[0-9]+\〕)", text)
    for i, page in enumerate(pages[1:]):
        if re.search(r"(\〔[𰵀-󴉱]?[0-9]+\〕)", page):
            match = re.match(r"\〔([𰵀-󴉱])?([0-9]+)\〕", page)
            page_num = match.groups(1)
            page = correct_page_num(page_num)
        if i % 2 == 0:
            pg_text += page
        else:
            pg_text += page
            result.append(pg_text)
            pg_text = ""
    return result




if __name__ == "__main__":
    path = Path(f"./hfml/derge_google_pedurma/")
    hfml_names = ["D2905_v037.txt"]
    hfml_names.sort()
    for hfml_name in hfml_names:
        text = Path(path/hfml_name).read_text(encoding='utf-8')
        new_text = get_new_text(text)
        write_text(new_text, hfml_name)
        