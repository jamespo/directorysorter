#!/bin/env python

# directorysorter - moves files into subdirectories a-z, [0-9], _others
# useful for game ROMs

import os

DEBUG = os.getenv('DIRDEBUG')
SQUASH_DIGITS = True

def generate_dirname(filename):
    '''generate directory name'''
    # get first character of filename for dir name
    # ignore leading spaces and make lowercase
    # if non alphanumeric dirname is _others
    cleanchar = filename.strip()[0].lower()
    if cleanchar.isalpha():
        return cleanchar
    elif cleanchar.isdigit():
        if SQUASH_DIGITS:
            return '0-9'
        else:
            return cleanchar
    else:
        return '_others'


def createdir(dirname):
    '''create directory dirname'''
    try:
        if DEBUG:
            print('creating dir %s' % dirname)
        else:
            os.mkdir(dirname)
    except FileExistsError:
        # don't worry if dir exists
        pass
    return dirname


def movefile(srcfilepath, destfilepath):
    '''move filename to destdir'''
    # absolute paths required
    if DEBUG:
        print('moving %s to %s' % (srcfilepath, destfilepath))
    else:
        os.rename(srcfilepath, destfilepath)


def main():
    filecount = 0
    sourcedir = os.getcwd()
    mydir = os.scandir(sourcedir)
    for direntry in mydir:
        if direntry.is_file():
            filecount += 1
            newdir = createdir(generate_dirname(direntry.name))
            srcpath = os.path.join(sourcedir, direntry.name)
            destpath = os.path.join(sourcedir, newdir, direntry.name)
            movefile(srcpath, destpath)
    print('%s files moved' % filecount)


if __name__ == '__main__':
    main()
