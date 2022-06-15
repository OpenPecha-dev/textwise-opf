from pathlib import Path
from turtle import down
from git import Repo
import json
import os

config = {
    "OP_ORG": "https://github.com/Openpecha"
}


def update_real_opf(source_pecha_path, target_pecha_path):
    source_pecha_id = source_pecha_path.stem
    target_pecha_id = target_pecha_path.stem
    source_opf_path = Path(f"{source_pecha_path}/{source_pecha_id}.opf")
    target_opf_path = Path(f"{target_pecha_path}/{target_pecha_id}.opf")
    source_base_path = Path(f"{source_opf_path}/base")
    source_layers_path =  Path(f"{source_opf_path}/layers")
    source_index_path =  Path(f"{source_opf_path}/index.yml")
    target_base_path =  Path(f"{target_opf_path}/base")
    target_layers_path =  Path(f"{target_opf_path}/layers")
    target_index_path =  Path(f"{target_opf_path}/index.yml")
    os.system(f"rm -rf {target_base_path}")
    os.system(f"rm -rf {target_layers_path}")
    os.system(f"rm -rf {target_index_path}")
    os.system(f"cp -R {source_base_path} {target_base_path}")
    os.system(f"cp -R {source_layers_path} {target_layers_path}")
    os.system(f"cp -R {source_index_path} {target_index_path}")

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
    print(f"{pecha_id} Downloaded ")
    return pecha_path

if __name__=="__main__":
    list_json = json.loads(Path(f"./output.json").read_text(encoding='utf-8'))
    old_path = Path(f"./pecha_opf/")
    for id, info in list_json.items():
        google_id = info['google']
        namsel_id = info['namsel']
        target_google_path = Path(f"./original/derge_google_pedurma/")
        target_namsel_path = Path(f"./original/namsel_pedurma/")
        target_google_path = download_pecha(google_id, target_google_path)
        target_namsel_path = download_pecha(namsel_id, target_namsel_path)
        source_google_path = Path(old_path/f"derge_google_pedurma/{google_id}")
        source_namsel_path = Path(old_path/f"namsel_pedurma/{namsel_id}")
        update_real_opf(source_google_path, target_google_path)
        update_real_opf(source_namsel_path, target_namsel_path)
        