from pathlib import Path
import re

def get_img_num(index_num, index_end):
    if index_end == 'a':
        img_num = (int(index_num)*2) -1 
    elif index_end == 'b':
        img_num = (int(index_num)*2)
    return img_num


def update_pagination(hfml_text):
    new_hfml = ''
    match_extra = None
    text_lists = hfml_text.splitlines()
    for text in text_lists:
        if re.search(r"\[([𰵀-󴉱])?\d+[a-z]{1}\]", text):
            match = re.match(r'(.*)\[(.*)\]', text)
            match_extra = match.group(1)
            match_inside = match.group(2)
            output = re.match(r"([𰵀-󴉱])(\d+)([a-z]{1})", match_inside)
            index_num = output.group(2)
            index_end = output.group(3)
            img_num = get_img_num(index_num, index_end)
            new_hfml += f'〔{img_num}〕' + '\n'
        else:
            if match_extra:
                if text:
                    new_hfml += match_extra+text + '\n'
                    match_extra = None
                else:
                    new_hfml += text + '\n'
            else:
                new_hfml += text + '\n'
    return new_hfml
        



if __name__=='__main__':
    hfml_paths = list(Path(f'./tengyur/updated_durchen/derge_google').iterdir())
    hfml_paths.sort()
    for hfml_path in hfml_paths:
        vol_num = hfml_path.stem
        hfml_text = Path(f'{hfml_path}').read_text(encoding='utf-8')
        new_hfml = update_pagination(hfml_text)
        Path(f'./tengyur/new_hfml/derge_google/{vol_num}.txt').write_text(new_hfml, encoding='utf-8')
        print(f'{vol_num} done')
