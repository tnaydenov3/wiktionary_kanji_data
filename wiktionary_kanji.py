import requests
from bs4 import BeautifulSoup

ID_TRANSLINGUAL = 'Translingual'
ID_CHINESE = 'Chinese'
ID_JAPANESE = 'Japanese'
ID_KOREAN = 'Korean'

def get_kanji_info(kanji):
    url = f'https://en.wiktionary.org/wiki/{kanji}'

    # Send a request to the Wiktionary page for the kanji
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Table of content
        kj_rel_variants = ''
        kj_alt_forms = ''
        kj_radical = ''
        kj_composition = ''

        kj_zhuyin = ''
        kj_kana = ''
        kj_jyutping = ''
        kj_hangul = ''

        # Span markers
        mrk_translingual = soup.find('span', {'id': ID_TRANSLINGUAL})
        mrk_chinese = soup.find('span', {'id': ID_CHINESE})
        mrk_japanese = soup.find('span', {'id': ID_JAPANESE})
        mrk_korean = soup.find('span', {'id': ID_KOREAN})

        # Sections
        sctn_translingual = BeautifulSoup(extract_section_content(mrk_translingual), 'html.parser') if mrk_translingual else None
        sctn_chinese = BeautifulSoup(extract_section_content(mrk_chinese), 'html.parser') if mrk_chinese else None
        sctn_japanese = BeautifulSoup(extract_section_content(mrk_japanese), 'html.parser') if mrk_japanese else None
        sctn_korean = BeautifulSoup(extract_section_content(mrk_korean), 'html.parser') if mrk_korean else None

        # Get writing data
        kj_rel_variants = get_related_variants(sctn_translingual)
        kj_alt_forms = get_alt_forms(sctn_translingual)
        kj_radical, kj_composition = get_radical_and_composition(sctn_translingual)

        # Get reading data
        # kj_zhuyin = get_zhuyin()
        # kj_kana = get_kana()
        # kj_jyutping = get_jyutping()
        # kj_hangul = get_hangul()
        
        kanji_info = [kanji, kj_rel_variants, kj_alt_forms, kj_radical, kj_composition, kj_zhuyin, kj_kana, kj_jyutping, kj_hangul]        
        print(kanji_info)

        return kanji_info
    
    else:
        return f'Failed to retrieve information for {kanji}. Status code: {response.status_code}'
    
def get_related_variants(sctn_translingual):
    el_related_chars = sctn_translingual.find('span', {'id': 'Related_characters'})
    if el_related_chars:
        vars_list = []
        for li_el in el_related_chars.find_next('ul').find_all('li'):
            vars_list += [li_el.find('span').text.strip()]
        kj_rel_variants = ' '.join(vars_list)
    return kj_rel_variants

def get_alt_forms(sctn_translingual):
    kj_alt_forms = ''
    el_alt_forms = sctn_translingual.find('span', {'id': 'Alternative_forms'})
    if el_alt_forms:
        print(el_alt_forms.text.strip())
        alt_list = []
        for li_el in el_alt_forms.find_next('ul').find_all('li'):
            alt_list += [li_el.find('span').text.strip()]
        kj_alt_forms = ' '.join(alt_list)    
    return kj_alt_forms

def get_radical_and_composition(sctn_translingual):
    el_han_char = sctn_translingual.find('span', {'id': 'Han_character'})
    p_text = el_han_char.find_next('p').text.strip()
    kj_radical = p_text.split('(')[1].split('+')[0].strip().replace(',',':')
    kj_composition = p_text.split('composition ')[-1].replace(')','').strip() if 'composition' in p_text else ''
    return kj_radical, kj_composition

def extract_section_content(start_marker):
    start_element = start_marker.find_parent('h2')
    end_element_tag='h2'
    content = []
    current_element = start_element.find_next()

    while current_element and current_element.name != end_element_tag:
        content.append(str(current_element))
        current_element = current_element.find_next()

    return ''.join(content)
    
def main():
    input_filename = 'input.txt'
    output_filename = 'output.txt'

    with open(input_filename, 'r', encoding='utf-8') as input_file, open(output_filename, 'w', encoding='utf-8') as output_file:
        for line in input_file:
            kanji = line.strip()
            kanji_info = get_kanji_info(kanji)
            output_file.write(f'{kanji} - Output:\t{kanji_info}\n')

    print(f'Kanji information has been saved to {output_filename}')

if __name__ == '__main__':
    main()
