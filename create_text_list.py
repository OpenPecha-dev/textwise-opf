from pathlib import Path
from openpecha.utils import load_yaml
import json

def get_title(text_id, outline_info):
    for _, outline_info in outline_info.items():
            if outline_info['rkts_id'] == text_id:
                title = outline_info['text_title']
                return title

def create_editable_text_list(namsel_info, derge_google_info, outline_info):
    curr_final_info = {}
    final_info = {}
    curr_note_ref_info = {}
    note_ref_info = {}
    for text_id, namsel_text_info in namsel_info.items():
        title = get_title(text_id, outline_info)
        namsel_pecha_id = namsel_text_info["pecha_id"]
        if namsel_text_info["note_ref"] == "value present":
            namsel = True
        else:
            namsel = False
        derge_text_info = derge_google_info[text_id]
        derge_pecha_id = derge_text_info["pecha_id"]
        if derge_text_info["note_ref"] == "value present":
            derge_google = True
        else:
            derge_google = False
        if derge_google and namsel:
            curr_final_info[text_id]={
                'google': derge_pecha_id,
                'namsel': namsel_pecha_id,
                'title': title
            }
            final_info.update(curr_final_info)
            curr_final_info = {}
        else:
            curr_note_ref_info[text_id]={
                'google': derge_pecha_id,
                'namsel': namsel_pecha_id,
                'title': title
            }
            note_ref_info.update(curr_note_ref_info)
            curr_note_ref_info = {}

    final_info_yml = json.dumps(final_info, sort_keys=True, ensure_ascii=False)
    # note_ref_info_yml = json.dumps(note_ref_info, sort_keys=True, ensure_ascii=False)
    Path(f"./output.json").write_text(final_info_yml, encoding='utf-8')
    # Path(f"./no_note_ref_batch2.json").write_text(note_ref_info_yml, encoding='utf-8')


def read_yaml_files(file_name):
    file_path = Path(f"./{file_name}.yml")
    file_infos = load_yaml(file_path)
    return file_infos

def create_editable():
    list_info = Path(f"./dict/t_text_list.json").read_text(encoding='utf-8')
    list_json = json.loads(list_info)
    final_list = json.dumps(list_json, sort_keys=True, ensure_ascii=False)
    Path(f"./t_text_list.json").write_text(final_list, encoding='utf-8')


def create_text_list(note_ref_json,text_json):
    curr_final_info = {}
    final_info = {}
    curr_note_ref_info = {}
    note_ref_info = {}
    text_ids = (Path(f"./batch2_no_note_ref.txt").read_text(encoding='utf-8')).splitlines()
    for text_id in text_ids:
        if text_id in note_ref_json.keys():
            print(f"present")
        else:
            if text_id in text_json.keys():
                curr_final_info[text_id]={
                    'google': text_json[text_id]['google'],
                    'namsel': text_json[text_id]['namsel'],
                    'title': text_json[text_id]['title']
                }
                final_info.update(curr_final_info)
                curr_final_info = {}
            else:
                print(f"{text_id} not in list")

    final_info_yml = json.dumps(final_info, sort_keys=True, ensure_ascii=False)
    note_ref_info_yml = json.dumps(note_ref_json, sort_keys=True, ensure_ascii=False)
    # Path(f"./no_note_ref_batch2.json").write_text(final_info_yml, encoding='utf-8')
    Path(f"./batch2_no_note_ref.json").write_text(note_ref_info_yml, encoding='utf-8')

if __name__=="__main__":
    # derge_google_info = read_yaml_files("derge_google_pedurma_info")
    # namsel_info = read_yaml_files("namsel_pedurma_info")
    # outline_info = read_yaml_files("pedurma_outline")
    # create_editable_text_list(namsel_info, derge_google_info, outline_info)
    create_editable()
    # text_json = json.loads(Path(f"./t_text_list.json").read_text(encoding='utf-8'))
    # note_ref_json = json.loads(Path(f"./no_note_ref.json").read_text(encoding='utf-8'))
    # create_text_list(note_ref_json)