import os
from itertools import combinations

from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

from search_csv import __search_csv


def combined_search(sentence, num_res):
    directory = os.getcwd()+os.sep+"cache"
    keywords = __sentece_elaborator(sentence)
    results = []
    found = 0
    keys = ''
    key_limit = 5

    for index,k in enumerate(keywords):
        if index == key_limit:  #take max 5 keywords from the sentence
            break
        try:
            results.append({'key': k, 'result': __search_csv(k, directory+os.sep+k[0]+'.csv')})
            keys += k+'+'
        except FileNotFoundError as err:
            key_limit += 6  #ignores keywords that don't have a file with their initials in memory
            continue
    
    print('Keywords: "'+keys[:-1]+'"\n')

    for r in __result_elaborator(results):
        if r != 'None':
            found += 1
            print(r)
        if found==num_res:
            break
    print(f'\n--- {found} contracts ---')
        

def __sentece_elaborator(sentence):
    pos = pos_tag(word_tokenize(sentence))
    keywords = []

    for p in pos:
        if p[1][0]=='N':
            keywords.append(p[0])
    
    return keywords


def __result_elaborator(results):
    to_map = []
    to_print = []

    for r in results:
        splitted = str(r['result']).split(',')
        address_list=[]
        if splitted!='[]':
            for address in splitted:
                address_list.append(address.translate(str.maketrans({'[': '', ']': '', "'": '', " ":''})))
            to_map.append(address_list)

    for x in range (len(to_map),1,-1):
        for c in combinations(to_map,x):
            s = set.intersection(*map(set, list(c)))
            for contract in s:
                if contract not in to_print:
                    to_print.append(contract)
        
    return to_print
