import search_csv
import time

def main(folder, extension):
    print('\n-----------------------------------------------\n')
    keyword = input('Enter a keyword: ')
    start_time = time.time()
    search_csv.by_keyword(keyword, folder, extension)
    print("[%s seconds]\n" % (time.time() - start_time))

folder = input('\nEnter the path to the folder that contains your source codes: ')
extension = input('Are your file .sol or .txt? [sol/txt] ')
while True:
    main(folder, extension)
