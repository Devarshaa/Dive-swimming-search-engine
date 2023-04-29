from nltk import wordpunct_tokenize, PorterStemmer
from nltk.corpus import stopwords
from string import punctuation

def tokenize_and_stem(text):
    english_stopwords = stopwords.words("english")
    text = text.lower()
    tokens = wordpunct_tokenize(text)
    tokens = [token for token in tokens if token not in english_stopwords]
    tokens = [token for token in tokens if token not in punctuation]
    stemmer = PorterStemmer()
    stems = [stemmer.stem(token) for token in tokens]
    # # print(len(stems))
    return stems
    # return tokens