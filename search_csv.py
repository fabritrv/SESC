import csv
import glob
import os
from concurrent.futures import ThreadPoolExecutor
import json

from parser import get_functions_and_variables_by_address

csv.field_size_limit(100000000)
__address_found = {"keyword": str(""), "address_list": list()}
__owd = os.getcwd()
__fnv = False


def threaded_search(keyword, directory, extension, res_numb, fnv):
    global __address_found
    global __owd
    __address_found["keyword"] = keyword
    global __fnv

    __fnv = fnv

    folder = __owd + os.sep + "cache"
    if not os.path.isdir(folder):
        os.makedirs(folder)
    filename = folder + os.sep + keyword[0] + ".csv"

    try:
        res = __search_csv(keyword, filename)
        if (
            res == None
        ):  # the cache for the letter exist but it doesn't contain the keyword
            __first_search(directory, keyword, res_numb, filename)
        else:
            __addr_printer(res, keyword, res_numb)
        __empty_address_found()
        os.chdir(__owd)
        return
    except OSError:  # the cache for the letter doesn't exist yet
        __first_search(directory, keyword, res_numb, filename)
        __empty_address_found()
        os.chdir(__owd)
        return


def __empty_address_found():
    global __address_found
    __address_found = {"keyword": str(""), "address_list": list()}
    return


def __first_search(directory, keyword, res_numb, filename):
    global __address_found

    print(
        f'It is the first time that you search "{keyword}", this search could take a few minutes...'
    )
    __threader(os.listdir(directory), keyword, directory, res_numb)
    __to_csv(__address_found, filename)
    if len(__address_found["address_list"]) == 0:
        print(
            f'Contracts that contain "{keyword}":\n\nYou should try a better keyword. [0 results found in the directory]'
        )
    else:
        if len(__address_found["address_list"]) < res_numb:
            __addr_printer(
                str(__address_found["address_list"][:res_numb]), keyword, res_numb
            )
        print(
            f'\n[{len(__address_found["address_list"])}] contracts in total matched your search in the directory.'
        )

    return


def __threader(files, keyword, directory, res_numb):
    os.chdir(directory)

    with ThreadPoolExecutor(max_workers=500) as executor:
        for f in files:
            executor.submit(__par_search, f, keyword, res_numb)


def __par_search(file, keyword, res_numb):
    global __address_found

    with open(file, encoding="utf8") as f:
        if str(keyword) in f.read():
            __address_found["address_list"].append(file)
            if len(__address_found["address_list"]) == res_numb:
                __addr_printer(
                    str(__address_found["address_list"][:res_numb]), keyword, res_numb
                )


def __addr_printer(result, keyword, res_numb):
    addr = result.split(",")
    shown = 0
    global __fnv
    res_list = []

    print(f'Contracts that contain "{keyword}":\n')
    if addr[0] == "[]":
        print("You should try a better keyword. [0 results from cache]")
    else:
        for a in addr[:res_numb]:
            address = a.translate(str.maketrans({"[": "", "]": "", "'": "", " ": ""}))
            print(address)
            res_list.append(address)
            if __fnv:
                get_functions_and_variables_by_address(address, __owd)
                print("\n\n")
            shown += 1
        print(f"\n--- {shown} results ---")
    __to_json(res_list, keyword)
    return


def __to_csv(dictionary, filename):

    file_exists = os.path.isfile(filename)

    with open(filename, "a") as file:
        fieldnames = ["keyword", "address_list"]
        w = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            w.writeheader()
        w.writerow(dictionary)

    return


def __search_csv(keyword, filename):

    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["keyword"] == keyword:
                return row["address_list"]

    return


def __to_json(results, keyword):
    global __owd
    layout = {"name": keyword, "children": list()}
    layout["children"].append({"name": "results", "children": list()})
    for r in results:
        layout["children"][0]["children"].append({"name": r, "value": 1})
    folder = __owd + os.sep + "localh" + os.sep + "single_search"
    if not os.path.isdir(folder):
        os.makedirs(folder)
    filename = folder + os.sep + "files" + os.sep + "single_search.json"
    with open(filename, "w+") as fp:
        json.dump(layout, fp, indent=4)
