
# import mutagen

from os import listdir, mkdir
from os.path import isfile, join, abspath
from shutil import copyfile
from filetypes import types, getfiletype
from filetypes import MusicFile as MusicFile
import argparse


def main():
    parser = argparse.ArgumentParser(description="""Sorts and filters a given directory of music 
                                                    files by filetype and bitrate (in case of lossy 
                                                    compression).""")
    parser.add_argument("-dir", "--directory", help="Path to the music files.", default=".")
    #parser.add_argument("-mbr", "--min-bitrate", default="0", help="""The minimum bitrate for 
                                                                      lossyly-compressed files.""",)
    args = parser.parse_args()
    print(args)

    files = dict()
    dir = args.directory + "/test/data"
    files_in_cur_dir = [MusicFile(join(dir, f), f) \
                        for f in listdir(dir) \
                        if isfile(join(dir, f))]
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