from pathlib import Path
from openpecha.formatters import HFMLFormatter

def make_opf(output_path, pecha_id, hfml_path):
    formatter = HFMLFormatter(output_path)
    formatter.create_opf(hfml_path, pecha_id)


if __name__=='__main__':
    derge_google_id = '12d32eb31c1a4cc59741cda99ebc7211'
    namsel_id = '187ed94f85154ea5b1ac374a651e1770'
    derge_google_path = Path(f'./tengyur/serialized/derge_google/')
    namsel_path = Path(f'./tengyur/serialized/namsel/')
    output_path = Path(f"./tengyur/new_opf/")
    make_opf(output_path, derge_google_id, derge_google_path)
    # make_opf(output_path, namsel_id, namsel_path)