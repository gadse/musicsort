#!/usr/bin/env python

import logging
import click

from os import walk, makedirs, symlink
from os.path import join, abspath
from shutil import copyfile
from typing import List
from collections import namedtuple

from filetypes import types
from filetypes import get_file_type
from filetypes import get_file_bitrate
from filetypes import get_file_tag
from filetypes import MusicFile

Config = namedtuple("Config", ["input_dir", "output_dir", "simulate", "min_bitrate", "log_mode"])
MusicFileList = List[MusicFile]

logging.basicConfig()
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


def bitrate_is_valid(bitrate, threshold):
    return bitrate > threshold or bitrate == -1


@click.command(
    "Sorts and filters a given directory of music files by "
    "filetype and bitrate (in case of lossy compression)."
)
@click.option("-dir", "--directory", default=".", help="Path to the music files.")
@click.option(
    "-out",
    "--output_directory",
    default="out",
    help="Path to where the tree of sorted files shall root.",
)
@click.option(
    "-mbr",
    "--min_bitrate",
    default="0",
    help="The minimum bitrate (in kBit/s) for lossily-compressed files.",
)
@click.option(
    "-sim",
    "--simulate",
    is_flag=True,
    help="If set, no files are actually moved. Insdead, symlinks are created. Using this option, you can test and see "
         "if the output is to your liking, without possibly time-consuming file operations.",
)
@click.option("-bug", "--debug", is_flag=True, help="Enables gebug mode.")
def main(directory, output_directory, simulate, min_bitrate, debug):
    conf = Config(
        input_dir=directory,
        output_dir=output_directory,
        simulate=simulate,
        min_bitrate=min_bitrate,
        log_mode=logging.DEBUG if debug else logging.INFO
    )
    LOG.info(repr(conf))

    LOG.log(conf.log_mode, "=== FILES IN QUESTION ===")
    all_files = gather_files(conf)
    LOG.log(conf.log_mode, all_files)
    LOG.log(conf.log_mode, "=========")

    music_files = filter_music_files(all_files)
    good_music_files = filter_high_bitrate_music_files(
        files=music_files, min_bitrate=int(conf.min_bitrate)
    )
    sorted_music_files = sort_music_files(good_music_files)
    write_sorted_files(
        conf, sorted_music_files, consider_artist=True, consider_album=True
    )


def make_parser():
    return None


def make_config(args):
    if args.debug:
        log_mode = logging.DEBUG
    else:
        log_mode = logging.INFO
    return Config(
        args.directory, args.output_directory, simulate=args.simulate, log_mode=log_mode
    )


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
    return [file for file in files if bitrate_is_valid(file.bitrate, min_bitrate)]


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


def write_sorted_files(
    conf: Config, files_by_type, consider_artist=False, consider_album=False
):
    for t in files_by_type:
        path = join(conf.output_dir, types[t]["dir"])

        copy_file_list(path, files_by_type[t], consider_artist, consider_album)
        LOG.log(conf.log_mode, "{} \t> {}".format(path, files_by_type[t]))


def copy_file_list(
    path: str,
    musicfiles: MusicFileList,
    simulate=False,
    consider_artist=False,
    consider_album=False,
):
    """Copies a given list of files to the given path (if simulate is False),
    or creates symlinks instead (if simulate is True)."""
    for mf in musicfiles:
        print(">>>>>" + repr(mf.tag))
        if consider_artist:
            path = join(path, mf.tag.artist)
        if consider_album:
            path = join(path, mf.tag.album)
        try:
            makedirs(path)
        except FileExistsError:
            LOG.debug(f"skipping existing directory: {path}")
        try:
            if simulate:
                copyfile(mf.path, join(path, mf.file))
            else:
                symlink(abspath(mf.path), join(path, mf.file))
        except FileExistsError:
            LOG.debug(f"skipping existing file: {mf.file}")


if __name__ == "__main__":
    main()
