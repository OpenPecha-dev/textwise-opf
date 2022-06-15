import re
from pathlib import Path

from openpecha.serializers import HFMLSerializer
from openpecha.utils import load_yaml

def get_hfml_text(opf_path):
    serializer = HFMLSerializer(opf_path, layers=['Pagination', 'Durchen'])
    serializer.apply_layers()
    hfml_text = serializer.get_result()
    return hfml_text

def save_volwise(hfml_text, output_path):
    for vol_num, hfml in hfml_text.items():
        Path(f'{output_path}/{vol_num}.txt').write_text(hfml, encoding="utf-8")
        print(f'{vol_num} done')

def create_volwise(opf_path, type):
    output_path = f"./tengyur/serialized/{type}"
    text_hfml = get_hfml_text(opf_path)
    save_volwise(text_hfml, output_path)

if __name__ == "__main__":
    derge_id = "12d32eb31c1a4cc59741cda99ebc7211"
    namsel_id = "187ed94f85154ea5b1ac374a651e1770"
    derge_path = Path(f'./opfs/{derge_id}/{derge_id}.opf/')
    namsel_path = Path(f'./tengyur/new_opf/{namsel_id}/{namsel_id}.opf/')
    # create_volwise(derge_path, "derge_google")
    create_volwise(namsel_path, "namsel")
    
   