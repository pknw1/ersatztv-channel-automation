import sqlite3
#import re

connection = sqlite3.connect("../testdata/ersatztv.sqlite3")
cursor = connection.cursor()


rows = cursor.execute("SELECT id FROM PlexMovie ORDER BY id  ASC LIMIT 1").fetchall()
for row in rows:
    for item in row:
        res = str(item) 
        print(res)
        title = cursor.execute("SELECT Title FROM MovieMetadata WHERE MovieId = 985").fetchall()
        for movietitle in title:
            displaytitle=str(movietitle)
            test=movietitle[0]
            print(test)


