
# import mutagen

from os import listdir, mkdir
from os.path import isfile, join, abspath
from shutil import copyfile
from filetypes import types, getfiletype
from filetypes import MusicFile as MusicFile


def main():
    files = dict()
    files_in_cur_dir = [MusicFile(join("test/data", f), f) \
                        for f in listdir("test/data") \
                        if isfile(join("test/data", f))]
    for mf in files_in_cur_dir:
        filetype = getfiletype(mf)
        if filetype is not None:
            filelist = files.get(filetype, None)
            if filelist is None:
                files[filetype] = []
            files[filetype].append(mf)
            
    print("MP3 >\t" + repr(files["mp3"]))
    print("FLAC >\t" + repr(files["flac"]))
    print("* >\t" + repr(files_in_cur_dir))
    for t in files:
        mkdir(types[t]["dir"])
    copy_file_list("MP3", files["mp3"])
    copy_file_list("FLAC", files["flac"])


def copy_file_list(path, musicfiles):
    """Copies a given list of files to the given path."""
    for mf in musicfiles:
        print("copying to " + join(path, mf.file))
        copyfile(mf.path, join(path, mf.file))


if __name__ == '__main__':
    main()