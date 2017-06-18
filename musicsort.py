# import mutagen

from os import listdir, mkdir
from os.path import isfile, join, abspath
from shutil import copyfile

MP3_SUFFIX = ".mp3"
FLAC_SUFFIX = ".flac"


def main():
    print("hello!")
    mp3_files = []
    flac_files = []
    files_in_cur_dir = [(join("test/data", f), f) for f in listdir("test/data") if isfile(join("test/data", f))]
    for f in files_in_cur_dir:
        if is_mp3(f[0]):
            mp3_files.append(f)
        if is_flac(f[0]):
            flac_files.append(f)
    print("MP3 >\t" + repr(mp3_files))
    print("FLAC >\t" + repr(flac_files))
    print("* >\t" + repr(files_in_cur_dir))
    mkdir("MP3")
    mkdir("FLAC")
    copy_file_list("MP3", mp3_files)
    copy_file_list("FLAC", flac_files)

def copy_file_list(path, files):
    """Copies a given list of files to the given path."""
    for f in files:
        print("copying to " + join(path, f[1]))
        copyfile(f[0], join(path, f[1]))

def is_mp3(file):
    return file.endswith(MP3_SUFFIX)


def is_flac(file):
    return file.endswith(FLAC_SUFFIX)

if __name__ == '__main__':
    main()