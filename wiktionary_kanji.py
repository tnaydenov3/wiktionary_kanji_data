import re
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
        kj_radical = ''
        kj_composition = ''
        kj_disambig = ''

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
        soup_translingual = BeautifulSoup(extract_section_content(mrk_translingual), 'html.parser') if mrk_translingual else None
        soup_chinese = BeautifulSoup(extract_section_content(mrk_chinese), 'html.parser') if mrk_chinese else None
        soup_japanese = BeautifulSoup(extract_section_content(mrk_japanese), 'html.parser') if mrk_japanese else None
        soup_korean = BeautifulSoup(extract_section_content(mrk_korean), 'html.parser') if mrk_korean else None

        # Get writing data
        kj_radical, kj_composition = get_radical_and_composition(soup_translingual)
        kj_disambig = get_disambig(soup)

        # Get reading data
        # kj_zhuyin = get_zhuyin()
        # kj_kana = get_kana()
        # kj_jyutping = get_jyutping()
        # kj_hangul = get_hangul()
        
        kanji_info = [kanji, kj_radical, kj_composition, kj_disambig, kj_zhuyin, kj_kana, kj_jyutping, kj_hangul]        
        print(kanji_info)

        return '\t'.join(kanji_info)
        
    else:
        return f'Failed to retrieve information for {kanji}. Status code: {response.status_code}'

def get_disambig(soup):
    kj_disambig = ''
    disambig_list = []

    disambig_div = soup.find('div', {'class': re.compile(r'^disambig-see-also')})
    if disambig_div:
        for b_el in disambig_div.find_all('b', {'class': 'Hani'}):
            b_text = b_el.text.strip()
            if not b_text in disambig_list:
                disambig_list += [b_text]
        kj_disambig = ' '.join(disambig_list)
    return kj_disambig

def get_radical_and_composition(soup_translingual):
    mrk_han_char = soup_translingual.find('span', {'id': 'Han_character'})
    p_text = mrk_han_char.find_next('p').text.strip()

    kj_radical = p_text.split('(')[1].split('+')[0].strip().replace(',',':').replace('Kangxi radical','Kangxi')

    kj_composition = p_text.split('composition ')[-1].strip() if 'composition' in p_text else ''
    kj_composition = re.sub(r'\([^)]*\)', '', kj_composition).split(')')[0]

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

def is_kanji(char):
    return bool(re.match(r'^[\u4e00-\u9faf]$', char))

def main():
    input_filename = 'input.txt'
    output_filename = 'output.txt'

    with open(input_filename, 'r', encoding='utf-8') as input_file, open(output_filename, 'w', encoding='utf-8') as output_file:
        for line in input_file:
            kanji = line.strip()
            kanji_info = get_kanji_info(kanji)
            output_file.write(f'{kanji} output:\t{kanji_info}\n')

    print(f'Kanji information has been saved to {output_filename}')

if __name__ == '__main__':
    main()
