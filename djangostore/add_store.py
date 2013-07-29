import os
import sys

# banned subdomains
BANNED = ['www',]

if len(sys.argv) == 2:
    with open(os.path.dirname(os.path.abspath(__file__)) + '/stores', 'a+') as file:
        stores = [l.strip() for l in file.readlines()]
        new_store = sys.argv[1]
        if new_store not in stores and new_store not in BANNED:
            file.write(new_store + '\n')
            print 'Created ' + new_store
        else:
            print new_store + ' already exists!'
else:
    print 'Usage: ./add_store.py store_name'