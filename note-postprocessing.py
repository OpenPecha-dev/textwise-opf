import re
from pathlib  import Path
from preprocess import get_pages

def has_double_notes(note_line):
    pecing_notes = re.findall('«པེ་»', note_line)
    narthang_notes = re.findall('«སྣར་»', note_line)
    if len(pecing_notes)>1 or len(narthang_notes)>1:
        return True
    else:
        return False

def get_note_num(note):
    num = 1
    if num_pat := re.search('\d+', note):
        num = int(num_pat[0])
    return num

def get_split_notes(notes, text_type):
    splited_notes = []
    cur_note = ''
    cur_note_num = get_note_num(notes[0])
    for note in notes:
        if re.search('\d+', note):
            pass
        elif not re.search('«.+»', note):   
            cur_note += note
            if text_type == "namsel":
                splited_notes.append(f'<u{cur_note_num}>{cur_note}')
            else:
                splited_notes.append(f'{cur_note_num}{cur_note}')
            cur_note_num += 1
            cur_note = ""
        else:
            cur_note += note
    if cur_note:
        splited_notes.append(f'{cur_note_num}{cur_note}')
    return splited_notes

def get_reformated_note(note_line, text_type):
    reformated_notes = ''
    notes = re.split('(«པེ་»|«སྣར་»?)', note_line)
    notes = [note for note in notes if note]
    splited_notes = get_split_notes(notes, text_type)
    reformated_notes = "\n".join(splited_notes)
    reformated_notes = re.sub('<u.+><u.+>\n', '', reformated_notes)
    return reformated_notes

    
def post_process_note(note_content, text_type):
    new_notes = ''
    lines = note_content.splitlines()
    for line in lines:
        if has_double_notes(line):
            new_notes += get_reformated_note(line, text_type) + '\n'
        else:
            new_notes += line + '\n'
    return new_notes

def post_process_text(text, text_type):
    new_text = ''
    pages = get_pages(text)
    for page in pages:
        if "«" in page:
            new_text += post_process_note(page, text_type)
        else:
            new_text += page
    return new_text
        


if __name__ == "__main__":
    text = Path('./test/D1118_nam.txt').read_text(encoding='utf-8')
    new_text = post_process_text(text, text_type="namsel")
    Path('./test/new_D1118_nam.txt').write_text(new_text, encoding='utf-8')