import numpy as np
import re
from nltk.corpus import stopwords

stop = stopwords.words('english')
def tokenizer(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text.lower())
    text = (re.sub('[\W]+', ' ', text.lower()) + ' '.join(emoticons).replace('-', ''))
    tokenized = [w for w in text.split() if w not in stop]
    return tokenized

def stream_docs(path):
    with open(path, 'r', encoding='utf-8') as csv:
        next(csv)
        for line in csv:
            print(line[:-3])
            print(int(line[-2]))
            #  text, label = line[:-3], int(line[-2])
            # yield text, label

next(stream_docs(path='movie_data.csv'))
