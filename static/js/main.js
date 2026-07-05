document.getElementById("folder-browser-input").addEventListener("input", getPath)
let navOpen = false;
let sideNav = document.getElementById("mySidenav")
let mainPush = document.querySelectorAll("main-push")
//fetch folder paths

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

//modals

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

// sidebar w/push


function openNav() {
    if (navOpen === false) {
        navOpen = true
        document.getElementById("mySidenav").style.width = "450px";
    } else{
        navOpen = false
        document.getElementById("mySidenav").style.width = "0";
        document.querySelectorAll("main-push").style.marginLeft = "0";
    }

}

function openEditor(selectionName) {
  var i;
  var x = document.getElementsByClassName("editable-content");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
    console.log("wat")
  }
  document.getElementById(selectionName).style.display = "block";
}