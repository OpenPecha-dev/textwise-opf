import os
import re
import logging
import json
from pathlib import Path
from git import Repo 
from pathlib import Path
from github import Github
from datetime import datetime
from openpecha.utils import load_yaml, dump_yaml
from openpecha.formatters import HFMLFormatter
from openpecha.serializers import HFMLSerializer
from openpecha.core.ids import get_pecha_id
import yaml
from uuid import uuid4

config = {
    "OP_ORG": "https://github.com/Openpecha"
}


logging.basicConfig(
    filename="nalada_text_special_cases.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
)


def update_real_opf(new_pecha_path, target_pecha_id):
    source_pecha_id = new_pecha_path.stem
    source_opf_path = Path(f"{new_pecha_path}/{source_pecha_id}.opf")
    target_opf_path = Path(f"./pecha_opf/namsel_pedurma/{target_pecha_id}/{target_pecha_id}.opf")
    source_base_path = Path(f"{source_opf_path}/base")
    source_layers_path =  Path(f"{source_opf_path}/layers")
    source_index_path =  Path(f"{source_opf_path}/index.yml")
    source_meta_path =  Path(f"{source_opf_path}/meta.yml")
    target_base_path =  Path(f"{target_opf_path}/base")
    target_layers_path =  Path(f"{target_opf_path}/layers")
    target_index_path =  Path(f"{target_opf_path}/index.yml")
    target_meta_path =  Path(f"{target_opf_path}/meta.yml")
    os.system(f"rm -rf {target_base_path}")
    os.system(f"rm -rf {target_layers_path}")
    os.system(f"rm -rf {target_index_path}")
    os.system(f"rm -rf {target_meta_path}")
    os.system(f"cp -R {source_base_path} {target_base_path}")
    os.system(f"cp -R {source_layers_path} {target_layers_path}")
    os.system(f"cp -R {source_index_path} {target_index_path}")
    os.system(f"cp -R {source_meta_path} {target_meta_path}")


def update_index(new_pecha_path, pecha_id, vol_num):
    index = load_yaml(Path(f"{new_pecha_path}/{pecha_id}.opf/index.yml"))
    annotations = index['annotations']
    for _, annotation in annotations.items():
        annotation['parts'] = {}
        annotation['span'][0]['vol'] = vol_num
    index_path = Path(f"{new_pecha_path}/{pecha_id}.opf/index.yml")
    dump_yaml(index, index_path)
 


def add_title_to_meta(real_pecha_id, title):
    meta_path = Path(f"./pecha_opf/namsel_pedurma/{real_pecha_id}/{real_pecha_id}.opf/meta.yml")
    meta = load_yaml(meta_path)
    volumes = meta["source_metadata"]['volumes']
    for _, vol_info in volumes.items():
        if vol_info["title"] == "":
            vol_info['title'] = title
    metadata_yml = yaml.safe_dump(meta,sort_keys=False, allow_unicode=True)
    meta_path.write_text(metadata_yml, encoding='utf-8')


def change_base_text_name(pecha_id, vol, pecha_opf_path):
    source = f"{pecha_opf_path}/{pecha_id}.opf/base/v001.txt"
    dest = f"{pecha_opf_path}/{pecha_id}.opf/base/v{vol:03}.txt"
    os.rename(source, dest)


def get_note_ref_id(img_num, tar_pagination):
    for uuid, pg_ann in tar_pagination['annotations'].items():
        if int(pg_ann['imgnum']) == img_num:
            return uuid
    return ''


def transfer_note_ref(tar_pagination, note_ref_img_num, img_num):
    for uuid, pg_ann in tar_pagination['annotations'].items():
        note_ref_id = get_note_ref_id(note_ref_img_num, tar_pagination)
        if int(pg_ann['imgnum'] )== img_num:
            tar_pagination['annotations'][uuid]['note_ref'] = note_ref_id
            return tar_pagination
    return tar_pagination


def parse_src_pg(pg_ann):
   return pg_ann['note_ref'], pg_ann['imgnum']


def update_note_ref(src_pagination, tar_pagination):
    for _, pg_ann in src_pagination['annotations'].items():
        if pg_ann.get('note_ref', ''):
            note_ref_id, img_num = parse_src_pg(pg_ann)
            note_ref_img_num = src_pagination['annotations'][note_ref_id]['imgnum']
            tar_pagination = transfer_note_ref(tar_pagination, note_ref_img_num, img_num)
    return tar_pagination


def transfer_text_note_ref(pecha_id, vol_num, new_pecha_path, real_pecha_id):
    # vol_num = (Path(f'./pecha_opf/namsel_pedurma/{real_pecha_id}/{real_pecha_id}.opf/layers/').iterdir())[0]
    text_pg_layer = load_yaml(Path(f'{new_pecha_path}/{pecha_id}.opf/layers/v{int(vol_num):03}/Pagination.yml'))
    src_pagination = load_yaml(Path(f'./pecha_opf/namsel_pedurma/{real_pecha_id}/{real_pecha_id}.opf/layers/v{int(vol_num):03}/Pagination.yml'))
    new_text_pg_layer = update_note_ref(src_pagination, text_pg_layer)
    pagination_path = Path(f"{new_pecha_path}/{pecha_id}.opf/layers/v{int(vol_num):03}/Pagination.yml")
    dump_yaml(new_text_pg_layer, pagination_path)
    


def change_vol_num(pecha_id, vol, pecha_opf_path):
    source = f"{pecha_opf_path}/{pecha_id}.opf/layers/v001"
    dest = f"{pecha_opf_path}/{pecha_id}.opf/layers/v{vol:03}"
    os.rename(source, dest)


def update_meta(P9_metadata, pecha_meta, pecha_opf_path, pecha_id, vol_num, title):
    source_metadata = {}
    id = pecha_id
    P9_volumes = P9_metadata['source_metadata']['volumes']
    for _, vol_info in P9_volumes.items():
        if vol_info['volume_number'] == vol_num:
            source_metadata['volumes'] = {
                f'{uuid4().hex}': {
                    'base_file': f"v{vol_num:03}.txt",
                    'image_group_id': vol_info["image_group_id"],
                    'title': title,
                    'total_pages': vol_info["total_pages"],
                    'volume_number': vol_info["volume_number"]     
                }
            }
            break
    metadata ={
        'id':id,
        'initial_creation_type': 'ocr',
        'source_metadata': source_metadata
    }
    metadata_yml = yaml.safe_dump(metadata,sort_keys=False, allow_unicode=True)
    Path(f"{pecha_opf_path}/{pecha_opf_path.stem}.opf/meta.yml").write_text(metadata_yml, encoding='utf-8')



def transfer_ref(vol_num, title, new_pecha_path, real_pecha_id):
    new_pecha_id = new_pecha_path.stem
    change_vol_num(new_pecha_id, int(vol_num[1:]), new_pecha_path)
    # transfer_text_note_ref(new_pecha_id, int(vol_num[1:]), new_pecha_path, real_pecha_id)
    change_base_text_name(new_pecha_id, int(vol_num[1:]), new_pecha_path)
    add_title_to_meta(real_pecha_id, title)
    pecha_meta_yml = Path(f"./new_opf/{new_pecha_id}/{new_pecha_id}.opf/meta.yml").read_text(encoding='utf-8')
    pecha_meta = yaml.safe_load(pecha_meta_yml)
    source_meta_yml =  Path(f"./opfs/new_meta.yml").read_text(encoding='utf-8')
    P9_metadata = yaml.safe_load(source_meta_yml)
    update_meta(P9_metadata, pecha_meta, new_pecha_path, real_pecha_id, int(vol_num[1:]), title)
    update_index(new_pecha_path, new_pecha_id, int(vol_num[1:]))

def notifier(msg):
    logging.info(msg)

def get_branch(repo, branch):
    if branch in repo.heads:
        return branch
    return "master"


def download_pecha(pecha_id, out_path=None, branch="master"):
    pecha_url = f"{config['OP_ORG']}/{pecha_id}.git"
    out_path = Path(out_path)
    out_path.mkdir(exist_ok=True, parents=True)
    pecha_path = out_path / pecha_id
    Repo.clone_from(pecha_url, str(pecha_path))
    repo = Repo(str(pecha_path))
    branch_to_pull = get_branch(repo, branch)
    repo.git.checkout(branch_to_pull)
    # print(f"{pecha_id} Downloaded ")
    return pecha_path        

def get_layers(opf_path):
    files = os.listdir(opf_path)
    if "pedyrma.yml" in files:
        layers = ['Pagination', 'Durchen', 'Peydurma']
    else:
        layers = ['Pagination', 'Durchen']
    return layers

def get_hfml_text(opf_path):
    layers = get_layers(opf_path)
    serializer = HFMLSerializer(opf_path, layers=layers)
    serializer.apply_layers()
    hfml_text = serializer.get_result()
    for vol_num, text in hfml_text.items():
        return vol_num, text

def serialise_the_opf(pecha_path):
    pecha_id = pecha_path.stem
    opf_path = Path(f"{pecha_path}/{pecha_id}.opf")
    vol_num, text = get_hfml_text(opf_path)
    return vol_num, text

def format_opf(hfml_name, output_path):
    Path(f"./namsel_pedurma/{hfml_name}").mkdir(parents=True, exist_ok=True)
    target_path = Path(f"./namsel_pedurma/{hfml_name}/")
    source_path = Path(f"./hfmls/namsel_pedurma/{hfml_name}.txt")
    os.system(f" cp -R {source_path} {target_path}")
    hfml_path = Path(f"./namsel_pedurma/{hfml_name}")
    pecha_id = get_pecha_id()
    formatter = HFMLFormatter(output_path=output_path)
    formatter.create_opf(hfml_path, pecha_id)
    return Path(output_path/pecha_id)

def check_derge(text_id, text_json, hfml_name):
    if text_id in text_json.keys():
        pecha_id = text_json[text_id]['namsel']
        title = text_json[text_id]['title']
        pecha_opf = Path(f"./pecha_opf/namsel_pedurma/")
        pecha_path = download_pecha(pecha_id, out_path=pecha_opf)
        output_path = (Path(f"./new_opf/"))
        new_opf_path  = format_opf(hfml_name, output_path)
        transfer_ref(vol_num, title, new_opf_path, pecha_path.stem)
        update_real_opf(new_opf_path, pecha_path.stem)
    # elif text_id in note_json.keys():
    #     pecha_id = note_json[text_id]['google']
    #     title = note_json[text_id]['title']
    #     pecha_opf = Path(f"./pecha_opf/namsel_pedurma/")
    #     pecha_path = download_pecha(pecha_id, out_path=pecha_opf)
        # output_path = (Path(f"./new_opf/"))
        # new_opf_path  = format_opf(hfml_name, output_path)
        # transfer_ref(vol_num, title, new_opf_path, pecha_path.stem)
        # update_real_opf(new_opf_path, pecha_path.stem)
    else:
        print(f"{text_id} is not present in the list")
        # return text_id
    # special_hfml_path = Path(f"./special_hfml/namsel_pedurma/{file}")
    
   


if __name__ == "__main__":
    hfml_names = ""
    t_json = Path(f"./t_text_list.json").read_text(encoding="utf-8")
    text_json = json.loads(t_json)
    # n_json = Path(f"./no_note_ref.json").read_text(encoding="utf-8")
    # note_json = json.loads(n_json)
    # text_list = (Path(f"./batch2_no_note_ref.txt").read_text(encoding='utf-8')).splitlines()
    hfmls = ["D4036_v073"]
    hfmls.sort()
    # done_list = ["D1307", "D2850"]
    for hfml_name in hfmls:
        # hfml_name = hfml_name.stem
        map = re.match(r"(D[0-9]+[a-z]?)\_(v[0-9]+)",hfml_name)
        text_id = map.group(1)
        vol_num = map.group(2)
        # if text_id in done_list:
        #     pass
        # else:
        check_derge(text_id, text_json, hfml_name)
        

    
    
    
    # Path(f"./not_made_into_opf_list.txt").write_text(hfml_names, encoding="utf-8")