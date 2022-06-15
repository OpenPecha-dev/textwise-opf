from pathlib import Path
import json
from pandas import DataFrame
from openpecha.utils import load_yaml

def get_title(text_id, outline_info):
    for _, outline_info in outline_info.items():
            if outline_info['rkts_id'] == text_id:
                title = outline_info['pedurma_title']
                return title

def creat_json(outlines, list_json, namsel_info):
    curr_info = {}
    final_info = {}
    list = list_json.keys()
    for id in list:
        title = get_title(id, outlines)
        google = list_json[id]['google']
        namsel = namsel_info[id]['pecha_id']
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
    df.to_excel('no_note_ref_batch3.xlsx',sheet_name='Esukhia Work', index=True)


def create_csv(list_json):
    text_ids = []
    links = []
    all_status = []
    status = "Not Done"
    for text_id, _ in list_json.items():
        link = f"https://openpecha.bdrc.io/pedurma/{text_id}/notes"
        text_ids.append(text_id)
        links.append(link)
        all_status.append(status)
    add_to_excel(text_ids, links, all_status)


if __name__=="__main__":
    # list = (Path(f"./no_note_ref_list.txt").read_text(encoding='utf-8')).splitlines()
    outlines = load_yaml(Path(f"./pedurma_outline.yml"))
    namsel_info = load_yaml(Path(f"./namsel_pecha_info.yml"))
    list_info = Path(f"./output.json").read_text(encoding='utf-8')
    list_json = json.loads(list_info)
    creat_json(outlines,list_json, namsel_info)
    # create_csv(list_json)
