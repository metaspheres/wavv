from pathlib import Path
from mutagen import File

def scan_folder(folder_path):

    path = Path(folder_path)
    file_list = []

    for file_name in path.rglob('*'): 
        if file_name.is_file() and file_name.suffix in (".mp3", ".flac", ".m4a", ".wav", ".ogg"):
            file_list.append(file_name)

    return file_list

def read_metadata(file_path):
    file = File(file_path)

    def get_tag(key):
        value = file.get(key)
        if value is not None:
            return value[0]

        if hasattr(file, 'tags') and hasattr(file.tags, 'get'):
            id3_map = {
                'artist': 'TPE1',
                'title': 'TIT2',
                'album': 'TALB',
                'albumartist': 'TPE2',
                'tracknumber': 'TRCK',
                'date': 'TDRC',
            }
            id3_key = id3_map.get(key)
            if id3_key:
                value = file.tags.get(id3_key)
                if value is not None:
                    return str(value[0]) if not isinstance(value[0], str) else value[0]
        return None

    try:
        date = int((get_tag('date') or '1980')[:4])
    except (ValueError, TypeError):
        date = 1980

    file_metadata = {
        "Artist": get_tag('artist') or 'Unknown',
        "Album Artist": get_tag('albumartist') or 'Unknown',
        "Title": get_tag('title') or 'Unknown',
        "Album": get_tag('album') or 'Unknown',
        "Track Number": get_tag('tracknumber') or 'Unknown',
        "Date": date,
        "Path": str(file_path)
        }

    return file_metadata

def group_by_album(library):
    album_dict = {}

    for song in library:
        album_name = song["Album"]
        if album_name not in album_dict:
            album_dict[album_name] = []
        album_dict[album_name].append(song)

    return album_dict


def group_by_artist(library):
    artist_list = []

    for artist in library:
        artist_name = artist["Artist"]

        if artist_name not in artist_list:
            artist_list.append(artist_name)

    return artist_list
    
def get_library(folder_path):

    file_list = []

    for file_path in scan_folder(folder_path):
        file_list.append(read_metadata(file_path))
    
    return file_list

def get_directory(directory):
    selected_directory = Path(directory)
    subdir_list = []

    for subdir in selected_directory.iterdir():
        if subdir.is_dir():
            subdir_list.append(str(subdir)) 

    return subdir_list

