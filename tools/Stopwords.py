#/usr/bin/env python
# -*- coding: utf-8 -*-
# Written by Sam Tseng on 2018/09/20
# So far, this file works best for English and Chinese.

import sys, re
from nltk.stem import PorterStemmer, WordNetLemmatizer

# The English punctuations are from: https://keras.io/preprocessing/text/
English_PUNCTUATIONS = '''
!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
'''
English_PUNCTUATIONS = [c for c in English_PUNCTUATIONS]

Chinese_PUNCTUATIONS = r'''
！＃＄％＆\、（）＊＋，。/：；「」『』　■．．・…’’“”〝〞‵′。
''' # there is a Chinese white space before '■'
Chinese_PUNCTUATIONS = [c for c in Chinese_PUNCTUATIONS]

PUNCTUATIONS = Chinese_PUNCTUATIONS
PUNCTUATIONS.extend(English_PUNCTUATIONS)


# https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/feature_extraction/stop_words.py
English_STOP_WORDS = '''
    a about above across after afterwards again against
    all almost alone along already also although always
    am among amongst amoungst amount an and another
    any anyhow anyone anything anyway anywhere are
    around as at back be became because become
    becomes becoming been before beforehand behind being
    below beside besides between beyond bill both
    bottom but by call can cannot cant co con
    could couldnt cry de describe detail do done
    down due during each eg eight either eleven else
    elsewhere empty enough etc even ever every everyone
    everything everywhere except few fifteen fifty fill
    find fire first five for former formerly forty
    found four from front full further get give go
    had has hasnt have he hence her here hereafter
    hereby herein hereupon hers herself him himself his
    how however hundred i ie if in inc indeed
    interest into is it its itself keep last latter
    latterly least less ltd made many may me
    meanwhile might mill mine more moreover most mostly
    move much must my myself name namely neither
    never nevertheless next nine no nobody none noone
    nor not nothing now nowhere of off often on
    once one only onto or other others otherwise our
    ours ourselves out over own part per perhaps
    please put rather re same see seem seemed
    seeming seems serious several she should show side
    since sincere six sixty so some somehow someone
    something sometime sometimes somewhere still such
    system take ten than that the their them
    themselves then thence there thereafter thereby
    therefore therein thereupon these they thick thin
    third this those though three through throughout
    thru thus to together too top toward towards
    twelve twenty two un under until up upon us
    very via was we well were what whatever when
    whence whenever where whereafter whereas whereby
    wherein whereupon wherever whether which while whither
    who whoever whole whom whose why will with
    within without would yet you your yours yourself
    yourselves
'''.split()
English_STOP_WORDS.extend('''said told '''.split())

Chinese_STOP_WORDS = '''
的 是 了 和 與 及 或 於 也 並 之 以 在 另 又 該 由 但 仍 就
都 讓 要 把 上 來 說 從 等 
我 你 他 妳 她 它 您 我們 你們 妳們 他們 她們 
有 此 因 且 為 嗎 那 哪 吧 很 這
並有 並可 可以 可供 提供 以及 包括 另有 另外 此外 除了 目前 現在 仍就 就是 
⒈ ⒉ ⒊ 可能 應該 則是 它會 這麼 什麼 因為 那些 圖上
'''.split()
# StopWords.extend(['　', '■']) # these chars belong to r'\W'
#Chinese_STOP_WORDS= []


# Combine multi-lingual stop words
STOP_WORDS = Chinese_STOP_WORDS
STOP_WORDS.extend(English_STOP_WORDS)
#print(STOP_WORDS)


def clean_text(text): 
    '''
    Given a raw text string, return a clean text string.
    Example: 
        input:  "Years  passed. 多少   年过 去 了 。  "
        output: "years passed.多少年过去了。"
    '''
    text = text.lower() # 'years  passed. 多少   年过 去 了 。'
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"\'scuse", " excuse ", text)
    # Next line will remove punctuations. \w matches Chinese characters
    #text = re.sub('\W', ' ', text) # 'Years passed  多少 年过 去 了  '
    # Next line will remove redundant white space for jeiba to cut
    text = re.sub(r'\s+([^a-zA-Z0-9.])', r'\1', text) # years passed.多少年过去了。
# see: https://stackoverflow.com/questions/16720541/python-string-replace-regular-expression
    text = text.strip(' ')
    return text


ps = PorterStemmer()
wnl = WordNetLemmatizer()

def clean_words(words, RmvStopWord=True, RmvMark=True):
#    print("After jieba.lcut():", words)
#    WL = [ w 
    WL = [ ps.stem(w)
#    WL = [ wnl.lemmatize(w)
        for w in words 
          if (not re.match(r'\s', w)) # remove white spaces
            and (RmvMark==False or not re.match(r'\W', w)) # remove punctuations
#            and (RmvMark==False or not re.match('^[a-z_]$', w)) # remove punctuations
#            and (RmvMark==False or w not in PUNCTUATIONS)
            and (RmvStopWord==False or w not in STOP_WORDS)
            and (not re.match(r'^\d+$', w)) # remove digit
         ]
    return WL

# Usage of the functions
#words_list = jieba.lcut(clean_text(text)) # https://github.com/fxsjy/jieba
#words = clean_words(words_list)

