# audioinfo

A tool to check audio file durations in a directory.

## Usage

Install the audioinfo package with:

```bash
pip install audioinfo
```

Check the help with:

```bash
$ audioinfo --help

usage: audioinfo [-h] [--directory DIRECTORY] [--ext EXT [EXT ...]] [--recurse] [--case-sensitive]

A tool to check the durations of audio files in a directory.

options:
  -h, --help            show this help message and exit
  --directory DIRECTORY, -d DIRECTORY
                        The directory to search (default: ./)
  --ext EXT [EXT ...], -e EXT [EXT ...]
                        The extension to search for (default: wav)
  --recurse, -r         Recurse into subdirectories (default: True)
  --case-sensitive, -c  Case sensitive search (default: False)
```

## Examples

Check all audio files with the ".wav" in the current directory:

```bash
audioinfo --directory ./ --ext wav
```

The default directory is the current directory and the default extension is ".wav". Therefore you may precisely omit these options, like this:

```bash
audioinfo
```

Check all audio files with the ".wav"  in the directory "~/Music":

```bash
audioinfo --directory ~/Music --ext wav
# or use the short form:
audioinfo -d ~/Music -e wav
```

Check all audio files with ".wav" and ".flac" suffixes in the directory "~/Music":

```bash
audioinfo --directory ~/Music --ext wav flac
```

Check audio files with the ".wav" suffix in the directory "~/Music" and do not recurse into subdirectories:

```bash
audioinfo --directory ~/Music --ext wav --recurse=false
```


## License

This software is licensed under the [MIT License](https://opensource.org/licenses/MIT).
