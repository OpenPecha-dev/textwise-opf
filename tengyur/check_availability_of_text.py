from pathlib import Path
from openpecha.utils import load_yaml

def write_list(final_list):
    final_text = ""
    for text in final_list:
        final_text  += text + "\n"
    Path(f"./final_nalanda_list.txt").write_text(final_text, encoding='utf-8')


def check_the_list_in_namsel_index(text_list):
    available_list = []
    index_path = Path(f"./opfs/187ed94f85154ea5b1ac374a651e1770/187ed94f85154ea5b1ac374a651e1770.opf/index.yml")
    index = load_yaml(index_path)
    annotations = index["annotations"]
    for text_id in text_list:
        for _, info in annotations.items():
            if text_id == info["work_id"]:
                available_list.append(text_id)
                break
    return available_list

def check_the_list_in_derge_index(text_list):
    available_list = []
    index_path = Path(f"./opfs/12d32eb31c1a4cc59741cda99ebc7211/12d32eb31c1a4cc59741cda99ebc7211.opf/index.yml")
    index = load_yaml(index_path)
    annotations = index["annotations"]
    for text_id in text_list:
        for _, info in annotations.items():
            if text_id == info["work_id"]:
                available_list.append(text_id)
                break
    return available_list


if __name__ == "__main__":
    text_list = Path(f"./tengyur/nalanda_text_list.txt").read_text(encoding='utf-8')
    text_list = text_list.splitlines()
    # derge_list = check_the_list_in_derge_index(text_list)
    final_list = check_the_list_in_namsel_index(text_list)
    write_list(final_list)
    