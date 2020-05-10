import os, csv, shutil
from concurrent.futures import ThreadPoolExecutor
from search_csv import __to_csv

csv.field_size_limit(100000000)
__owd = os.getcwd()
to_search = []


def creator(word_list, folder):
    global to_search
    reply_list = []
    directory = __owd+os.sep+"cache"
    if not os.path.isdir(directory):
        os.makedirs(directory)

    for w in word_list:
        if w=='':
            continue
        filename=directory+os.sep+w[0]+'.csv'
        try:
            if __in_cache(filename, w):
                reply_list.append(f'"{w}" already in cache.')
            else:
                to_search.append({'keyword': w, 'address_list': list()})
        except OSError as err:
            to_search.append({'keyword': w, 'address_list': list()})

    __threaded_multisearch(folder)
    __write_cache(directory)
    for r in reply_list:
        print(r)


def delete_cache():
    try:
        shutil.rmtree(__owd+os.sep+'cache')
        print('\nCache deleted.')
    except FileNotFoundError as err:
        print('\nNo cache in this folder.')


def __write_cache(directory):
    global to_search

    print('\n')
    for d in to_search:
        filename = directory+os.sep+d['keyword'][0]+'.csv'
        __to_csv(d, filename)
        print(f'"{d["keyword"]}" - {len(d["address_list"])} contracts matching. ')

    to_search=[]


def __threaded_multisearch(folder):
    os.chdir(folder)

    with ThreadPoolExecutor(max_workers=1) as executor:
        for f in os.listdir(folder):
            executor.submit(__search_words, f)


def __search_words(filename):
    global to_search

    with open(filename, encoding='utf8') as f:
        for d in to_search:
            f.seek(0)
            if str(d['keyword']) in f.read():
                d['address_list'].append(filename)



def __in_cache(filename, word):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
    
        for row in reader:
            if row['keyword'] == word:
                return True
        return False