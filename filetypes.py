from collections import namedtuple

MusicFile = namedtuple("MusicFile", ["path", "file"])

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


def getfiletype(f: MusicFile):
    for t in types:
        if f.path.endswith(types[t]["ext"]):
            return t
    return None