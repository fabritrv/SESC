import os
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations

from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

from search_csv import __search_csv, __to_csv

__owd = os.getcwd()
to_search = []
results = []
__keys = ""


def combined_search(sentence, num_res, folder):
    global to_search
    global __owd
    global results
    global __keys
    directory = __owd + os.sep + "cache"
    keywords = __sentece_elaborator(sentence)
    found = 0
    key_limit = 5

    for index, k in enumerate(keywords):
        if index == key_limit:  # take max 5 keywords from the sentence
            break
        try:
            res = __search_csv(k, directory + os.sep + k[0] + ".csv")
            if res == None:
                to_search.append({"keyword": k, "address_list": list()})
            else:
                results.append({"key": k, "result": res})
                __keys += k + "+"
        except FileNotFoundError as err:
            to_search.append({"keyword": k, "address_list": list()})

    if len(to_search) != 0:
        print(
            "Some of your keywords are being searched  for the first time. This search could take a few minutes.."
        )
        __threaded_multisearch_from_dict(folder)
        __write_cache(directory)

    print('Keywords: "' + __keys[:-1] + '"\n')

    for r in __result_elaborator(results):
        if r != "None":
            found += 1
            print(r)
        if found == num_res:
            break

    __resetter()
    print(f"\n--- {found} contracts ---")


def __resetter():
    global results
    global __owd
    global __keys

    results = []
    os.chdir(__owd)
    __keys = ""


def __sentece_elaborator(sentence):
    pos = pos_tag(word_tokenize(sentence))
    keywords = []

    for p in pos:
        if p[1][0] == "N":
            keywords.append(p[0])

    return keywords


def __result_elaborator(results):
    to_map = []
    to_print = []

    for r in results:
        splitted = str(r["result"]).split(",")
        address_list = []
        if splitted != "[]":
            for address in splitted:
                address_list.append(
                    address.translate(
                        str.maketrans({"[": "", "]": "", "'": "", " ": ""})
                    )
                )
            to_map.append(address_list)

    for x in range(len(to_map), 1, -1):
        for c in combinations(to_map, x):
            s = set.intersection(*map(set, list(c)))
            for contract in s:
                if contract not in to_print:
                    to_print.append(contract)

    return to_print


def __threaded_multisearch_from_dict(folder):
    os.chdir(folder)

    with ThreadPoolExecutor(max_workers=500) as executor:
        for f in os.listdir(folder):
            executor.submit(__search_words_from_dict, f)


def __search_words_from_dict(filename):
    global to_search

    with open(filename, encoding="utf8") as f:
        for d in to_search:
            f.seek(0)
            if str(d["keyword"]) in f.read():
                d["address_list"].append(filename)


def __write_cache(directory):
    global to_search
    global results
    global __keys

    for d in to_search:
        filename = directory + os.sep + d["keyword"][0] + ".csv"
        __to_csv(d, filename)
        results.append({"key": d["keyword"], "result": d["address_list"]})
        __keys += d["keyword"] + "+"

    to_search = []
