from os import listdir, walk, makedirs, symlink
from os.path import isfile, join, abspath
from shutil import copyfile
from typing import List
from filetypes import types, get_file_type, get_file_bitrate
from filetypes import MusicFile as MusicFile
import argparse

MusicFileList = List[MusicFile]


def bitrate_is_valid(bitrate, threshold):
    return bitrate > threshold or bitrate == -1


def main():
    parser = argparse.ArgumentParser(description="""Sorts and filters a given directory of music 
                                                    files by filetype and bitrate (in case of lossy 
                                                    compression).""")
    parser.add_argument("-dir", "--directory", help="Path to the music files.", default=".")
    parser.add_argument("-out", "--output_directory", help="""Path to where the tree of sorted 
                                                              files shall root.""", default="out")
    parser.add_argument("-mbr", "--min_bitrate", default="0", help="""The minimum bitrate (in kBit/s) for 
                                                                      lossily-compressed files.""")
    parser.add_argument("-sim", "--simulate", action="store_true")
    parser.add_argument("-bug", "--debug", action="store_true")
    
    args = parser.parse_args()
    print(args)

    debug = args.debug
    simulate = args.simulate

    input_dir = args.directory
    output_dir = args.output_directory
    all_files = gather_files(input_dir, debug=debug)
    bugprint(all_files, debug)
    music_files = filter_music_files(all_files)
    good_music_files = filter_high_bitrate_music_files(music_files, int(args.min_bitrate))
    sorted_music_files = sort_music_files(good_music_files)
    write_sorted_files(output_dir, sorted_music_files, debug=debug, simulate=simulate, all_files=music_files)


def bugprint(s, debug):
    if debug:
        print(s)


def sort_music_files(files: MusicFileList):
    tree = dict()
    for t in types:
        tree[t] = []
    for file in files:
        file_type = get_file_type(file.path)
        tree[file_type].append(file)
    for t in types:
        if len(tree[t]) == 0:
            del tree[t]
    return tree


def filter_high_bitrate_music_files(files: MusicFileList, min_bitrate):
    return [file for file in files if bitrate_is_valid(file.bitrate, min_bitrate)]


def gather_files(root, debug=False):
    all_files = []
    for (dirpath, dirnames, filenames) in walk(root):
        for name in filenames:
            bugprint(name, debug)
            path_and_name = (join(dirpath, name), name)
            all_files.append(path_and_name)
    return all_files


def filter_music_files(files: list):
    music_files = []
    for file in files:
        path = file[0]
        name = file[1]
        file_type = get_file_type(path)
        if file_type:
            bitrate = get_file_bitrate(path)
            mf = MusicFile(path, name, bitrate)
            music_files.append(mf)
    return music_files


def write_sorted_files(output_dir, files_by_type, debug=False, simulate=False, all_files=None):
    if debug:
        print("*ALL* \t> " + repr(all_files))
    for t in files_by_type:
        final_path = join(output_dir, types[t]["dir"])
        makedirs(final_path)
        copy_file_list(final_path, files_by_type[t])
        bugprint("{} \t> {}".format(final_path, files_by_type[t]), debug)


def copy_file_list(path: str, musicfiles: MusicFileList, simulate=False):
    """Copies a given list of files to the given path (if simulate is False), or creates symlinks instead (if simulate is True)."""
    for mf in musicfiles:
        print("copying to " + join(path, mf.file))
        if simulate:
            copyfile(mf.path, join(path, mf.file))
        else:
            symlink(abspath(mf.path), join(path, mf.file))


if __name__ == '__main__':
    main()