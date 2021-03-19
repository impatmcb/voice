from whoosh.index import create_in
from whoosh.fields import *
import os
import csv
import re

file = open('kcsarticles.csv', 'r', encoding="utf8")
reader = list(csv.reader(file))

for r in reader:
    title = str(r[3])
    if "/" or '"' or '*' or '|' or '?' or '(' or ')' or ':' or ';' or '\\' or '<' in title:
        title = re.sub('/|"|\*|\||\?|\(|\)|:|;|\\\\|<|>', '', title)
    if title[-1] == ".":
        title = re.sub('.', '', title)
    kcsinfo = str(r[14]) + "\n\nKeywords: \n" +str(r[13])
    if "\\n" in kcsinfo:
        kcsinfo = re.sub('\\\\n|\\\\r', "\n", kcsinfo)
    newfile = open("/SutterVoice/kcsarticles/" + title + ".txt", 'w+')
    newfile.write(kcsinfo)
    newfile.close()

schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True), textdata=TEXT(stored=True))

ix = create_in("indexdir", schema)
writer = ix.writer()
filepath = os.listdir("kcsarticles")
for i in filepath:
    path = os.path.join("kcsarticles", i)
    title = i.split(".txt")[0]
    file = open("kcsarticles/" + i, 'r')
    text = file.read()
    writer.add_document(title=title, path=path, content=text, textdata=text)
    file.close()
writer.commit()

