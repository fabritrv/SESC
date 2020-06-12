import os
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
import json

from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

from search_csv import __search_csv, __to_csv
from parser import get_functions_and_variables_by_address

__owd = os.getcwd()
to_search = []
results = []
__keys = ""
__fnv = False


def combined_search(sentence, num_res, folder, fnv):
    global to_search
    global __owd
    global results
    global __keys
    directory = __owd + os.sep + "cache"
    keywords = __sentece_elaborator(sentence)
    found = 0
    key_limit = 5
    global __fnv

    __fnv = fnv

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
        except FileNotFoundError:
            to_search.append({"keyword": k, "address_list": list()})

    if len(to_search) != 0:
        print(
            "Some of your keywords are being searched  for the first time. This search could take a few minutes.."
        )
        __threaded_multisearch_from_dict(folder)
        __write_cache(directory)

    print('Keywords: "' + __keys[:-1] + '"\n')

    for r in __result_elaborator(results, num_res):
        if r != "None":
            found += 1
            print(r)
            if __fnv:
                get_functions_and_variables_by_address(r, __owd)
                print("\n\n")
        if found == num_res:
            break

    __resetter()
    print(f"\n--- {found} contracts ---")
    print("\nA .json of the results was created.")


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


def __result_elaborator(results, num_res):
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

    possible_matches = []
    i = 0
    res = 0
    match = {}
    for x in range(len(to_map), 1, -1):
        for c in combinations(to_map, x):
            s = set.intersection(*map(set, list(c)))
            for contract in s:
                if contract not in to_print:
                    if res <= num_res:
                        if x != i:
                            i = x
                            match = {"name": x, "children": list()}
                            value = __get_size(x)
                        match["children"].append(
                            {"name": contract[:-4], "value": value}
                        )
                        res += 1
                    to_print.append(contract)
        try:
            if possible_matches[-1]["name"] != i:
                possible_matches.append(match)
        except (IndexError, KeyError):
            possible_matches.append(match)
    __to_json(possible_matches)
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


def __to_json(possible_matches):
    global __owd
    global __keys
    key_num = len(__keys[:-1].split("+"))
    for to_remove in list(possible_matches):
        if to_remove == {}:
            possible_matches.remove(to_remove)
        else:
            to_remove["name"] = str((to_remove["name"] * 100) / key_num) + "% matching"
    layout = {"name": __keys[:-1], "children": possible_matches}
    folder = __owd + os.sep + "localh" + os.sep + "search_results"
    if not os.path.isdir(folder):
        os.makedirs(folder)
    filename = folder + os.sep + "files" + os.sep + "search_results.json"
    with open(filename, "w+") as fp:
        json.dump(layout, fp, indent=4)


def __get_size(num_comb):
    if num_comb == 5:
        return 1000
    elif num_comb == 4:
        return 200
    elif num_comb == 3:
        return 10
    elif num_comb == 2:
        return 2
    else:
        return 1
