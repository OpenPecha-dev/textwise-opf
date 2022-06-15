from pathlib import Path
from openpecha.formatters import HFMLFormatter


def create_openpecha(text_path, output_path, pecha_id):
    formatter = HFMLFormatter(output_path=output_path)
    formatter.create_opf(text_path, pecha_id)


if __name__ == '__main__':
    derge_google_id = '12d32eb31c1a4cc59741cda99ebc7211'
    namsel_id = '187ed94f85154ea5b1ac374a651e1770'
    output_path = Path('./tengyur/new_opf')
    derge_google_path = Path('./tengyur/updated_durchen/derge_google')
    namsel_path = Path('./tengyur/updated_durchen/namsel')
    create_openpecha(derge_google_path,output_path, derge_google_id)
    print('done with derge_google opf')
    create_openpecha(namsel_path, output_path, namsel_id)
    print('done with namsel opf')