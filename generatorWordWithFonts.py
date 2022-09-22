import os
import json
import os
import shutil
import threading
import random

from wordcloud import WordCloud, STOPWORDS
from Wikidb import wikiDB


def generate_coralmap(id):
    r = random.randint(0, 4)

    background_color = ['white', '#000000', '#2A0A29', '#2A0A0A', '#0A0A2A']
    bg = background_color[r]

    c = {
        'white': ['cividis', 'PRGn_r', 'bone', 'Greens_r', 'PuBu_r', 'PuBuGn', 'twilight_shifted_r', 'bone_r', 'Greens',
                  'twilight_shifted_r', 'terrain', 'Set2', 'PuRd', 'flag_r', 'tab20', 'binary_r', 'cubehelix', 'CMRmap',
                  'cool_r', 'RdYlBu', 'twilight_shifted_r', 'Set2_r', 'Set2', 'RdYlBu', 'Blues'],
        '#000000': ['terrain', 'binary_r', 'Greens_r', 'Greens', 'tab10_r', 'cividis_r', 'PRGn', 'tab10_r', 'bwr',
                    'Set1_r', 'Dark2', 'Greys_r', 'Dark2', 'Accent', 'RdGy', 'Reds_r', 'RdGy'],
        '#2A0A29': ['bwr', 'PuOr_r', 'Set2_r', 'Set3_r', 'RdPu', 'tab10_r', 'brg_r', 'Dark2', 'Spectral_r', 'Reds_r',
                    'cool_r', 'tab20', 'brg_r', 'Reds', 'tab10_r', 'cool', 'PiYG_r'],
        '#2A0A0A': ['Dark2', 'BuGn', 'RdYlBu_r', 'RdBu', 'coolwarm', 'Paired', 'CMRmap_r', 'terrain',
                    'RdBu',
                    'Accent_r', 'tab20_r', 'Greens', 'Dark2', 'Reds', 'Blues', 'Set3_r', 'flag', 'Dark2', 'PuRd'],
        '#0A0A2A': ['RdGy', 'Blues', 'RdBu', 'PuRd', 'Blues_r', 'coolwarm_r', 'copper', 'tab20_r', 'Blues', 'Dark2_r',
                    'terrain'], '#2E2E2E': ['tab20_r', 'Reds', 'Set3_r', 'Dark2_r', 'Dark2_r']}
    maxx = len(c[bg])
    r = random.randint(0, maxx - 1)
    color = c[bg][r]
    maxx = len(fonts)
    r = random.randint(0, maxx)
    try:
        font = fonts[r]
    except:
        font = ' '
    return bg, color, font


global k
k = 0


def generatedJson(id, name, power, Sattelites, style, sattelites):
    Sattelite = []
    for i in range(len(sattelites)):
        A = {"trait_type": f"Satellite N{i + 1}", 'value': sattelites[i]}
        Sattelite.append(A)
    dict_font = {'53e59-muller-extrabold-demo.ttf': 'Muller', 'beer-money12.ttf': 'Beer money',
                 'caviar-dreams.ttf': 'Caviar dreams', 'cd2f1-36d91_sunday.ttf': 'Sunday',
                 'd9464-arkhip_font.ttf': 'Arkhip', 'impact2.ttf': 'Impact', 'pobeda-regular1.ttf': 'Pobeda',
                 'sfns-display-bold.ttf': 'Display',
                 'sfns-display-thin.ttf': 'Display thin', 'teddy-bear.ttf': 'Teddy', 'Def': 'Def'}

    my_list = {"image": f"ipfs://IPFSPUT/{id}.png", f"name": f"{name}", "attributes": [
        {
            "trait_type": "Sattelites",
            "value": f"{Sattelites}"
        },
        {
            "trait_type": "Power",
            "value": f"{power}"
        },
        {
            "trait_type": "Style",
            "value": f"{dict_font[style]}"
        },
        *Sattelite
    ]}
    with open(f'mnt/HC_Volume_22862748/Json3/{id}.json', 'w') as outfile:
        json.dump(my_list, outfile, indent=4)


def generate_cloud(id, name, power):
    global k
    db = wikiDB()
    s: str = name.split('/')[-1].replace('_', ' ').replace('#', ' ')
    if '%' not in s:
        a = {s: 0.55}
        l, p = db.get_word_from_url(name)
        text = a | l
        if p > 15:
            k += 1
            stopwords = set(STOPWORDS)
            background_color, color, font = generate_coralmap(id)
            if font != ' ':
                wordcloud = WordCloud(stopwords=stopwords, width=1600, height=1600, max_font_size=450, min_font_size=30,
                                      max_words=1000000, colormap=color, background_color=background_color,
                                      font_path='fonts/' + font).fit_words(text)
                wordcloud.to_file(f'mnt/HC_Volume_22862748/Img3/{id}.png')
                style = font
                generatedJson(id, s, power, p, style, list(l))
            else:
                wordcloud = WordCloud(stopwords=stopwords, width=1600, height=1600, max_font_size=450, min_font_size=30,
                                      max_words=1000000, colormap=color, background_color=background_color,
                                      ).fit_words(text)
                wordcloud.to_file(f'mnt/HC_Volume_22862748/Img3/{id}.png')
                style = font
                generatedJson(id, s, power, p, 'Def', list(l))
    db.db_set_pic(id)


if __name__ == '__main__':

    fonts = []
    for filename in os.listdir("fonts"):
        fonts.append(filename)
    try:
        shutil.rmtree('mnt/HC_Volume_22862748/Img3')
        os.mkdir('mnt/HC_Volume_22862748/Img3')
    except:
        os.mkdir('mnt/HC_Volume_22862748/Img3')
    try:
        shutil.rmtree('mnt/HC_Volume_22862748/Json3')
        os.mkdir('mnt/HC_Volume_22862748/Json3')
    except:
        os.mkdir('mnt/HC_Volume_22862748/Json3')
    db = wikiDB()
    db.db_clear_pic()
    while True:
        print(k)
        rows = db.get_wiki_word()
        t1 = threading.Thread(target=generate_cloud, args=(rows[0][0], rows[0][1], rows[0][2]))
        t2 = threading.Thread(target=generate_cloud, args=(rows[1][0], rows[1][1], rows[1][2]))
        t3 = threading.Thread(target=generate_cloud, args=(rows[2][0], rows[2][1], rows[2][2]))
        t4 = threading.Thread(target=generate_cloud, args=(rows[3][0], rows[3][1], rows[3][2]))
        t5 = threading.Thread(target=generate_cloud, args=(rows[4][0], rows[4][1], rows[4][2]))
        t6 = threading.Thread(target=generate_cloud, args=(rows[5][0], rows[5][1], rows[5][2]))
        t7 = threading.Thread(target=generate_cloud, args=(rows[6][0], rows[6][1], rows[6][2]))
        t8 = threading.Thread(target=generate_cloud, args=(rows[7][0], rows[7][1], rows[7][2]))

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        t8.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        t8.join()
