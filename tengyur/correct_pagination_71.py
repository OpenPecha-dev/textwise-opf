from pathlib import Path
import yaml
import re

def from_yaml(yml_path):
    return yaml.load(yml_path.read_text(encoding="utf-8"), Loader=yaml.CLoader)

def to_yaml(dict_):
    return yaml.dump(dict_, sort_keys=False, allow_unicode=True, Dumper=yaml.CDumper)

def get_page_index(pg_num):
    pg_index = ""
    if pg_num % 2 == 0:
        pg_index = f"{int(pg_num/2)}b"
    else:
        pg_index = f"{int(pg_num/2+1)}a"
    return pg_index
    
def correct_71(pagination):
    num = 0
    pagination_ann = pagination['annotations']
    for num, (_, pg_ann) in enumerate(pagination_ann.items(), 1):
        new_pg_in = get_page_index(num)
        pg_ann['page_index'] = new_pg_in
    return pagination


if __name__=='__main__':
    pecha_id = "12d32eb31c1a4cc59741cda99ebc7211"
    opf_path = Path(f'./tengyur/{pecha_id}/{pecha_id}.opf')
    layers_path = list(Path(f'{opf_path}/layers').iterdir())
    layers_path.sort()
    for layer_path in layers_path:
        pagination = from_yaml(Path(f'{layer_path}/Pagination.yml'))
        new_pagination = correct_71(pagination)
        pagination_yml = to_yaml(new_pagination)
        Path(f'{layer_path}/Pagination.yml').write_text(pagination_yml, encoding='utf-8')