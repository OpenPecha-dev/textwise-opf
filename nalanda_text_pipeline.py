import os
import yaml
import re
import uuid
import json
from pathlib import Path
from openpecha import github_utils
from note_postprocessing import post_process
from transfer_note_ref import transfer_ref
from correct_derge_google import correct_google_text
from openpecha.formatters import HFMLFormatter
from openpecha.core.ids import get_pecha_id
from openpecha.utils import load_yaml


def create_openpecha(post_process_path, pecha_name, pecha_opf_path, pecha_id):
    print(f'{pecha_name} is {pecha_id}')
    post_process_text = f"{post_process_path}/{pecha_name}"
    formatter = HFMLFormatter(output_path=pecha_opf_path)
    formatter.create_opf(post_process_text, pecha_id)

def write_vol_num_and_pecha_id(pecha_names):
    curr_file = {}
    file_info = {}
    yml_path = Path(f"./text_id_and_vol_num.yml")
    if os.path.isfile(yml_path) == True:
        file_info = read_yaml_files(None, "text_id_and_vol_num")
    for pecha_name in pecha_names:
        pecha_name = pecha_name.name[:-4]
        map = re.match(r"([A-Z][0-9]+[a-z]?)\_(v[0-9]+)", pecha_name)
        text_id = map.group(1)
        vol_num = map.group(2)
        curr_file[text_id] ={
            'vol': vol_num
            }
        file_info.update(curr_file)
        curr_file = {}
    file_info_yml = yaml.safe_dump(file_info, default_flow_style=False, sort_keys=True, allow_unicode=True)
    yml_path.write_text(file_info_yml, encoding='utf-8')


def replace_shad_in_text(hfml_path, pecha_name, after_clean_path, vol_num):
    text = Path(f"{hfml_path}/{pecha_name}.txt").read_text(encoding='utf-8')
    vol_num = vol_num[1:]
    text = text.replace("-།", "༑")
    text = text.replace(f"{int(vol_num)}བྱེད", f"{vol_num}-")
    new_text = text.replace("{}", "")
    Path(f"{after_clean_path}/{pecha_name}.txt").write_text(new_text, encoding='utf-8') 
    

def read_yaml_files(pedurma_type, file_type):
    if pedurma_type == None:
        file_info_yml = Path(f"./{file_type}.yml").read_text(encoding='utf-8')
    else:
        file_info_yml = Path(f"./{pedurma_type}_{file_type}.yml").read_text(encoding='utf-8')
    file_infos = yaml.safe_load(file_info_yml)
    return file_infos


def post_process_and_create_opf(pedurma_type, pecha_name, pecha_opf_path, after_clean_path, post_process_path):
    file_info = {}
    curr_file = {}
    _type = pedurma_type[:-8]
    yml_path = Path(f"./{pedurma_type}_text_id_and_uid.yml")
    if os.path.isfile(yml_path) == True:
        file_info = read_yaml_files(pedurma_type, "text_id_and_uid")
    post_process(after_clean_path, pecha_name, _type, post_process_path)
    pecha_id = get_pecha_id()
    create_openpecha(post_process_path, pecha_name, pecha_opf_path, pecha_id)
    map = re.match(r"([A-Z][0-9]+[a-z]?)\_(v[0-9]+)",pecha_name)
    text_id = map.group(1)
    curr_file[text_id] ={'uid': pecha_id}
    file_info.update(curr_file)
    curr_file = {}
    file_info_yml = yaml.safe_dump(file_info, default_flow_style=False, sort_keys=True, allow_unicode=True)
    yml_path.write_text(file_info_yml, encoding='utf-8')

def get_pecha_names():
    namsel_path = Path(f"./hfml/namsel_pedurma")
    derge_google_path = Path(f"./hfml/derge_google_pedurma")
    pecha_names = []
    namsel_names = []
    derge_names = []
    for file in os.listdir(namsel_path):
        if file.endswith(".txt"):
            file_name = file[:-4]
            namsel_names.append(file_name)
    for file in os.listdir(derge_google_path):
        if file.endswith(".txt"):
            file_name = file[:-4]
            derge_names.append(file_name)
    for namsel_name in namsel_names:
        if namsel_name in derge_names:
            pecha_names.append(namsel_name)
    print(pecha_names)
    return pecha_names

def clean_google(hfml_path, pecha_name, after_clean_path):
    text = Path(f"{hfml_path}/{pecha_name}.txt").read_text(encoding='utf-8')
    text = re.sub(r"\<p.+\>", "", text)
    new_text = text.replace(r"{}", "")
    Path(f"{after_clean_path}/{pecha_name}.txt").write_text(new_text, encoding='utf-8') 

if __name__ =="__main__":
    pedurma_types = ["namsel_pedurma", "derge_google_pedurma"]
    # pecha_names = get_pecha_names()
    pecha_names = list(Path(f"./hfml/namsel_pedurma/").iterdir())
    # text_list = (Path(f"./batch2_no_note_ref.txt").read_text(encoding='utf-8')).splitlines()
    pecha_names.sort()
    pedurma_outline = read_yaml_files(None, "pedurma_outline")
    write_vol_num_and_pecha_id(pecha_names)
    for pedurma_type in pedurma_types:
        post_process_path = f"./post_process/{pedurma_type}"
        hfml_path = f"./hfml/{pedurma_type}"
        pecha_opf_path = f"./pecha_opf/{pedurma_type}"
        after_clean_path = f"./after_clean/{pedurma_type}"
        for pecha_name in pecha_names:
            pecha_name = pecha_name.name[:-4]
            map = re.match(r"([A-Z][0-9]+[a-z]?)\_(v[0-9]+)",pecha_name)
            text_id = map.group(1)
            vol_num = map.group(2)
            if pedurma_type == "namsel_pedurma":
                replace_shad_in_text(hfml_path, pecha_name, after_clean_path, vol_num)
            else:
                clean_google(hfml_path, pecha_name, after_clean_path)
            post_process_and_create_opf(pedurma_type, pecha_name, pecha_opf_path, after_clean_path, post_process_path)
            file_infos = read_yaml_files(pedurma_type, "text_id_and_uid")
            vol_info = read_yaml_files(None, "text_id_and_vol_num")
            transfer_ref(text_id, file_infos, vol_info, pecha_opf_path, pedurma_outline)
            pecha_id = file_infos[text_id]['uid']
            pecha_path = Path(f"./pecha_opf/{pedurma_type}/{pecha_id}")
            print(f'{text_id} is correctly done')





# AIzaSyCrjjXDCwxEaAb74VRmmJrpk-CqlNSaQXM