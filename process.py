# -*- coding: UTF-8 -*-
import xlrd
import requests
import re

# define english words as latin-1 + common punctuations + Super/Sub scripts + currency + math symbol
non_en_pattern = re.compile('([\u0300-\u1cdf]|[\u1f00-\u1fff]|[\u2b00-\ua6ff]|[\ua800-\ufe1f]|[\ufe30-\uffff])+')
data = xlrd.open_workbook('FemaleA.xlsx')
sheet = data.sheets()[0]  # load the first sheet
data0 = sheet.col_values(0)  # load the first column data


def is_non_english(string):
    """判断一个utf-8字符串是否为英文合法字符"""
    match = non_en_pattern.search(string)
    return match  # true: non english exist


sing_name = ""
singer = []
lyrics = ""
info = []  # to note down target info
flag = True  # to note down whether this song involves non-english words; none is True
authen = ('5226dc5a-e3b4-4ab8-b060-b1912ce05c54', 'Jrz1z5OuFVTj')
headers1 = {
    'Content-Type': 'text/plain',
    'charset': 'utf-8'
}


def process_sentiment(lyric):
    res = requests.post('https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21',
                        auth=authen, data=lyric, headers=headers1)
    result = res.text
    res.close()
    print(result)
    song_tone = []
    pattern1 = re.compile('\"score\":[01]\.[0-9]+')
    pattern2 = re.compile('\"tone_id\":\"[A-Za-z]+\"')
    scores = pattern1.findall(result)
    ids = pattern2.findall(result)
    score = []
    id = []
    for i in scores:
        i_new = i.split(":")
        score.append(i_new[1])
    for j in ids:
        j_new = j.split(":")
        id.append(j_new[1])
    for i in range(0, len(score)):
        song_tone.append("[" + score[i] + ", " + id[i] + "]")

    return song_tone


if __name__ == '__main__':

    for line in data0:
        if 'Written by' in line:
            continue
        if is_non_english(line):
            flag = False
            continue

        if ' - ' in line:
            if sing_name != "":
                if flag:
                    #lyrics.encode('utf-8').decode('latin-1')
                    song_tone = process_sentiment(lyrics)
                    info.append([sing_name, singer, song_tone])
                sing_name = ""
                lyrics = ""
                singer = []
            flag = True
            new_line = line.split(' - ')
            sing_name = new_line[0]
            singers = new_line[1]
            singer = singers.split('/')
            continue

        lyrics = lyrics + line + " "

    song_tone = process_sentiment(lyrics)
    info.append([sing_name, singer, song_tone])
    out = open('result', 'w')
    out.write("{")
    punc0 = len(info)-1  # to calculate numbers of punc in whole list
    for i in info:
        if len(i[2])>0:
            out.write("{ song:" + i[0] + ", singers:[")
            punc1 = len(i[1])-1
            for j in i[1]:
                out.write(j)
                if punc1 > 0:
                    out.write(", ")
                    punc1 = punc1 - 1
            out.write("], tones:{")
            punc2 = len(i[2])-1  # to calculate numbers of punctuation
            for j in i[2]:
                out.write(j)
                if punc2>0:
                    out.write(", ")
                    punc2 = punc2-1
            out.write("} } ")
            if punc0>0:
                out.write(", ")
                punc0 = punc0-1

    out.write(" }")
    out.close()
