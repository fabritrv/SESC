import os
import glob
import csv

csv.field_size_limit(100000000)

def by_keyword(keyword, directory, extension):

    folder = os.getcwd()+"\\cache\\"
    if not os.path.isdir(folder):
        os.makedirs(folder)
    filename=folder+keyword[0]+'.csv'
    
    try:
        res = __search_csv(keyword, filename)
        if res == None: #the cache for the letter exists but the word hasn't been searched yet
            __write(keyword, directory, extension, filename)
        else:
            addr = res.split(',')
            print(f'Contracts that contain "{keyword}":\n')   
            if addr[0]=='[]':
                print('You should try a better keyword. [0 results]')
            else:
                for a in addr:
                    print(a.translate(str.maketrans({'[': '', ']': '', "'": '', " ":''})))
                print(f'\n[{len(addr)} results]') 
        return    
    except OSError as err:  #the cache for the letter doesn't exist yet
        __write(keyword, directory, extension, filename)
        return


def __to_csv(dictionary, filename):

    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a') as file:
        fieldnames = ['keyword', 'address_list']
        w = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            w.writeheader()
        w.writerow(dictionary)
    
    return


def __search_csv(keyword, filename):

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
    
        for row in reader:
            if row['keyword'] == keyword:
                return(row['address_list'])
    
    return
    


def __write(keyword, directory, extension, filename):

    address_dict = {'keyword': str(keyword), 'address_list': list()}
    found = 0
    owd = os.getcwd()
    os.chdir(directory)

    for file in glob.glob("*."+extension):
        with open(os.path.join(os.getcwd(), file), encoding="utf8") as f:
            if str(keyword) in f.read():
                address_dict['address_list'].append(file)
                found += 1

    os.chdir(owd)
    __to_csv(address_dict, filename)

    print(f'Contracts that contain "{keyword}":\n')
    for addr in address_dict['address_list']:
        print(addr)
    print(f'\n[{len(address_dict["address_list"])} results]')
    return
