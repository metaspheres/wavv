from main import app
from flask import render_template, request, redirect, url_for, jsonify, session
from mutagen import File as MutagenFile
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK, TDRC
from models import *

@app.route("/")

def homepage():
    folder_path = session.get('folder_path')

    if not folder_path:
        return render_template("homepage.html", data=[], albums={}, artists=[])

    library = get_library(folder_path)
    albums = group_by_album(library)
    artists = group_by_artist(library)
    return render_template("homepage.html", data=library, albums=albums, artists=artists)

@app.route("/edit", methods=["GET", "POST"])

def edit():
    path = request.args.get('path')
    song_data = read_metadata(path)

    return render_template("edit.html", song=song_data)

@app.route("/save", methods=["POST"])

def save():
    path = request.form.get('path')
    artist = request.form.get('artist')
    title = request.form.get('title')
    album = request.form.get('album')
    tracknumber = request.form.get('track-number')
    date = request.form.get('date')

    file = MutagenFile(path)

    if file.tags is None:
        file.add_tags()

    if hasattr(file, 'tags') and hasattr(file.tags, '__setitem__'):
        # MP3 uses ID3 tags
        if path.lower().endswith('.mp3'):
            file.tags['TPE1'] = TPE1(encoding=3, text=[artist])
            file.tags['TIT2'] = TIT2(encoding=3, text=[title])
            file.tags['TALB'] = TALB(encoding=3, text=[album])
            file.tags['TRCK'] = TRCK(encoding=3, text=[tracknumber])
            file.tags['TDRC'] = TDRC(encoding=3, text=[date])
        else:
            file['artist'] = [artist]
            file['title'] = [title]
            file['album'] = [album]
            file['tracknumber'] = [tracknumber]
            file['date'] = [date]

    file.save()

    return jsonify({"success": True})

@app.route("/browse", methods=["GET"])

def browse():
    directory = request.args.get('path')
    subdir_list = get_directory(directory)

    return jsonify(subdir_list)


@app.route("/load", methods=["POST"])

def load_library():
    path = request.form.get(('folder_path'))
    print("Received path:", path + "end of received path") 

    session['folder_path'] = path

    return redirect(url_for("homepage"))

@app.route("/save-album", methods=["POST"])
def save_album():
    old_album = request.form.get('old_album')
    new_album = request.form.get('new_album')
    folder_path = session.get('folder_path')

    library = get_library(folder_path)

    for song in library:
        if song['Album'] == old_album:
            path = song['Path']
            file = MutagenFile(path)

            if file.tags is None:
                file.add_tags()

            if path.lower().endswith('.mp3'):
                file.tags['TALB'] = TALB(encoding=3, text=[new_album])
            else:
                file['album'] = [new_album]

            file.save()

    return jsonify({"success": True})

@app.route("/save-artist", methods=["POST"])
def save_artist():
    old_artist = request.form.get('old_artist')
    new_artist= request.form.get('new_artist')
    folder_path = session.get('folder_path')

    library = get_library(folder_path)

    for song in library:
        if song['Artist'] == old_artist:
            path = song['Path']
            file = MutagenFile(path)

            if file.tags is None:
                file.add_tags()

            if path.lower().endswith('.mp3'):
                file.tags['TPE1'] = TPE1(encoding=3, text=[new_artist])
            else:
                file['artist'] = [new_artist]
            file.save()

    return jsonify({"success": True})