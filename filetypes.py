from collections import namedtuple

import mutagen
from mutagen.mp3 import MP3
from mutagen.mp3 import BitrateMode
from mutagen.oggvorbis import OggVorbis


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


