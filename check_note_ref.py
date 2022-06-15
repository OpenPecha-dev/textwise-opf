from pathlib import Path
import os
from openpecha.utils import load_yaml, dump_yaml

def check_note_ref(opf_path, vol_num):
    pagination_path = Path(f"{opf_path}/layers/{vol_num}/Pagination.yml")
    if os.path.isfile(pagination_path):
        durchen = load_yaml(pagination_path)
        annotations =  durchen["annotations"]
        for _, ann_info in annotations.items():
            if "note_ref" in ann_info.keys():
                if ann_info["note_ref"] != "":
                    return "value present"
                else:
                    return "No value but key present"
            return "No note_ref"

def check_durchen(opf_path, vol_num):
    durchen_path = Path(f"{opf_path}/layers/{vol_num}/Durchen.yml")
    if os.path.isfile(durchen_path):
        durchen = load_yaml(durchen_path)
        if durchen["annotations"]:
            return True
        else:
            return False
    else:
        return False

def get_text_id_and_vol_num(opf_path):
    index_path = Path(f"{opf_path}/index.yml")
    index = load_yaml(index_path)
    annotations = index["annotations"]
    if annotations:
        for _, info in annotations.items():
            text_id = info["work_id"]
            vol_num = info["span"][0]["vol"]
            return text_id, vol_num
    else:
        return None, None

def get_index_start(opf_path):
    index = load_yaml(Path(f"{opf_path}/index.yml"))
    ann = index['annotations']
    for _, ann_info in ann.items():
        start = ann_info['span'][0]['start']
    return start
        
def check_opfs(pecha_ids, pecha_path, pedurma_type):
    curr_info = {}
    info = {}
    for pecha_id in pecha_ids:
        opf_path = Path(f"{pecha_path}/{pecha_id}/{pecha_id}.opf")
        text_id, vol_num = get_text_id_and_vol_num(opf_path)
        if text_id:
            vol_num = f"v{vol_num:03}"
            durchen_check = check_durchen(opf_path, vol_num)
            note_ref_check = check_note_ref(opf_path, vol_num)
            start = get_index_start(opf_path)
            curr_info[text_id]= {
                    "pecha_id": pecha_id,
                    "durchen": durchen_check,
                    "note_ref": note_ref_check,
                    "vol_num": vol_num,
                    "index_start": start
            }
            info.update(curr_info)
            curr_info = {}
    info_path = Path(f"./{pedurma_type}_info.yml")
    dump_yaml(info, info_path)
    
if __name__=="__main__":
    pedurma_types = ["namsel_pedurma","derge_google_pedurma"]
    for pedurma_type in pedurma_types:
        pecha_path = Path(f"./pecha_opf/{pedurma_type}")
        pecha_ids = os.listdir(pecha_path)
        check_opfs(pecha_ids, pecha_path, pedurma_type)