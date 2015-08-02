__author__ = 'Sebastian Schuepbach'

from exifread import process_file
from os import listdir, chmod
from os.path import isfile, isdir, join, splitext
from datetime import datetime
from hashlib import sha1
from shutil import copyfile


def hashfile(fp, hashfun, checksize=65536):
    buf = fp.read(checksize)
    hashfun.update(buf)
    return hashfun.hexdigest()[0:3]


def createfilename(file):
    with (open(file, 'rb')) as f:
        tags = process_file(f, details=False, stop_tag='DateTimeOriginal')
        if 'EXIF DateTimeOriginal' in tags:
            rawdate = str(tags['EXIF DateTimeOriginal'])
            datestr = datetime.strptime(rawdate, '%Y:%m:%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
            filename = datestr + '_' + hashfile(f, sha1()) + '.jpg'
        else:
            filename = False
    return filename


def renameimage(rootpath, targetpath, recursive=False):
    for name in listdir(rootpath):
        file = join(rootpath, name)
        ext = splitext(file)[1].lower()
        if isfile(file) & (ext == '.jpg'):
            filename = createfilename(file)
            if filename:
                targetfile = join(targetpath, filename)
                copyfile(file, targetfile)
                chmod(targetfile, 0o777)
            else:
                print('ERROR: Couldn\'t copy file ' + file + '!')
        elif isdir(file) & recursive:
            renameimage(file, targetpath, recursive)


if __name__ == '__main__':
    renameimage('/home/sebi/Bild', '/home/sebi/testfolder', True)
