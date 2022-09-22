import pymysql

connect = pymysql.connect(host='localhost', user='root', password='1111', database="wiki")


with connect.cursor() as cursor:
    cursor.execute("SELECT * FROM wikiurl")
    connect.commit()
    rows = cursor.fetchall()
    cursor.close()

for row in rows:
    id = row[0]
    termin = str(row[1].split('/')[-1]).replace('_', ' ')
    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM wikiaddiction where wikiid = %s", id)
        connect.commit()
        row0 = cursor.fetchall()
        cursor.close()
    power = len(row0)
    try:

        with connect.cursor() as cursor:
            cursor.execute("UPDATE wikiurl SET termin = %s, power = %s WHERE id = %s", (termin, power, id))
        connect.commit()
    except Exception as e:
        print(-1)

