__author__ = 'Sebastian Schuepbach'

from os import listdir, remove
from os.path import join, splitext, isfile, isdir, getsize


def findsimilar(rootpath, recursive=False):
    f = dict()
    for name in listdir(rootpath):
        file = join(rootpath, name)
        trunk, ext = splitext(file)
        if isfile(file) & (ext.lower() == '.jpg'):
            if trunk in f:
                originfile = trunk + f[trunk]
                keypress = None
                while keypress not in (0, 1, 2):
                    print("Similar file for " + file + " found! What should be done?")
                    print("[1] Delete original file: " + originfile + " (" + str(getsize(originfile)) + " Bytes)")
                    print("[2] Delete new found file: " + file + " (" + str(getsize(file)) + " Bytes)")
                    print("[0] Nothing")
                    keypress = int(input("Press number and hit return."))
                    if keypress == 1:
                        remove(originfile)
                        f[trunk] = ext
                    elif keypress == 2:
                        remove(file)
            else:
                f[trunk] = ext
        elif isdir(file) & recursive:
            f.update(findsimilar(file, recursive))
    return f

if __name__ == '__main__':
    findsimilar('/home/sebi/testfolder', True)
