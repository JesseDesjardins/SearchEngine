# Import libraries
import re
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag

symbols = [':', ';', '(', ')', '!', '?', '...', ',', '.', '-', '\'', '\"', '\\', '/']
""" List of symbols """             

def tokenize(text):
    sentences = []
    for sentence in sent_tokenize(text):
        sentences.append(word_tokenize(sentence))
    return [token for sentence in sentences for token in sentence]

def case_fold(tokens):
    return [token.lower() for token in tokens]

def remove_stopwords(tokens):
   return [token for token in tokens if token not in set(stopwords.words('english'))]

def normalize(tokens):
    for symbol in symbols:
        tokens = [token.replace(symbol, '') for token in tokens]
    return [token for token in tokens if token!='']

def stem(tokens):
    stemmer = PorterStemmer()
    return list(dict.fromkeys([stemmer.stem(token) for token in tokens])) # Removes possible duplicates after stemming

# lemmatize method inpired by https://stackoverflow.com/a/15590384/3943418
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