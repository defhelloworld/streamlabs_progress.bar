import linecache
import sys
from lxml import html
import re
import argparse

parser = argparse.ArgumentParser(description='Govno ebanoe za 3 chasa')
parser.add_argument("--mana_add", default=None, type=int, help="Аргумент для передачи mana")

args = parser.parse_args()

u = int(args.mana_add)

progressbar = "C://Users//Zenusoid//AppData//Roaming//Streamlabs//Streamlabs Chatbot//Services//Scripts//TestGovno//index.html"

with open(progressbar, "r", encoding="UTF-8") as file:
    tree = html.parse(file)

    h2_element = tree.xpath('//h2')[0]

    h2_element.text = h2_element.text.replace('O', '0')

    match_re = re.findall(r'\d+', h2_element.text)
    if match_re:
        first_number = int(match_re[0])
        last_number = int(match_re[-1])

        new_first_number = str(first_number + u)

        h2_element.text = h2_element.text.replace(str(first_number), str(new_first_number), 1)

        percentage = (first_number + u) / last_number * 100
        if percentage > 100:
            percentage = 100


        progress_fill = tree.xpath('//div[@class="progress-fill"]')[0]
        current_style = progress_fill.get('style', '')
        if 'width:' in current_style:
            new_style = re.sub(r'width:\s*[\d.]+%;', f'width: {percentage:.1f}%;', current_style)
        else:
            new_style = current_style + f' width: {percentage:.1f}%;'
        progress_fill.set('style', new_style)

        new_html = html.tostring(tree, pretty_print=True, encoding='unicode')

with open(progressbar, "w", encoding='UTF-8') as file:
    file.write(new_html)
