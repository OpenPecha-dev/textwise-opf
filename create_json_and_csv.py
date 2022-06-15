import json
import yaml

from pathlib import Path


def read_yaml_files(pedurma_type, file_type):
    if pedurma_type == None:
        file_info_yml = Path(f"./{file_type}.yml").read_text(encoding='utf-8')
    else:
        file_info_yml = Path(f"./{pedurma_type}_{file_type}.yml").read_text(encoding='utf-8')
    file_infos = yaml.safe_load(file_info_yml)
    return file_infos


def create_json():
    curr_file = {}
    file_info = {}
    namsel_info = read_yaml_files("namsel_pedurma_text_id", "and_uid")
    derge_google_pedurma_info = read_yaml_files("derge_google_pedurma_text_id", "and_uid")
    pedurma_outline_info = read_yaml_files(None, "pedurma_outline")
    for text_id, _ in namsel_info.items():
        namsel_uid = namsel_info[text_id]['uid'],
        derge_google_uid = derge_google_pedurma_info[text_id]['uid']
        for id_, outline_info in pedurma_outline_info.items():
            if outline_info['rkts_id'] == text_id:
                title = outline_info['text_title']
                break
        curr_file[text_id] ={
            'title': title,
            'namsel': namsel_uid[0],
            'google': derge_google_uid,
            }
        file_info.update(curr_file)
        curr_file = {}
        title = ""
    file_info_yml = json.dumps(file_info, sort_keys=True, ensure_ascii=False)
    Path(f"./output.json").write_text(file_info_yml, encoding='utf-8')

def add_to_csv(pecha_id, title, type, text_id):
    row = f"[{pecha_id}](https://github.com/OpenPecha/{pecha_id}),{title},{type},{text_id}\n"
    with open(f"textwise_opf.csv", "a", encoding='utf-8') as csvfile:
        csvfile.write(row)


def create_csv():
    json_dict = open('./output.json')
    dict = json.load(json_dict)

    for text_id, info in dict.items():
        namsel_id = info['namsel']
        google_id = info['google']
        title = info['title']
        add_to_csv(google_id, title, 'google', text_id)
        add_to_csv(namsel_id, title, 'namsel', text_id)
        
if __name__=='__main__':
    create_json()
    # create_csv()