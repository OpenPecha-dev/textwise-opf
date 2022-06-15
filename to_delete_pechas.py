from pathlib import Path
import json
import time
from github import Github
import logging

logging.basicConfig(
    filename="pecha_delted.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
)

def notifier(msg):
    logging.info(msg)

def _get_openpecha_org(token, org_name):
    """OpenPecha github org singleton."""
    g = Github(token)
    org = g.get_organization(org_name)
    return org

def delete_repo(repo_name, org_name, token):
    org = _get_openpecha_org(org_name, token)
    try:
        repo = org.get_repo(repo_name)
    except:
        notifier(f"{pecha_id} is not present in github")
        print(f"{repo_name} is not present in github")
        return
    repo.delete()

def clean_repo(pecha_id, token):
    org_name = 'Openpecha'
    delete_repo(pecha_id, token, org_name)
    time.sleep(2)
    notifier(f"{pecha_id} opf is delete")
    print(f'{pecha_id} opf is delete')

if __name__=='__main__':
    token = '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'
    pecha_list = Path(f"./pecha_delete_list.txt").read_text(encoding='utf-8').splitlines()
    for pecha_id in pecha_list:
        clean_repo(pecha_id, token)

