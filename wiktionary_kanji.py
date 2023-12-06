import requests
from bs4 import BeautifulSoup

def get_kanji_info(kanji):
    url = f'https://en.wiktionary.org/wiki/{kanji}'

    # Send a request to the Wiktionary page for the kanji
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Define variables with placeholder values
        kj_variants = ''
        kj_alt_forms = ''

        kj_radical = ''
        kj_composition = ''

        kj_zhuyin = ''
        kj_kana = ''

        # Span markers
        mrk_translingual = soup.find('span', {'id': 'Translingual'})
        mrk_chinese = soup.find('span', {'id': 'Chinese'})
        mrk_japanese = soup.find('span', {'id': 'Japanese'})

        # Sections
        sctn_translingual = extract_section_content(mrk_translingual)
        sctn_chinese = extract_section_content(mrk_chinese)
        sctn_japanese = extract_section_content(mrk_japanese)

        el_alt_forms = soup.find('span', {'id': 'Alternative_forms'})
        if el_alt_forms:
            print(el_alt_forms.text.strip())
            alt_list = []
            for li_el in el_alt_forms.find_next('ul').find_all('li'):
                alt_list += [li_el.find('span').text.strip()]
            kj_alt_forms = ' '.join(alt_list)

        el_han_char = soup.find('span', {'id': 'Han_character'})
        p_text = el_han_char.find_next('p').text.strip()
        kj_radical = p_text.split('(')[1].split('+')[0].strip().replace(',',':')
        kj_composition = p_text.split('composition ')[-1].replace(')','').strip() if 'composition' in p_text else ''

        el_related_chars = soup.find('span', {'id': 'Related_characters'})
        if el_related_chars:
            vars_list = []
            for li_el in el_related_chars.find_next('ul').find_all('li'):
                vars_list += [li_el.find('span').text.strip()]
            kj_variants = ' '.join(vars_list)
        
        kanji_info = [kanji, kj_variants, kj_alt_forms, kj_radical, kj_composition, kj_zhuyin, kj_kana]        
        print(kanji_info)

        return kanji_info

    else:
        return f'Failed to retrieve information for {kanji}. Status code: {response.status_code}'
        
def extract_section_content(start_element):
    end_element = start_element.find_next('h2')

    if start_element and end_element:
        content = []
        current_element = start_element.find_next()

        while current_element and current_element != end_element:
            content.append(str(current_element))
            current_element = current_element.find_next()

        return ''.join(content)
    else:
        return None
    
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
