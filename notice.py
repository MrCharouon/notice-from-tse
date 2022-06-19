#!/usr/bin/python
from bs4 import BeautifulSoup as bs
import pandas as pd
import subprocess
import requests
import csv
import sqlite3
import re
import os
import time

exit_code = subprocess.call('/home/ali/tmp/notice-from-tse/directory.sh')
# print(exit_code)
PATH = '/tmp/notice/'

### Get information from the server
url = 'http://www.tsetmc.com/Loader.aspx?ParTree=151313&Flow=0'
r = requests.get(url)
soup = bs(r.content)

result = soup.find_all(attrs={'class': 'table1'})
# result

### Save information in Output.txt file
string_it = str(result)

with open("/tmp/notice/Output.txt", "w+") as fo:
        fo.write(string_it)
        fo.close()
# string_it


### find the string by replacing and Save this in replacing_Output.txt file
### e by a
string = string_it

a = (string.replace("[", ""))
b = (a.replace("<tr>", ""))
c = (b.replace("</tr>", ""))
d = (c.replace("<th>", "\""))
f = (d.replace("</th>", ""))
# g = (f.replace("</td>", "\""))
g = (f.replace("</td>", ""))
m = (g.replace("<tbody>", ""))
n = (m.replace("</tbody>", ""))
h = (n.replace("<hr/>", ""))
j = (h.replace("</table>", ""))
u = (j.replace("]", ""))
i = (u.replace("<th class=\"ltr\">", ""))
o = (i.replace("<td colspan=\"2\">", ""))
final_result = (o.replace("<table class=\"table1\">", ""))

replacing_Output = str(final_result)
with open("/tmp/notice/replacing_Output.txt", "w+") as fo:
        fo.write(replacing_Output)
        fo.close()
# print(replacing_Output)



### Removes extra lines from replacing_Output.txt and save new data on the Final_Output.txt
output = ""
with open("/tmp/notice/replacing_Output.txt") as f:
    for line in f:
        if not line.isspace():
            output+=line
f= open("/tmp/notice/Final_Output.txt","w")
f.write(output)
# print(output)



### split lines from "
grade_data = output.split('\"')
# print(grade_data[1],"\n")
# print(grade_data[2],"\n")
# print(grade_data[99],"\n")
# print(grade_data[100],"\n")
len(grade_data)
# type(grade_data)


### Save data to grade_data.csv file
df = pd.DataFrame(grade_data)
df.to_csv('/tmp/notice/grade_data.csv', index=False)
len(df)




### Convert csv to database for find the values
file = open('/tmp/notice/grade_data.csv')
csvreader = csv.reader(file)
header = next(csvreader)
db_rows = []
for row in csvreader:
    db_rows.append(row)
file.close()


conn = sqlite3.connect('/tmp/notice/grade_data.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS data')
cur.execute("""CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message Text );""")
conn.commit()

def Insert_Data ():

    for i in range(1, len(db_rows)):

        message = str(db_rows[i][0])
        number = i
        query = f'INSERT INTO data VALUES ("{number}", "{message}")'
        cur.execute(query)
        conn.commit()

    conn.close()

Insert_Data()



### search dataframe for column
conn = sqlite3.connect('/tmp/notice/grade_data.db')
cur0 = conn.cursor()
cur1 = conn.cursor()
cur2 = conn.cursor()
# Variable = '12'
# cur.execute("SELECT * FROM data WHERE id=?", (Variable,))

Variable0 = 'پذيره نويسي'
cur0.execute("SELECT message FROM data WHERE message like '%'||?||'%'", (Variable0,))
Variable1 = 'عرضه اوليه'
cur1.execute("SELECT message FROM data WHERE message like '%'||?||'%'", (Variable1,))
Variable2 = 'ثبت سفارش'
cur2.execute("SELECT message FROM data WHERE message like '%'||?||'%'", (Variable2,))

rows0 = cur0.fetchall()
rows1 = cur1.fetchall()
rows2 = cur2.fetchall()
conn.close()

notice_rows0 = []
for row0 in rows0:
    notice_rows0.append(row0)
notice_rows1 = []
for row1 in rows1:
    notice_rows1.append(row1)
notice_rows2 = []
for row2 in rows2:
    notice_rows2.append(row2)

notice_rows = list(set(notice_rows0 + notice_rows1 + notice_rows2))
# notice_rows.reverse()



### Show notifications
def convertTuple(tup):
        # initialize an empty string
    str = ''
    for item in tup:
        str = str + item
    return str

n = 0

# print(len(notice_rows))
len_rows = (len(notice_rows))
if (len_rows == 0 ):
    final_output = "فعلا خبری نیست"
    os.system(f'notify-send {n}"/"{len(notice_rows)} "{final_output}"')
    os.system("mpv /home/ali/tmp/notice-from-tse/bell.mp3")

else:
    for i in range (len(notice_rows)):
    #     print(notice_rows[n])
        tuple = (notice_rows[n])
        sample_str = convertTuple(tuple)
        print ((len(sample_str)))
    #     aaa = str(notice_rows[n])
        final_output = re.sub("^", "  * پیام :  ", sample_str)
        os.system(f'notify-send {n+1}"/"{len(notice_rows)} "{final_output}"')
        os.system("mpv /home/ali/tmp/notice-from-tse/bell.mp3")
#         print(final_output)
        n+=1
        time.sleep(12)



