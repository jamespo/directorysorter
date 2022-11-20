#!/bin/env python

# directorysorter - moves files into subdirectories a-z, [0-9], _others
# useful for game ROMs

from argparse import ArgumentParser
import os

DEBUG = os.getenv('DIRDEBUG')
SQUASH_DIGITS = True


def get_options():
    """return CLI options"""
    parser = ArgumentParser()
    parser.add_argument("-r", help="recursive",
                        dest="recursive", action="store_true")
    parser.add_argument("-d", help="don't squash digits", dest="squash_digits",
                        action="store_false")
    parser.add_argument("-n", help="minimum # of files to cleanup in recursive",
                        dest="min_recur", type=int, default=300)
    parser.set_defaults(recursive=False, squash_digits=True)
    args = parser.parse_args()
    return args


def generate_dirname(filename, squash_digits):
    '''generate directory name'''
    # get first character of filename for dir name
    # ignore leading spaces and make lowercase
    # if non alphanumeric dirname is _others
    cleanchar = filename.strip()[0].lower()
    if cleanchar.isalpha():
        return cleanchar
    elif cleanchar.isdigit():
        if squash_digits:
            return '0-9'
        else:
            return cleanchar
    else:
        return '_others'


def createdir(srcdir, dirname):
    '''create directory dirname'''
    newdir = os.path.join(srcdir, dirname)
    try:
        if DEBUG:
            print('creating dir %s' % newdir)
        else:
            os.mkdir(newdir)
    except FileExistsError:
        # don't worry if dir exists
        pass
    return newdir


def movefile(srcfilepath, destfilepath):
    '''move filename to destdir'''
    # absolute paths required
    if DEBUG:
        print('moving %s to %s' % (srcfilepath, destfilepath))
    else:
        os.rename(srcfilepath, destfilepath)


def cleanup_dir(mydir, squash_digits):
    '''move the files in mydir - returns # moved'''
    filecount = 0
    mydir_obj = os.scandir(mydir)
    for direntry in mydir_obj:
        if direntry.is_file():
            filecount += 1
            direntry_fullpath = os.path.join(mydir, direntry.name)
            newdir = generate_dirname(direntry.name, squash_digits)
            destdir = createdir(mydir, newdir)
            dest_fullpath = os.path.join(destdir, direntry.name)
            movefile(direntry_fullpath, dest_fullpath)
    return filecount


def count_files(mydir):
    '''return # of files in mydir'''
    return len([name for name in os.listdir(mydir)
                if os.path.isfile(os.path.join(mydir, name))])


def find_dirs_to_cleanup(sourcedir, min_recursive_files):
    '''recursively find dirs for later cleanup'''
    dirs_to_clean = []
    for root, dirs, files in os.walk(sourcedir, topdown=False):
        for mydir in dirs:
            # TODO: check if already cleaned up (don't create a/a/a)
            fullpath = os.path.join(root, mydir)
            # check if filecount in dir > min_recursive_files
            numfiles = count_files(fullpath)
            if numfiles >= min_recursive_files:
                dirs_to_clean.append(fullpath)
    # add root if valid
    if count_files(sourcedir) >= min_recursive_files:
        dirs_to_clean.append(sourcedir)
    return dirs_to_clean


def main():
    args = get_options()
    filecount = 0
    sourcedir = os.getcwd()
    if not args.recursive:
        # single dir mode
        filecount = cleanup_dir(sourcedir, args.squash_digits)
        print('%s files moved' % filecount)
    else:
        dirs_to_clean = find_dirs_to_cleanup(sourcedir, args.min_recur)
        for mydir in dirs_to_clean:
            filecount += cleanup_dir(mydir, args.squash_digits)
        print('%s files moved' % filecount)
        print('Directories cleaned:')
        for cleaned_dir in dirs_to_clean:
            print(cleaned_dir)


if __name__ == '__main__':
    main()
