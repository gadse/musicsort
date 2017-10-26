[![Codacy Badge](https://api.codacy.com/project/badge/Grade/10f45a8a26994d7c9a9373e76f73c085)](https://www.codacy.com/app/inbox-github/musicsort?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=gadse/musicsort&amp;utm_campaign=Badge_Grade)

# Warning
This project is still in an infant stage, so use at your own risk. I won't be responsible if this breaks your music collection. And remember: No Backup - No Mercy! ;)

# musicsort
This is a personal project that aims to sort a "bunch of music files" nicely by file type and filter out those with bad quality (low bitrate). I started this because no tool I tried offered such sorting and filtering functionality, not even MusicBrainz Picard. A second-level sorting by artist, album, etc. is not implemented yet, but will follow soon(TM).

## Usage
Just invoke your favourite Python 3 interpreter with `musicsort.py`.
``` bash
$ python musicsort.py
```
If you just want to see how this would sort your stuff - without changing aniything - set the -sim flag to create symlinks instead of moving files.
``` bash
$ python musicsort.py -sim
```

## Parameters
musicsort Currently supports the following optional arguments:

-  **-dir / --directory**:  The directory in which the files are located. Defaults to the directory of musicsort.py.
-  **-out / --output_directory**:  The directory to which the sorted and filtered files should be written. Defaults to "out".
-  **-mbr / --minimum_bitrate**:  The minimum bitrate for lossily-compressed files. Defaults to "0" for disabled filtering.
-  **-bug / --debug**:  Toggles debug output on the console.
-  **-sim / --simulate**: Toogles simulation mode in which no files are changed and symlinks are created instead.

Example:
``` bash
$ python musicsort.py -dir src -out dst -mbr 265
```
