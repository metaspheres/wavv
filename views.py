from main import app
from flask import render_template, request, redirect, url_for, jsonify, session
from mutagen import File as MutagenFile
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK, TDRC
from models import *

@app.route("/")

def homepage():
    folder_path = session.get('folder_path')

    if not folder_path:
        return render_template("homepage.html", data=[])
    
    library = get_library(folder_path)
    return render_template("homepage.html", data=library)

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

    return redirect(url_for("homepage"))

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
