from os import walk, makedirs, symlink
from os.path import join, abspath
from shutil import copyfile
from typing import List
from filetypes import types
from filetypes import get_file_type
from filetypes import get_file_bitrate
from filetypes import get_file_tag
from filetypes import MusicFile
import argparse
import logging

logging.basicConfig()

MusicFileList = List[MusicFile]

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class Config(object):
    """This class is meant to hold all configuration settings."""

    def __init__(self, input_dir, output_dir, simulate=True, log_mode=logging.INFO):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.simulate = simulate
        self.log_mode = log_mode

    def __repr__(self):
        representation = {
            "input_dir": self.input_dir,
            "output_dir": self.output_dir,
            "simulate": self.simulate,
            "log_mode": self.log_mode
        }
        return repr(representation)


def bitrate_is_valid(bitrate, threshold):
    return bitrate > threshold or bitrate == -1


def main():
    args = make_parser().parse_args()
    LOG.debug(args)

    conf = make_config(args)
    LOG.info(repr(conf))

    LOG.log(conf.log_mode, "=== FILES IN QUESTION ===")
    all_files = gather_files(conf)
    LOG.log(conf.log_mode, all_files)
    LOG.log(conf.log_mode, "=========")

    music_files = filter_music_files(all_files)
    good_music_files = filter_high_bitrate_music_files(
        files=music_files,
        min_bitrate=int(args.min_bitrate)
    )
    sorted_music_files = sort_music_files(good_music_files)
    write_sorted_files(conf, sorted_music_files)


def make_parser():
    parser = argparse.ArgumentParser(
        description="Sorts and filters a given directory of music files by "
                    "filetype and bitrate (in case of lossy compression)."
    )
    parser.add_argument(
        "-dir",
        "--directory",
        help="Path to the music files.",
        default="."
    )
    parser.add_argument(
        "-out",
        "--output_directory",
        help="Path to where the tree of sorted files shall root.",
        default="out"
    )
    parser.add_argument(
        "-mbr",
        "--min_bitrate",
        default="0",
        help="The minimum bitrate (in kBit/s) for lossily-compressed files."
    )
    parser.add_argument(
        "-sim",
        "--simulate",
        action="store_true"
    )
    parser.add_argument(
        "-bug",
        "--debug",
        action="store_true"
    )
    return parser


def make_config(args):
    if args.debug:
        log_mode = logging.DEBUG
    else:
        log_mode = logging.INFO
    return Config(args.directory, args.output_directory, simulate=args.simulate, log_mode=log_mode)


def gather_files(conf):
    all_files = []
    for (dirpath, _, filenames) in walk(conf.input_dir):
        for name in filenames:
            if get_file_type(join(dirpath, name)):
                LOG.log(conf.log_mode, name)
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
            tag = get_file_tag(path)
            mf = MusicFile(path, name, bitrate, tag)
            music_files.append(mf)
    return music_files


def filter_high_bitrate_music_files(files: MusicFileList, min_bitrate):
    return [file for file
            in files
            if bitrate_is_valid(file.bitrate, min_bitrate)]


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


def write_sorted_files(conf: Config, files_by_type):
    for t in files_by_type:
        type_path = join(conf.output_dir, types[t]["dir"])
        try:
            makedirs(type_path)
        except FileExistsError:
            LOG.debug(f"skipping existing directory: {type_path}")
        copy_file_list(type_path, files_by_type[t])
        LOG.log(conf.log_mode, "{} \t> {}".format(type_path, files_by_type[t]))


def copy_file_list(path: str, musicfiles: MusicFileList, simulate=False):
    """Copies a given list of files to the given path (if simulate is False),
    or creates symlinks instead (if simulate is True)."""
    for mf in musicfiles:
        try:
            if simulate:
                copyfile(mf.path, join(path, mf.file))
            else:
                symlink(abspath(mf.path), join(path, mf.file))
        except FileExistsError:
            LOG.debug(f"skipping existing file: {mf.file}")

if __name__ == "__main__":
    main()
