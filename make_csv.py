from pathlib import Path
import json
import csv
import re
from pandas import DataFrame

def creat_json(list,list_json):
    curr_info = {}
    final_info = {}
    for id in list:
        google = list_json[id]['google']
        namsel = list_json[id]['namsel']
        title = list_json[id]['title']
        curr_info[id]= {
            'google': google,
            'namsel': namsel,
            'title': title
        }
        final_info.update(curr_info)
        curr_info = {}
    final_json = json.dumps(final_info, sort_keys=True, ensure_ascii=False)
    Path(f"./no_note_ref.json").write_text(final_json, encoding="utf-8")




def add_to_excel(text_ids, links, all_status):
    df = DataFrame({'Text_id':text_ids,'Link':links, 'Status':all_status})
    df.to_excel('pedurma_list_batch6.xlsx',sheet_name='Esukhia Work', index=True)


def get_number_of_notes(text_id):
    list = (Path(f"./batch4_with_note_num.txt").read_text(encoding='utf-8')).splitlines()
    for pecha in list:
        infos = pecha.split(",")
        pecha_id = infos[0]
        if pecha_id == text_id:
            note_num = int(infos[1])
            return note_num

def create_csv(text_list):
    text_ids = []
    links = []
    all_status = []
    number_of_notes = []
    status = "Not Done"
    for text_id in text_list:
        # number = get_number_of_notes(text_id)
        link = f"https://openpecha.bdrc.io/pedurma/{text_id}"
        text_ids.append(text_id)
        links.append(link)
        all_status.append(status)
        # number_of_notes.append(number)
    add_to_excel(text_ids, links, all_status)


if __name__=="__main__":
    pecha_names = list(Path(f"./hfml/namsel_pedurma/").iterdir())
    pecha_names.sort()
    text_ids = []
    for pecha_name in pecha_names:
            pecha_name = pecha_name.name[:-4]
            map = re.match(r"([A-Z][0-9]+[a-z]?)\_(v[0-9]+)",pecha_name)
            text_id = map.group(1)
            vol_num = map.group(2)
            text_ids.append(text_id)
    # list = (Path(f"./list/batch4.txt").read_text(encoding='utf-8')).splitlines()

    # list_info = Path(f"./json_yaml/t_text_list.json").read_text(encoding='utf-8')
    # list_json = json.loads(list_info)
    # creat_json(list, list_json)
    text_ids.sort()
    create_csv(text_ids)