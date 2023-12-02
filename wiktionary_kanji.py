import requests
from bs4 import BeautifulSoup

def get_kanji_info(kanji):
    url = f"https://en.wiktionary.org/wiki/{kanji}"

    # Send a request to the Wiktionary page for the kanji
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the relevant section on the page (you may need to customize this based on Wiktionary's structure)
        kanji_info_section = soup.find("div", {"class": "section-paragraph"})

        for p_el in soup.find_all('p'):
            p_text = p_el.text.strip()
            if 'composition' in p_text:
                kj_composition = p_text.split('composition ')[-1].replace(')','').strip()
                break

        kanji_info = kj_composition

        print(kanji_info)
        return kanji_info

    else:
        return f"Failed to retrieve information for {kanji}. Status code: {response.status_code}"

def main():
    input_filename = "input.txt"
    output_filename = "output.txt"

    with open(input_filename, "r", encoding="utf-8") as input_file, open(output_filename, "w", encoding="utf-8") as output_file:
        for line in input_file:
            kanji = line.strip()
            kanji_info = get_kanji_info(kanji)
            output_file.write(f"{kanji}\t{kanji_info}\n")

    print(f"Kanji information has been saved to {output_filename}")

if __name__ == "__main__":
    main()
