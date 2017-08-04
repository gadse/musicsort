
# import mutagen

from os import listdir, mkdir
from os.path import isfile, join, abspath
from shutil import copyfile
from collections import namedtuple

MP3_SUFFIX = ".mp3"
OGG_SUFFIX = ".ogg"
FLAC_SUFFIX = ".flac"

MusicFile = namedtuple("MusicFile", ["path", "file"])


def main():
    # Arrays of MusicFiles
    mp3_files = []
    flac_files = []
    ogg_files = []
    # Contains MusicFile namedtuples (path, file)
    files_in_cur_dir = [MusicFile(join("test/data", f), f) \
                        for f in listdir("test/data") \
                        if isfile(join("test/data", f))]
    for mf in files_in_cur_dir:
        if is_mp3(mf):
            mp3_files.append(mf)
        if is_flac(mf):
            flac_files.append(mf)
        if is_ogg(mf):
            ogg_files.append(mf)
    print("MP3 >\t" + repr(mp3_files))
    print("FLAC >\t" + repr(flac_files))
    print("OGG >\t" + repr(ogg_files))
    print("* >\t" + repr(files_in_cur_dir))
    mkdir("MP3")
    mkdir("FLAC")
    mkdir("OGG")
    copy_file_list("MP3", mp3_files)
    copy_file_list("FLAC", flac_files)
    copy_file_list("OGG", ogg_files)


def copy_file_list(path, musicfiles):
    """Copies a given list of files to the given path."""
    for mf in musicfiles:
        print("copying to " + join(path, mf.file))
        copyfile(mf.path, join(path, mf.file))


def is_mp3(f: MusicFile):
    return f.path.endswith(MP3_SUFFIX)


def is_flac(f: MusicFile):
    return f.path.endswith(FLAC_SUFFIX)


def is_ogg(f: MusicFile):
    return f.path.endswith(OGG_SUFFIX)


if __name__ == '__main__':
    main()