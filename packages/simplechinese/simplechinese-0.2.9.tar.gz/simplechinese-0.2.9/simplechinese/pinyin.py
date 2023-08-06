import simplepinyin as sp

lm = sp.Languagle_Model()

def str2pinyin(words, hasTone=False):
    return lm.translate_c2p(words, hasTone=hasTone)

def pinyin2str(pinyins):
    return lm.translate_p2c(words.strip().split())
