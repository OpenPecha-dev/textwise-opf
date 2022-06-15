import yaml
import os
import re
from uuid import uuid4
from pathlib import Path
from openpecha.utils import dump_yaml, load_yaml

def from_yaml(yml_path):
    return yaml.load(yml_path.read_text(encoding="utf-8"), Loader=yaml.CLoader)

def to_yaml(dict_):
    return yaml.dump(dict_, sort_keys=False, allow_unicode=True, Dumper=yaml.CDumper)

def parse_src_pg(pg_ann):
   return pg_ann['note_ref'], pg_ann['page_index']


def  get_img_num(page_index):
    if re.search(r'\d+[a-z]{1}', page_index):
        match = re.match(r'(\d+)([a-z]{1})', page_index)
        num = match.group(1)
        side = match.group(2)
        if side == 'a':
            img_num = int(num)*2 - 1
        elif side == 'b':
             img_num = int(num)*2
        return img_num

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

def update_note_ref(src_pagination, tar_pagination):
    for _, pg_ann in src_pagination['annotations'].items():
        if pg_ann.get('note_ref', ''):
            note_ref_id, page_indx = parse_src_pg(pg_ann)
            note_ref_pg_idx= src_pagination['annotations'][note_ref_id]['page_index']
            note_ref_img_num = get_img_num(note_ref_pg_idx)
            img_num = get_img_num(page_indx)
            tar_pagination = transfer_note_ref(tar_pagination, note_ref_img_num, img_num)
    return tar_pagination

# def transfer_text_note_ref(pecha_id, vol_num, pecha_opf_path):
#     text_pg_layer = from_yaml(Path(f'{pecha_opf_path}/{pecha_id}/{pecha_id}.opf/layers/v{int(vol_num):03}/Pagination.yml'))
#     src_pagination = from_yaml(Path(f'./opfs/P000792/P000792.opf/layers/v{int(vol_num):03}/Pagination.yml'))
#     new_text_pg_layer = update_note_ref(src_pagination, text_pg_layer)
#     new_text_pg_layer = to_yaml(new_text_pg_layer)
#     return new_text_pg_layer

def change_vol_num(pecha_id, vol, pecha_opf_path):
    source = f"{pecha_opf_path}/{pecha_id}/{pecha_id}.opf/layers/v001"
    dest = f"{pecha_opf_path}/{pecha_id}/{pecha_id}.opf/layers/v{vol:03}"
    os.rename(source, dest)

def change_base_text_name(pecha_id, vol, pecha_opf_path):
    source = f"{pecha_opf_path}/{pecha_id}/{pecha_id}.opf/base/v001.txt"
    dest = f"{pecha_opf_path}/{pecha_id}/{pecha_id}.opf/base/v{vol:03}.txt"
    os.rename(source, dest)

def get_note_ref_id_last(ann):
    for uuid, ann_info in ann.items():
        highest_imgnum = 0
        temp_imgnum = ann_info['imgnum']
        if temp_imgnum > highest_imgnum:
            highest_imgnum = temp_imgnum
            note_ref_id = uuid
    return note_ref_id
    

def add_note_ref(text_pg_layer):
    new_ann = {}
    curr_ann = {}
    ann = text_pg_layer['annotations']
    note_ref_id = get_note_ref_id_last(ann)
    for uuid, ann_info in ann.items():
        if uuid != note_ref_id:
            curr_ann[uuid] = {
                "imgnum": ann_info['imgnum'],
                "reference": ann_info['reference'],
                "span":{
                   "start": ann_info['span']['start'],
                    "end": ann_info['span']['end']
                },
               "note_ref": note_ref_id
            }
            new_ann.update(curr_ann)
            curr_ann = {}
        else:
            curr_ann[uuid] = {
                "imgnum": ann_info['imgnum'],
                "reference": ann_info['reference'],
                "span":{
                   "start": ann_info['span']['start'],
                    "end": ann_info['span']['end']
                }
            }
            new_ann.update(curr_ann)
            curr_ann = {}
    text_pg_layer['annotations'] = new_ann
    return text_pg_layer


def transfer_text_note_ref(pecha_id, vol_num, pecha_opf_path):
    text_pg_layer = load_yaml(Path(f'{pecha_opf_path}/{pecha_id}/{pecha_id}.opf/layers/v{int(vol_num):03}/Pagination.yml'))
    new_pagination_layer = add_note_ref(text_pg_layer)
    # src_pagination = load_yaml(Path(f'./pecha/{real_pecha_id}/{real_pecha_id}.opf/layers/v{int(vol_num):03}/Pagination.yml'))
    # new_text_pg_layer = update_note_ref(src_pagination, text_pg_layer)
    pagination_path = Path(f"{pecha_opf_path}/{pecha_id}/{pecha_id}.opf/layers/v{int(vol_num):03}/Pagination.yml")
    dump_yaml(new_pagination_layer, pagination_path)

def transfer_ref(text_id, file_infos, vol_info, pecha_opf_path, pedurma_outline):
    title = ""
    for _, outline_info in pedurma_outline.items():
            if outline_info['rkts_id'] == text_id:
                title = outline_info['text_title']
                break
    pecha_id = file_infos[text_id]['uid']
    vol_num = vol_info[text_id]['vol'][1:]
    change_vol_num(pecha_id, int(vol_num), pecha_opf_path)
    transfer_text_note_ref(pecha_id, vol_num, pecha_opf_path)
    # new_text_pg_layer = transfer_text_note_ref(pecha_id, vol_num, pecha_opf_path)
    # Path(f"{pecha_opf_path}/{pecha_id}/{pecha_id}.opf/layers/v{int(vol_num):03}/Pagination.yml").write_text(new_text_pg_layer, encoding='utf-8')
    # print(f'done with {text_id}')
    change_base_text_name(pecha_id, int(vol_num), pecha_opf_path)
    pecha_meta_yml = Path(f"{pecha_opf_path}/{pecha_id}/{pecha_id}.opf/meta.yml").read_text(encoding='utf-8')
    pecha_meta = yaml.safe_load(pecha_meta_yml)
    source_meta_yml =  Path(f"./opfs/new_meta.yml").read_text(encoding='utf-8')
    P9_metadata = yaml.safe_load(source_meta_yml)
    update_meta(P9_metadata, pecha_meta, pecha_opf_path, pecha_id, int(vol_num), title)
    update_index(pecha_opf_path, pecha_id, int(vol_num))
   
def update_meta(P9_metadata, pecha_meta, pecha_opf_path, pecha_id, vol_num, title):
    source_metadata = {}
    id = pecha_meta['id'][7:]
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
    Path(f"{pecha_opf_path}/{pecha_id}/{pecha_id}.opf/meta.yml").write_text(metadata_yml, encoding='utf-8')


def update_index(pecha_opf_path, pecha_id, vol_num):
    index = from_yaml(Path(f"{pecha_opf_path}/{pecha_id}/{pecha_id}.opf/index.yml"))
    annotations = index['annotations']
    for _, annotation in annotations.items():
        annotation['parts'] = {}
        annotation['span'][0]['vol'] = vol_num
    index_yml = to_yaml(index)
    Path(f"{pecha_opf_path}/{pecha_id}/{pecha_id}.opf/index.yml").write_text(index_yml, encoding='utf-8')
