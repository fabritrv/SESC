import search_csv, cache_creator
import time

def main(folder, extension):
    print('\nActions:\n1 ---> Create cache\n2 ---> Search by keyword\n3 ---> Delete cache')
    operation = input('What do you want to do? [1/2/3] ')

    if int(operation)==1:
        word_list = []
        print('\nIn order to create a cache you will be asked to enter 20 keywords of your choice that represent topics you might search in the future.')
        print('Cache creation might take several minutes but it will speed up your search significantly.')
        print('Feel free to repeat this operation as many times as you like to expand your cache size.\n')
        for x in range(20):
            word = input(f'Enter keyword number {x+1}: ')
            word_list.append(word)
        start_time = time.time()
        cache_creator.creator(word_list, folder)
        print("\n[%.4f seconds]\n" %(time.time() - start_time))
    elif int(operation)==2:
        print('\n-----------------------------------------------\n')
        keyword = input('Enter a keyword: ')
        res_numb = input('How many results do you want to see? ')
        start_time = time.time()
        search_csv.threaded_search(keyword, folder, extension, int(res_numb))
        print("\n[%.4f seconds]\n" %(time.time() - start_time))
    elif int(operation)==3:
        cache_creator.delete_cache()
    else:
        print('Please enter a valid number.')


folder = input('\nEnter the path to the directory that contains your source codes: ')
extension = input('Are your file .sol or .txt? [sol/txt] ')
while True:
    main(folder, extension)
