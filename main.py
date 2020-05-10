import search_csv
import time

def main(folder, extension):
    print('\n-----------------------------------------------\n')
    keyword = input('Enter a keyword: ')
    res_numb = input('How many results do you want to see? ')
    start_time = time.time()
    search_csv.threaded_search(keyword, folder, extension, int(res_numb))
    print("\n[%.4f seconds]\n" %(time.time() - start_time))

folder = input('\nEnter the path to the directory that contains your source codes: ')
extension = input('Are your file .sol or .txt? [sol/txt] ')
while True:
    main(folder, extension)
