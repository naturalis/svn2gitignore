#!/usr/bin/env python
# -*- coding: utf-8 -*-
#test

import sys
import os
import subprocess


def svn_propget_svnignore(path):
    '''fetch the svn:ignore property of given path'''
    p = subprocess.Popen(['svn', 'propget',
                          'svn:ignore', '-R',
                          path], stdout=subprocess.PIPE)
    p.wait()
    data = p.stdout.read().strip()
    return data


def svnignore_to_gitignore(path, data):
    gitignore = path + '/.gitignore'
    if os.path.isfile(gitignore):
        os.rename(gitignore, gitignore + '.orig')
    f = open(gitignore, 'w')

    dirs = data.split('\n\n')

    for dir in dirs:
        subdir = dir.replace(' - ', '\n').replace(path, '').replace(path[:-1], '.').split('\n')
        print subdir
        if subdir[0] == '.':
            for i in subdir[1:]:
                f.write(i + '\n')
        elif subdir[0] == path:
            for i in subdir[1:]:
                print i
                f.write(i + '\n')
        elif subdir[0] == '':
            continue
        else:
            for i in subdir[1:]:
                f.write(subdir[0] + '/' + i + '\n')
    f.close()


def main():
    if len(sys.argv) < 2:
        print 'Usage: %s <repo path>' % sys.argv[0]
        sys.exit()

    for path in sys.argv[1:]:
        dirpath, filename = os.path.split(path)
        svnignore_data = svn_propget_svnignore(dirpath)

    svnignore_to_gitignore(path, svnignore_data)


if __name__ == '__main__':
    main()
