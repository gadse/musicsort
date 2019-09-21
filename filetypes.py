from collections import namedtuple

from mutagen.mp3 import MP3
from mutagen.mp3 import BitrateMode
from mutagen.oggvorbis import OggVorbis
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC

MusicTag = namedtuple(
    "MusicTag",
    ["title", "title_number", "album", "artist", "album_artist"]
)
MusicFile = namedtuple(
    "MusicFile",
    ["path", "file", "bitrate", "tag"]
)

types = dict()

types["mp3"] = dict()
types["mp3"]["ext"] = ".mp3"
types["mp3"]["dir"] = "MP3"

types["flac"] = dict()
types["flac"]["ext"] = ".flac"
types["flac"]["dir"] = "FLAC"

types["ogg"] = dict()
types["ogg"]["ext"] = ".ogg"
types["ogg"]["dir"] = "OGG"


def get_file_type(f: str):
    out_type = None

    for t in types:
        if f.endswith(types[t]["ext"]):
            out_type = t
    return out_type


def get_file_bitrate(f):
    bitrate = -1

    if f.endswith(types["mp3"]["ext"]):
        bitrate_mode = MP3(f).info.bitrate_mode
        if bitrate_mode == BitrateMode.VBR:
            bitrate = -1
        else:
            bitrate = MP3(f).info.bitrate

    elif f.endswith(types["ogg"]["ext"]):
        bitrate = OggVorbis(f).info.bitrate

    return bitrate


def get_file_tag(f):
    system_tag = None

    if f.endswith(types["mp3"]["ext"]):
        system_tag = EasyID3(f)
    elif f.endswith(types["flac"]["ext"]):
        system_tag = FLAC(f)
    elif f.endswith(types["ogg"]["ext"]):
        system_tag = OggVorbis(f)

    out_tag = MusicTag(
        title=system_tag["title"][0],
        title_number=system_tag["tracknumber"][0],
        album=system_tag["album"][0],
        artist=system_tag["artist"][0],
        album_artist=system_tag["albumartist"][0]
    )
    return out_tag
