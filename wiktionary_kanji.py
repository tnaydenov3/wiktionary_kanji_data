import requests
from bs4 import BeautifulSoup

def get_kanji_info(kanji):
    url = f"https://en.wiktionary.org/wiki/{kanji}"

    # Send a request to the Wiktionary page for the kanji
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Define variables with placeholder values
        kj_radical = "N/A"
        kj_composition = "N/A"
        kj_zhuyin = "N/A"
        kj_onyomi = "N/A"
        kj_kunyomi = "N/A"
        kj_english = "N/A"
        kj_jp = "N/A"
        kj_tw = "N/A"
        kj_cn = "N/A"

        transligual_marker = soup.find('span', {'id': 'Translingual'})
        chinese_marker = soup.find('span', {'id': 'Chinese'})
        japanese_marker = soup.find('span', {'id': 'Japanese'})

        p_text = transligual_marker.find_next('p').text.strip()
        kj_radical = p_text.split('Kangxi radical ')[1].split('+')[0].strip()
        kj_composition = p_text.split('composition ')[-1].replace(')','').strip()

        for dd_el in chinese_marker.find_all_next('dd'):
            dd_text = dd_el.text.strip()
            if '(Zhuyin):' in dd_text:
                kj_zhuyin = dd_text.split(': ')[1].strip()

        for b_el in japanese_marker.find_next('ul').find_all('b'):
            b_text = b_el.text.strip()
            if 'Go-on' in b_text or 'Kan-on' in b_text:
                kj_onyomi = b_el.find_next('span').text.strip().split(' ')[0].strip()
            if 'Kun' in b_text:
                kj_kunyomi = b_el.find_next('span').text.strip().split(' ')[0].strip()
        if kj_onyomi == 'N/A':
            span_el = japanese_marker.find_next('span', {'class': 'on-yomi'})
            if not span_el is None:
                kj_onyomi = span_el.text.strip().split(' ')[0].strip()

        marker = japanese_marker if not japanese_marker is None else chinese_marker
        ol_element = marker.find_next('ol')
        kj_english = ol_element.find('li').text.strip().split('\n')[0].strip()

        table_el = transligual_marker.find_next('table', {'class': 'wikitable floatright'})
        if not table_el is None:
            kj_tw, kj_jp, kj_cn = extract_table_trans(table_el, kj_tw, kj_jp, kj_cn)
        else:
            table_el = japanese_marker.find_next('table')
            if not table_el is None:
                kj_tw, kj_jp = extract_table_jp(table_el, kj_tw, kj_jp)            
            table_el = chinese_marker.find_next('table')
            if not table_el is None:
                kj_tw, kj_cn = extract_table_cn(table_el, kj_tw, kj_cn)

        kanji_info = [kj_jp, kj_tw, kj_cn, kj_radical, kj_composition, kj_zhuyin, kj_onyomi, kj_kunyomi, kj_english]
        kanji_info = '\t'.join(kanji_info).replace('N/A',kanji)
        
        print(kanji_info)
        return kanji_info

    else:
        return f"Failed to retrieve information for {kanji}. Status code: {response.status_code}"
    
def extract_table_trans(table_el, kj_tw, kj_jp, kj_cn):
    for tr_el in table_el.find_all('tr'):
        tr_text = tr_el.text.strip()
        if 'Traditional' in tr_text:
            kj_tw = tr_el.find('td').text.strip()
        if 'Shinjitai' in tr_text:
            kj_jp = tr_el.find('td').text.strip()
        if 'Simplified' in tr_text:
            kj_cn = tr_el.find('td').text.strip()
    return kj_tw, kj_jp, kj_cn

def extract_table_jp(table_el, kj_tw, kj_jp):
    for tr_el in table_el.find_all('tr'):
        tr_text = tr_el.text.strip()
        if 'Kyūjitai' in tr_text:
            kj_tw = tr_el.find('span', {'class': 'Jpan'}).text.strip()
        if 'Shinjitai' in tr_text:
            kj_jp = tr_el.find('span', {'class': 'Jpan'}).text.strip()
    return kj_tw, kj_jp

def extract_table_cn(table_el, kj_tw, kj_cn):
    for tr_el in table_el.find_all('tr'):
        tr_text = tr_el.text.strip()
        if 'trad.' in tr_text:
            kj_tw = tr_el.find('td').text.strip()
        if 'simp.' in tr_text:
            kj_cn = tr_el.find('td').text.strip()
    return kj_tw, kj_cn

def main():
    input_filename = "input.txt"
    output_filename = "output.txt"

    with open(input_filename, "r", encoding="utf-8") as input_file, open(output_filename, "w", encoding="utf-8") as output_file:
        for line in input_file:
            kanji = line.strip()
            kanji_info = get_kanji_info(kanji)
            output_file.write(f"{kanji}\tOutput status:\t{kanji_info}\n")

    print(f"Kanji information has been saved to {output_filename}")

if __name__ == "__main__":
    main()
