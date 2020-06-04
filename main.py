import time

from parser import get_functions_and_variables, get_functions_and_variables_by_address
from cache_creator import creator, delete_cache
from search_csv import threaded_search
from sentence_search import combined_search
from graph import create


def main(folder, extension):
    print("\nActions:")
    print("0 ---> Create graph")
    print("1 ---> Create cache")
    print("2 ---> Search by keyword")
    print("3 ---> Search by sentence")
    print("4 ---> Delete cache")
    print("5 ---> Get functions and variables for each contract")
    print("6 ---> Get functions and variables for a single contract")
    print("7 ---> Exit")
    operation = input("What do you want to do? [0/1/2/3/4/5/6/7] ")

    if int(operation) == 1:
        word_list = []
        print(
            "\nIn order to create a cache you will be asked to enter 20 keywords of your choice that represent topics you might search in the future."
        )
        print(
            "Cache creation might take several minutes but it will speed up your search significantly."
        )
        print(
            "Feel free to repeat this operation as many times as you like to expand your cache size.\n"
        )
        for x in range(20):
            word = input(f"Enter keyword number {x+1}: ")
            word_list.append(word)
        start_time = time.time()
        creator(word_list, folder)
        print("\n[%.4f seconds]\n" % (time.time() - start_time))
    elif int(operation) == 2:
        print("\n-----------------------------------------------\n")
        keyword = input("Enter a keyword: ")
        res_numb = input("How many results do you want to see? ")
        fnv = input(
            "Do you want to see functions and variables for the contracts that match your search? [y/n] "
        )
        if fnv == "y":
            param = True
        else:
            param = False
        start_time = time.time()
        threaded_search(keyword, folder, extension, int(res_numb), param)
        print("\n[%.4f seconds]\n" % (time.time() - start_time))
    elif int(operation) == 3:
        print("\n-----------------------------------------------\n")
        sentence = input("Enter a short sentence: ")
        num_res = input("How many results do you want to see? ")
        fnv = input(
            "Do you want to see functions and variables for the contracts that match your search? [y/n] "
        )
        if fnv == "y":
            param = True
        else:
            param = False
        start_time = time.time()
        combined_search(sentence, int(num_res), folder, param)
        print("\n[%.4f seconds]\n" % (time.time() - start_time))
    elif int(operation) == 4:
        delete_cache()
    elif int(operation) == 5:
        start_time = time.time()
        print("\nOk, this could take some time..")
        get_functions_and_variables(folder)
        print("\n[%.4f seconds]\n" % (time.time() - start_time))
    elif int(operation) == 6:
        address = input("Insert address: ")
        start_time = time.time()
        get_functions_and_variables_by_address(address)
        print("\n[%.4f seconds]\n" % (time.time() - start_time))
    elif int(operation) == 7:
        raise SystemExit
    elif int(operation) == 0:
        address = input("Please enter a contract (eg. 'address.sol'): ")
        print("Creating the graph...")
        start_time = time.time()
        create(address)
        print("\n[%.4f seconds]\n" % (time.time() - start_time))
    else:
        print("Please enter a valid number.")


folder = input("\nEnter the path to the directory that contains your source codes: ")
extension = input("Are your file .sol or .txt? [sol/txt] ")
while True:
    main(folder, extension)
