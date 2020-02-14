# Import libraries
import re
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
#from nltk import download

# NLTK stopwords list added manually because of error with the download comman
stopwords = {'you', 'yourselves', 'she', 'because', 'not', 'more', 'won',
    'we', 'do', 'them', 'how', 'there', "hasn't", "don't", 'as', 'of', 'being',
    'can', 'my', "should've", 'very', 'isn', 'ours', 'once', 'during', 'above',
    'on', 'after', 'with', 'for', 'before', 'o', 'mustn', 'he', 'have', 'both',
    'who', 'haven', 'down', "weren't", "that'll", 'myself', 'that', 'below',
    'by', 'then', 'if', 'does', "mustn't", 'further', 'had', "doesn't", 'few',
    "it's", 'whom', 'y', 'having', 'his', 't', 'they', 're', 'needn', 'am',
    'll', 'against', "you're", 'were', 'in', "you'll", "shouldn't", 'her',
    'only', 'each', 'its', 'at', 'd', "couldn't", 'shouldn', "hadn't", 'what',
    'now', 'again', 'when', 'been', 'i', 'your', 'which', "won't", 'a', 'yours',
    'theirs', 'aren', 'but', 'it', 'this', 'most', "shan't", 'are', 'the', 'him',
    'wasn', 'while', 'an', 'mightn', 'yourself', 'out', 'such', 'nor', "didn't",
    'off', 'from', 'why', 'all', "wouldn't", 'into', 'under', 'any', 'and',
    'doesn', 'to', 's', 'was', 'up', 'just', "needn't", "she's", 'didn', 'own',
    'so', 'has', 'until', 'wouldn', 'themselves', 'is', 'about', 'should', 've',
    'hers', 'too', 'hasn', "mightn't", 'through', 'shan', 'these', 'between',
    'weren', 'no', 'doing', 'or', 'hadn', 'over', 'where', 'some', 'will', 'their',
    "you've", 'did', 'me', 'our', 'itself', 'himself', 'those', 'don', 'couldn',
    'other', 'be', 'than', 'm', "isn't", 'ourselves', 'here', "wasn't", 'ain',
    'same', "you'd", "aren't", 'ma', "haven't", 'herself'}
""" NLTK Stopwords list """

symbols = ['!', '?', '...', ',', '.', '-', '\'', '\"']
""" List of symbols """             

def tokenize(text):
    sentences = []
    for sentence in sent_tokenize(text):
        sentences.append(word_tokenize(sentence))
    return [token for sentence in sentences for token in sentence]

def case_fold(tokens):
    return [token.lower() for token in tokens]

def remove_stopwords(tokens):
   return [token for token in tokens if token not in stopwords]

def normalize(tokens):
    for symbol in symbols:
        tokens = [token.replace(symbol, '') for token in tokens]
    return [token for token in tokens if token!='']

def stem(tokens):
    stemmer = PorterStemmer()
    return list(dict.fromkeys([stemmer.stem(token) for token in tokens])) # Removes possible duplicates after stemming

def lemmatize(tokens):    
    lemmatizer = WordNetLemmatizer()
    tagged_tokens = pos_tag(tokens)
    tagged_tokens = [(token[0], _tag_to_wordnet(token[1])) for token in tagged_tokens]
    lemmatized_tokens = []
    for token, tag in tagged_tokens:
        if tag is None:
            lemmatized_tokens.append(token)
        else:
            lemmatized_tokens.append(lemmatizer.lemmatize(token, tag))
    return list(dict.fromkeys(lemmatized_tokens)) # Removes possible duplicates after stemming

def _tag_to_wordnet(tag):
    """ Helper function for lemmatize """
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:          
        return None