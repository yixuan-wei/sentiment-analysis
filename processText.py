import requests
import re

authen = ('5226dc5a-e3b4-4ab8-b060-b1912ce05c54', 'Jrz1z5OuFVTj')
headers1 = {
    'Content-Type': 'application/json',
    'charset': 'utf-8'
}
ref = {}
filein = open('result')
data = open('text')

def read_data(file):
    for i in file:
        print(re.findall('{ song:[ ]}',i))



def process_sentiment(text):
    res = requests.post('https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21',
                        auth=authen, data=text, headers=headers1)
    result = res.text
    res.close()
    print(result)
    text_tone = []
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
        text_tone.append("[" + score[i] + ", " + id[i] + "]")

    return text_tone


def song_match(text):
    text_tone_gen = process_sentiment(text)


if __name__ == '__main__':
    read_data(filein)
