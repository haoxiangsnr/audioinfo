import argparse
import glob
import os
from typing import Optional, Union

import soundfile as sf
from rich.progress import track


def __get_files(dir_name: str, extensions: Union[list[str], set[str]]) -> set[str]:
    """Helper function to get files in a single directory"""

    # Expand out the directory
    dir_name = os.path.abspath(os.path.expanduser(dir_name))

    files = set()

    for sub_ext in extensions:
        globstr = os.path.join(dir_name, "*" + os.path.extsep + sub_ext)
        files |= set(glob.glob(globstr))

    return files


def find_files(
    directory: str,
    ext: Optional[Union[list, set]] = None,
    recurse: Optional[bool] = True,
    case_sensitive: Optional[bool] = False,
) -> list[str]:
    """
    Find files in a directory.

    Args:
        directory (str): The directory to search.
        ext (str): The extension to search for.
        recurse (bool): Whether to recurse into subdirectories.
        case_sensitive (bool): Whether to do a case sensitive search.
    """
    if ext is None:
        ext = ["aac", "au", "flac", "m4a", "mp3", "ogg", "wav"]

    elif isinstance(ext, str):
        ext = [ext]

    # Cast into a set
    ext = set(ext)

    # Generate upper-case versions
    if not case_sensitive:
        # Force to lower-case
        ext = set([e.lower() for e in ext])
        # Add in upper-case versions
        ext |= set([e.upper() for e in ext])

    files = set()

    if recurse:
        for walk in os.walk(directory):
            files |= __get_files(walk[0], ext)
    else:
        files = __get_files(directory, ext)

    files = list(files)
    files.sort()
    return files


def duration_str(duration) -> str:
    hours, rest = divmod(duration, 3600)
    minutes, seconds = divmod(rest, 60)
    if hours >= 1:
        duration = f"{hours:.0f}h {minutes:.0f}min {seconds:.3f}s"
    elif minutes >= 1:
        duration = "{0:02.0g}:{1:05.3f} min".format(minutes, seconds)
    else:
        duration = f"{seconds:.2f}s"
    return duration


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="audioinfo", description="A tool to check audio file durations in a directory."
    )
    parser.add_argument(
        "--directory",
        "-d",
        help="The directory to search",
    )
    parser.add_argument(
        "--ext",
        "-e",
        nargs="+",
        default="wav",
        help="The extension to search for",
    )
    parser.add_argument(
        "--recurse",
        "-r",
        default=True,
        action="store_true",
        help="Recurse into subdirectories",
    )
    parser.add_argument(
        "--case-sensitive",
        "-c",
        default=False,
        action="store_true",
        help="Case sensitive search",
    )
    args = parser.parse_args()

    print("Searching for files...")
    files = find_files(args.directory, args.ext, args.recurse, args.case_sensitive)
    print(f"Finished searching for {len(files)} files.")

    if len(files) == 0:
        print(f"No files found in {args.directory}, please check your arguments.")
        return

    total_duration = 0.0
    for file in track(files, description="Analyzing files:"):
        with sf.SoundFile(file) as f:
            name = f.name
            samplerate = f.samplerate
            channels = f.channels
            frames = f.frames
            duration = float(frames) / f.samplerate
            format = f.format

            print(
                f"{name} - {samplerate} - {format} - # channels: {channels}, duration: {duration:.3f}s"
            )

            total_duration += duration

    print(f"Total number of files: {len(files)}.")
    print(f"Total duration: {duration_str(total_duration)}.")
    print(f"Average duration: {duration_str(total_duration / len(files))}.")
