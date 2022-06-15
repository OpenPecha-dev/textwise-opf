import re
from itertools import zip_longest
from pathlib import Path

def get_pages(vol_text):
    result = []
    pg_text = ""
    pages = re.split(r"(\[[𰵀-󴉱]?[0-9]+[a-z]{1}\])", vol_text)
    for i, page in enumerate(pages[1:]):
        if i % 2 == 0:
            pg_text += page
        else:
            pg_text += page
            result.append(pg_text)
            pg_text = ""
    return result

def transfer_durchen(src_pg, tar_pg):
    new_pg = tar_pg
    if '<d' in src_pg:
        new_pg =  re.sub(r"(\[[𰵀-󴉱]?[0-9]+[a-z]{1}\])", '\g<1>\n<d', new_pg)
    if 'd>' in src_pg:
        new_pg += 'd>\n\n'
    return new_pg

def transfer_durchens(src_vol, tar_vol):
    new_vol = ''
    src_pages = get_pages(src_vol)
    target_pages = get_pages(tar_vol)
    for src_pg, tar_pg in zip_longest(src_pages, target_pages, fillvalue=''):
        new_vol += transfer_durchen(src_pg, tar_pg)
    return new_vol.strip()


def flow():
    target_vol_paths = list(Path('./tengyur/serialized/derge_google').iterdir())
    src_vol_paths = list(Path('./tengyur/pedurma_durchen/derge_google_with_durchen').iterdir())
    target_vol_paths.sort()
    src_vol_paths.sort()
    for src_vol_path, target_vol_path in zip(src_vol_paths, target_vol_paths):
        src_vol_text = src_vol_path.read_text(encoding='utf-8')
        target_vol_text = target_vol_path.read_text(encoding='utf-8')
        new_vol_text = transfer_durchens(src_vol_text, target_vol_text)
        Path(f'./tengyur/updated_durchen/derge_google/{target_vol_path.stem}.txt').write_text(new_vol_text)
        print(f'{target_vol_path.stem} completed...')


if __name__ == "__main__":
    flow()
    print('done')

