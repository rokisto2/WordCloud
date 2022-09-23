import random
import re

import pymysql


class wikiDB:
    #Подключение к бд
    def __init__(self):
        self.connect = pymysql.connect(host='localhost', user='root', password='1111', database="wiki")

    def __del__(self):
        self.connect.close()
    #Добавление ссылок на обработку
    def add_raw_urls(self, urls):
        try:
            with self.connect.cursor() as cursor:

                for url in urls:

                    try:
                        cursor.execute("INSERT INTO rawwiki (url) VALUE (%s)", url)
                        self.connect.commit()
                    except:
                        pass

            cursor.close()
            self.connect.close()
        except:
            print('error 1')
    #Добавление ссылок в главную таблицу
    def add_url(self, url: str, u):
        try:

            with self.connect.cursor() as cursor:
                cursor.execute("INSERT INTO wikiurl (url) VALUE (%s)", url.strip())

            self.connect.commit()
            cursor.close()
            return 0

        except Exception as e:
            return -1
    #Поиск определённого url
    def find_url(self, url):

        with self.connect.cursor() as cursor:
            cursor.execute("SELECT id FROM wikiurl WHERE url = %s", url)
            self.connect.commit()
            row = cursor.fetchall()
            cursor.close()
            return row[0][0]

    #Создание зависемостей от одной ссылки
    def creat_mig(self, id, url):
        try:
            with self.connect.cursor() as cursor:

                cursor.execute("INSERT INTO wikiaddiction (wikiId, url) VALUES (%s, %s)", (id, url))
            self.connect.commit()
            cursor.close()
        except:
            print('error')

    #Получаем все термины которые в стречаються на данном сайте
    def get_word_from_url(self, url):
        with self.connect.cursor() as cursor:
            #Берём все зависимые ссылки
            cursor.execute("SELECT wikiid FROM wikiaddiction WHERE url = %s", url)
            self.connect.commit()
            id = cursor.fetchall()
            ids = ''
            for i in id:
                ids+=str(i[0])+', '
            ans = {}
            k = 1
            try:
                #Берём все термины из ссылок
                cursor.execute(f"SELECT termin FROM wikiurl where id IN ({ids[:-2]})")
                self.connect.commit()

                termins = cursor.fetchall()
                for termin0 in termins:
                    #Проверяем термины на невоспроизводимые символы
                    termin = str(termin0[0]).split('/')[-1].replace('_', ' ').encode('utf-16').decode('utf-16').replace('#', ' ')
                    if '%' not in termin:
                        k+=1
                        ans[termin] = 0.05

            except:
                k=-1

        cursor.close()
        return ans, k

    # Берём все ссылки которые не проверели
    def get_wiki_word(self):
        with self.connect.cursor() as cursor:
            cursor.execute("SELECT id,url,power FROM wikiurl where status != 'pic' ORDER BY power DESC ")
            self.connect.commit()
            row = cursor.fetchall()
            cursor.close()

        return row

    #Устанавливаем на определенную ссылку что мы её проверили
    def db_set_pic(self, id):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute("UPDATE wikiurl SET status = 'pic' WHERE id = %s", id)
            self.connect.commit()
        except Exception as e:
            print(-1)
        finally:
            cursor.close()

    # Устанавливаем на все ссылки что мы их не проверели
    def db_clear_pic(self):
        with self.connect.cursor() as cursor:
            cursor.execute("UPDATE wikiurl SET status = ' '")
        self.connect.commit()
        cursor.close()