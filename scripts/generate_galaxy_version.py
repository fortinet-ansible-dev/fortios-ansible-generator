#! /usr/bin/python3
import json
import sys

def version_key(version):
    key = ''
    lst = version.split('.')
    for i in lst:
        key += '%2d' % (int(i))
    return key

def main():
    target_version = sys.argv[1]
    versions = None
    with open('galaxy_version.json') as f:
        versions = json.loads(f.read())
    fos_versions = list(versions.keys())
    fos_versions.sort(key=version_key)

    print('| FOS version|Galaxy  Version| Release date|Install Path |')
    print('|----------|:-------------:|:-------------:|:------:|')

    for fos in fos_versions:
        galaxy_versions = list(versions[fos].keys())
        galaxy_versions.sort(key=version_key)
        for galaxy in galaxy_versions:
            if version_key(galaxy) > version_key(target_version):
                continue
            date = versions[fos][galaxy]
            print('|%s|%s %s|%s|`ansible-galaxy collection install fortinet.fortios:%s`|' % (fos, galaxy, '`latest`' if galaxy == galaxy_versions[-1] else '', date, galaxy))
if __name__ == '__main__':
    main()
