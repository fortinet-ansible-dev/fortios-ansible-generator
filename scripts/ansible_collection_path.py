#! /usr/bin/python3
import sys
try:
    import ansible_collections
except:
    sys.exit(1)

for i in ansible_collections.__path__:
    print(i[:-(len('ansible_collections') + 1)], end='')
    break
