from collections import namedtuple

import mutagen
from mutagen.mp3 import MP3


MusicFile = namedtuple("MusicFile", ["path", "file", "bitrate"])

types = dict();

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
    for t in types:
        if f.endswith(types[t]["ext"]):
            return t
    return None


def get_file_bitrate(f):
    bitrate = -1
    if f.endswith(types["mp3"]["ext"]):
        bitrate = MP3(f).info.bitrate
    return bitrate