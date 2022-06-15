import yaml
import os
import re
from uuid import uuid4
from pathlib import Path

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
        return str(img_num)

def get_note_ref_id(page_index, tar_pagination):
    img_num = get_img_num(page_index)
    for uuid, pg_ann in tar_pagination['annotations'].items():
        if pg_ann['imgnum'] == img_num:
            return uuid
    return ''

def transfer_note_ref(tar_pagination, note_ref_idx, pg_idx):
    img_num = get_img_num(pg_idx)
    for uuid, pg_ann in tar_pagination['annotations'].items():
        note_ref_id = get_note_ref_id(note_ref_idx, tar_pagination)
        if pg_ann['imgnum'] == img_num:
            tar_pagination['annotations'][uuid]['note_ref'] = note_ref_id
            return tar_pagination
    return tar_pagination

def update_note_ref(src_pagination, tar_pagination):
    for uuid, pg_ann in src_pagination['annotations'].items():
        if pg_ann.get('note_ref', ''):
            note_ref_id, pg_idx = parse_src_pg(pg_ann)
            note_ref_idx = src_pagination['annotations'][note_ref_id]['page_index']
            tar_pagination = transfer_note_ref(tar_pagination, note_ref_idx, pg_idx)
    return tar_pagination

def transfer_text_note_ref(vol_num, layer_path):
    tar_pagination = from_yaml(Path(f'{layer_path}/Pagination.yml'))
    src_pagination = from_yaml(Path(f'./opfs/P000792/P000792.opf/layers/{vol_num}/Pagination.yml'))
    new_tar_pagination = update_note_ref(src_pagination, tar_pagination)
    new_tar_pagination = to_yaml(new_tar_pagination)
    return new_tar_pagination

def transfer_ref(pecha_id, opf_path):
    layers_paths = list(Path(f'{opf_path}/layers').iterdir())
    layers_paths.sort()
    for layer_path in layers_paths:
        vol_num = layer_path.stem
        new_text_pg_layer = transfer_text_note_ref(vol_num, layer_path)
        Path(f"./tengyur/note/{pecha_id}/{pecha_id}.opf/layers/{vol_num}/Pagination.yml").write_text(new_text_pg_layer, encoding='utf-8')
        print(f"note tranfered on {vol_num}")

    
if __name__=='__main__':
    derge_google_id = '12d32eb31c1a4cc59741cda99ebc7211'
    namsel_id = '187ed94f85154ea5b1ac374a651e1770'
    derge_google_opf_path = f'./tengyur/note/{derge_google_id}/{derge_google_id}.opf'
    namsel_opf_path = f'./tengyur/note/{namsel_id}/{namsel_id}.opf'
    transfer_ref(derge_google_id, derge_google_opf_path)
    transfer_ref(namsel_id, namsel_opf_path)