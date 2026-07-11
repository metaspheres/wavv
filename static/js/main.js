// ====================
// GLOBAL
// ====================

document.getElementById("folder-browser-input").addEventListener("input", getPath)
let navOpen = false;
let sideNav = document.getElementById("mySidenav")
let mainPush = document.querySelectorAll("main-push")

// ====================
// FETCH FOLDER PATH
// ====================

function getPath(event) {
    const path = event.target.value
    fetch('/browse?path=' + path)
        .then(response => response.json())
        .then(data => {

            const suggestions = document.getElementById("suggestions")
            suggestions.innerHTML = ""
            data.forEach(path => {
                console.log("Creating item for:", path)
                const item = document.createElement("div")
                item.textContent = path
                item.addEventListener("click", () => {
                    document.getElementById("folder-browser-input").value = path
                    document.getElementById("selected-path").value = path
                    getPath()

                })
                suggestions.appendChild(item)
            })

        })
}

document.querySelector("form").addEventListener("submit", () => {
    const typedPath = document.getElementById("folder-browser-input").value
    const hiddenInput = document.getElementById("selected-path")
    if (!hiddenInput.value) {
        hiddenInput.value = typedPath
    }
})

// ====================
// SIDEBAR PUSH
// ====================

function openNav() {
    if (navOpen === false) {
        navOpen = true
        document.getElementById("mySidenav").style.width = "450px";
    } else {
        navOpen = false
        document.getElementById("mySidenav").style.width = "0";
        document.querySelectorAll("main-push").style.marginLeft = "0";
    }

}

function openEditor(selectionName) {
    let i;
    let x = document.getElementsByClassName("editable-content");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
        console.log("wat")
    }
    document.getElementById(selectionName).style.display = "block";
}

// ====================
// MODALS
// ====================

function openArtistModal(artistName) {
    const artistModal = document.getElementById("artist-modal")
    const artistNameInput = document.getElementById("modal-artist-name")
    const artist = document.getElementById("modal-artist-list")
    artistModal.dataset.oldArtist = artistName

    artistNameInput.value = artistName
    artist.innerHTML = ''
    console.log(artistName)

    const div = document.createElement('div')
    div.textContent = artistName

    artistModal.style.display = 'flex'

}

function closeArtistModal() {
    document.getElementById('artist-modal').style.display = 'none';
}

function openAlbumModal(albumName) {
    const modal = document.getElementById('album-modal');
    const nameInput = document.getElementById('modal-album-name');
    const songList = document.getElementById('modal-song-list');

    modal.dataset.oldAlbum = albumName;

    nameInput.value = albumName;

    songList.innerHTML = '';
    albumData[albumName].forEach(song => {
        const div = document.createElement('div');
        div.textContent = song['Track Number'] + ' - ' + song['Title'];
        songList.appendChild(div);
    });

    modal.style.display = 'flex';
}

function closeAlbumModal() {
    document.getElementById('album-modal').style.display = 'none';
}

function openSongModal(index) {
    const song = songData[index]
    const songModal = document.getElementById("song-modal")

    songModal.dataset.songIndex = index

    document.querySelector('input[name="artist"]').value = song['Artist']
    document.querySelector('input[name="title"]').value = song['Title']
    document.querySelector('input[name="album"]').value = song['Album']
    document.querySelector('input[name="track-number"]').value = song['Track Number']
    document.querySelector('input[name="date"]').value = song['Date']
    document.querySelector('input[name="path"]').value = song['Path']

    songModal.style.display = 'flex'
}

function closeSongModal() {
    document.getElementById('song-modal').style.display = 'none'
}

// =======================
// EDIT METADATA FUNCTIONS
// =======================

function saveArtistEdit() {
    const artistEditModal = document.getElementById('artist-modal');
    const oldArtistName = artistEditModal.dataset.oldArtist;
    const newArtistName = document.getElementById('modal-artist-name').value;

    fetch('/save-artist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: 'old_artist=' + encodeURIComponent(oldArtistName) + '&new_artist=' + encodeURIComponent(newArtistName)
    })
        .then(response => {
            if (response.ok) {
                console.log(newArtistName)
                window.location.reload();
            }
        });
}

function saveAlbumEdit() {
    const modal = document.getElementById('album-modal');
    const oldName = modal.dataset.oldAlbum;
    const newName = document.getElementById('modal-album-name').value;

    fetch('/save-album', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: 'old_album=' + encodeURIComponent(oldName) + '&new_album=' + encodeURIComponent(newName)
    })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            }
        });
}

function saveSongEdit() {
    const path = document.querySelector('input[name=path').value
    const artist = document.querySelector('input[name="artist"]').value
    const title = document.querySelector('input[name="title"').value
    const album = document.querySelector('input[name="album"]').value
    const tracknumber = document.querySelector('input[name="track-number"]').value;
    const date = document.querySelector('input[name= "track-number"]').value

    fetch('/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: 'path=' + encodeURIComponent(path) +
            '&artist=' + encodeURIComponent(artist) +
            '&title=' + encodeURIComponent(title) +
            '&album=' + encodeURIComponent(album) +
            '&track-number=' + encodeURIComponent(tracknumber) +
            '&date=' + encodeURIComponent(date)
    })

        .then(response => {
            if (response.ok) {
                window.location.reload();
            }
        }

        )
}

