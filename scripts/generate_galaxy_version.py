#! /usr/bin/python3
import json
import sys

def main():
    target_version = sys.argv[1]
    versions = None
    with open('galaxy_version.json') as f:
        versions = json.loads(f.read())
    fos_versions = list(versions.keys())
    fos_versions.sort()

    print('| FOS version|Galaxy  Version| Release date|Install Path |')
    print('|----------|:-------------:|:-------------:|:------:|')

    for fos in fos_versions:
        galaxy_versions = list(versions[fos].keys())
        galaxy_versions.sort()
        for galaxy in galaxy_versions:
            if galaxy > target_version:
                continue
            date = versions[fos][galaxy]
            print('|%s|%s %s|%s|`ansible-galaxy collection install fortinet.fortios:%s`|' % (fos, galaxy, '`latest`' if galaxy == galaxy_versions[-1] else '', date, galaxy))
if __name__ == '__main__':
    main()
