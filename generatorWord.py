import os
import json
import os
import shutil
import threading
import random

from wordcloud import WordCloud, STOPWORDS
from Wikidb import wikiDB

#Функция по генерации стиля
def generate_coralmap():
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

#Функция по генерации json
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
    with open(f'mnt/HC_Volume_22862748/Json3/{int(k / 10000) + 1}/{id}.json', 'w') as outfile:
        json.dump(my_list, outfile, indent=4)


# Функция по созданию картинок
def generate_cloud(id, name, power):
    global k
    db = wikiDB()
    s: str = name.split('/')[-1].replace('_', ' ').replace('#', ' ')
    if '%' not in s:
        a = {s: 0.55}
        l, p = db.get_word_from_url(name)
        text = a | l
        # Проверяем больше ли 15 слов
        if p > 15:
            k += 1
            stopwords = set(STOPWORDS)
            # получаем все стили для картинки
            background_color, color, font = generate_coralmap()
            try:
                os.mkdir(f"mnt/HC_Volume_22862748/Img3/{int(k / 10000) + 1}")
            except:
                pass
            try:
                os.mkdir(f"mnt/HC_Volume_22862748/Json3/{int(k / 10000) + 1}")
            except:
                pass
            # генерируем картинку
            if font != ' ':
                wordcloud = WordCloud(stopwords=stopwords, width=1600, height=1600, max_font_size=450, min_font_size=30,
                                      max_words=1000000, colormap=color, background_color=background_color,
                                      font_path='fonts/' + font).fit_words(text)
                style = font

            else:
                wordcloud = WordCloud(stopwords=stopwords, width=1600, height=1600, max_font_size=450, min_font_size=30,
                                      max_words=1000000, colormap=color, background_color=background_color,
                                      ).fit_words(text)
                style = 'Def'
            # сохраняем картинку
            wordcloud.to_file(f'mnt/HC_Volume_22862748/Img3/{int(k / 10000) + 1}/{id}.png')
            # Запускаем генерацию json
            generatedJson(id, s, power, p, style, list(l))
    db.db_set_pic(id)


if __name__ == '__main__':
    #Выбераем откуда будет генерация
    run = input('Choose where to run the generator\nS - start\nE - end\n')
    fonts = []
    # Берём все шрифты
    for filename in os.listdir("fonts"):
        fonts.append(filename)
    # Создаём или очишаем все зависимые папки
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
    row = db.get_wiki_word()
    #Если с конца то перварачеваем вывод
    if run.lower() == 'e':
        row = row[::-1]
    row=row[:int(len(row)/2)]
    while True:
        print(k)
        rows = row[0:8]
        row = row[8:]
        t = []
        # создаём потоки
        for row0 in rows:
            # В потоки устанавлевам функцию для генерации картинок
            t.append(threading.Thread(target=generate_cloud, args=(row0[0], row0[1], row0[2])))

        # Запускаем потоки
        for i in t:
            i.start()

        # Ждем когда потоки перестанут работать
        for i in t:
            i.join()
