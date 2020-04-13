from nltk.corpus import wordnet
import operator
from collections import defaultdict

def query_expansion_wordnet(query, rm):
    """ returns a suitable expanded query, if there is one """

    bool_terms = ['AND_NOT', 'AND', 'OR_NOT', 'OR', 'NOT', '(', ')']
    expanded_query = ''

    if rm == "bool":
        query_terms = query.split()
        search_terms = [term for term in query_terms if term not in bool_terms] # remove boolean terms
        for term in search_terms: # Strip off brakets
            if term[0] == '(' : term = term[1:]
            if term[-1] == ')' : term = term[:-1]
            # Find synonyms of term
            synonyms = []
            for synset in wordnet.synsets(term):
                for lemma in synset.lemmas():
                    synonyms.append(lemma.name())    # add the synonyms
            synDict = {} # key will be synonym, value will be similarity score
            for word in [word for word in list(dict.fromkeys(synonyms)) if word != term]: # removes duplicates
                sim_score = wordnet.synset(wordnet.synsets(term)[0].name()).wup_similarity(wordnet.synset(wordnet.synsets(word)[0].name()))
                synDict[word] = sim_score if sim_score != None else 0
            best_syn = (max(synDict.items(), key=operator.itemgetter(1))[0] if synDict else None)
            if best_syn != None and synDict[best_syn] >= 0.5: # if match is less than 0.5 don't expand
                expanded_query = query.replace(term, "(" + term + " OR " + best_syn + ")", 1)

    elif rm == "vsm":
        # TODO Implement VSM expansion
        None
    else:
        None
    return expanded_query


if __name__ == "__main__":
    print(query_expansion_wordnet("(travel) OR sad", "bool"))