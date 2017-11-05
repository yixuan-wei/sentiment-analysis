import requests
import re
import json
from .process import process_sentiment

authen = ('5226dc5a-e3b4-4ab8-b060-b1912ce05c54', 'Jrz1z5OuFVTj')
headers1 = {
    'Content-Type': 'application/json',
    'charset': 'utf-8'
}
ref = {}
filein = open('data')
data = open('text')


def read_data(file):
    data = []
    for i in file:
        data.append(json.loads(i))
    return data


def song_match(text):
    text_tone_gen = process_sentiment(text)


if __name__ == '__main__':
    data = read_data(filein)
    for piece in data:
        print(piece.songs)

filein.close()
data.close()
