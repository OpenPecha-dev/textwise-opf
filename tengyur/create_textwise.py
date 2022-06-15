import re
from pathlib import Path
import logging
from openpecha.serializers import HFMLSerializer
from openpecha.utils import load_yaml

logging.basicConfig(
    filename="nalada_text_special_cases.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
)

def notifier(msg):
    logging.info(msg)

def get_hfml_text(opf_path, text_id, index=None):
    serializer = HFMLSerializer(opf_path, text_id=text_id, index_layer=index, layers=['Pagination', 'Durchen'])
    serializer.apply_layers()
    hfml_text = serializer.get_result()
    return hfml_text

# def get_pages(vol_text):
#     result = []
#     pg_text = ""
#     pages = re.split(r"(\〔[𰵀-󴉱]?[0-9]+\〕)", vol_text)
#     for i, page in enumerate(pages[1:]):
#         if i % 2 == 0:
#             pg_text += page
#         else:
#             pg_text += page
#             result.append(pg_text)
#             pg_text = ""
#     return result

# def clean_page(pg_text):
#     pg_text = re.sub(r"\〔[𰵀-󴉱]?[0-9]+\〕.*","", pg_text)
#     pg_text = re.sub(r"[𰵀-󴉱]", "", pg_text)
#     pg_text = pg_text.strip()
#     return pg_text

# def get_page_num(page_ann):
#     pg_num = int(page_ann[:-1]) * 2
#     pg_face = page_ann[-1]
#     if pg_face == "a":
#         pg_num -= 1
#     return pg_num

# def save_pagewise(hfmls, text_id, pecha_name):
#     for vol_num, hfml in hfmls.items():
#         vol_num = int(vol_num[1:])
#         vol_path = Path(f'./hfmls/{pecha_name}/{text_id}_{vol_num:03}/').mkdir(parents=True, exist_ok=True)
#         pages = get_pages(hfml)
#         for page in pages:
#             pg_num = re.search(r"\〔[𰵀-󴉱]?([0-9]+)\〕", page).group(1)
#             # pg_num = get_page_num(pg_idx)
#             # pg_text = clean_page(page)
#             Path(f'./hfmls/{pecha_name}/{text_id}_{vol_num:03}/{pg_num:04}.txt').write_text(page, encoding='utf-8')

def save_text(hfml_text, text_id, type):
    text = ''
    for vol_id, hfml in hfml_text.items():
        text = hfml
    # if len(hfml_text) == 1:
        Path(f'./hfml/{type}/{text_id}_{vol_id}.txt').write_text(text, encoding='utf-8')
    # else:
    #     print(text_id)
        print(f'{text_id} saved..')

def check_text_id(text_id, pedurma_index):
    vol = []
    annotations = pedurma_index["annotations"]
    for _, info in annotations.items():
        if info["work_id"] == text_id:
            if len(info["span"]) > 1:
                for i in range(0, len(info["span"])):
                    vol_num = info["span"][i]["vol"]
                    vol.append(vol_num)
                    vol_num = ""
                if vol[0] == vol[1]:
                    notifier(f"{text_id} same volumes")
                else:
                    notifier(f"{text_id} different volumes")
                return False
            else:
                return True
    


if __name__ == "__main__":
    derge_id = "12d32eb31c1a4cc59741cda99ebc7211"
    namsel_id = "187ed94f85154ea5b1ac374a651e1770"
    derge_path = Path(f'./tengyur/new_opf/{derge_id}/{derge_id}.opf/')
    namsel_path = Path(f'./tengyur/new_opf/{namsel_id}/{namsel_id}.opf/')
    namsel_pedurma_index = load_yaml((namsel_path / 'index.yml'))
    derge_pedurma_index = load_yaml((derge_path / 'index.yml'))
    nalanda_texts = Path('./tengyur/nalanda_text_list.txt').read_text(encoding='utf-8')
    nalanda_text_ids = nalanda_texts.splitlines()
    for nalanda_text_id in nalanda_text_ids:
        text_hfml = get_hfml_text(derge_path, nalanda_text_id, index=derge_pedurma_index)
        save_text(text_hfml, nalanda_text_id, "derge_google_pedurma")
        text_hfml = get_hfml_text(derge_path, nalanda_text_id, index=namsel_pedurma_index)
        save_text(text_hfml, nalanda_text_id, "namsel_pedurma")
        print(f'{nalanda_text_id} completed..')
            