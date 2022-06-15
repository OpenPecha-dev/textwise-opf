from pathlib import Path
import yaml

def read_yaml_files(file_path):
    file_info_yml = Path(f"./{file_path}").read_text(encoding='utf-8')
    file_infos = yaml.safe_load(file_info_yml)
    return file_infos

def get_text_id(pecha_path):
    pecha_id = pecha_path.stem
    index_path = Path(f'{pecha_path}/{pecha_id}.opf/index.yml')
    index = read_yaml_files(index_path)
    index_ann = index['annotations']
    for _, ann_info in index_ann.items():
        text_id = ann_info['work_id']
        return text_id




if __name__=='__main__':
    curr_info = {}
    file_info = {}
    pecha_paths = list(Path(f'./pecha_opf/namsel_pedurma').iterdir())
    for pecha_path in pecha_paths:
        pecha_path = Path(pecha_path)
        text_id = get_text_id(pecha_path)
        pecha_id = pecha_path.stem
        curr_info[text_id] ={'uid': pecha_id}
        file_info.update(curr_info)
        curr_info = {}
    yml_path = Path('./namsel_and_uid.yml')
    file_info_yml = yaml.safe_dump(file_info, default_flow_style=False, sort_keys=True, allow_unicode=True)
    yml_path.write_text(file_info_yml, encoding='utf-8')