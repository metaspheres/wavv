# WAVV

WAVV is a song metadata editor using Flask and pywebview.

## Current functionalities
Load file paths into the program, batch edit album and artist names and edit individual songs metadata all in the same page, with a simple UI.

## How to test

! WAVV is a work in progress !

To test, open your command line/terminal and run these commands one by one.

Clone the repository:

    git clone https://github.com/metaspheres/wavv.git

Go to the directory:

    cd wavv
Recommended: create a virtual environment. A virtual environment means the dependencies are installed only on the WAVV folder and keeps the rest of your system clean.

    python -m venv venv

### Activate the virtual environment

**Windows**:
If using Windows Command Prompt (cmd):

	venv\Scripts\activate.bat

If using PowerShell:

    venv\Scripts\Activate.ps1
    
For PowerShell: If you get a "running scripts is disabled" error, run this once:

    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

**Mac and Linux:**

	python -m venv venv

Note: some systems require `python3` instead of `python`, so if the above returns an error try:

     python3 -m venv venv

Lastly, activate the Virtual Environment:
     
     source venv/bin/activate

## Install the dependencies on the virtual environment (all OS's):

     pip install -r requirements.txt

Run the app:

     python main.py
     
If the above is not recognized on Mac/Linux:

     python3 main.py

pywebwiew will automatically find an available port and open WAVV in its own window.

## Known issues on Linux (tested on Arch / EndeavourOS)

pywebview (which WAVV uses to open a native window) can run into a few common
issues on Linux. These seem to stem from missing GTK bindings and from
Wayland-related rendering bugs in WebKitGTK. I have been able to confirm these errors and the fixes below on
Arch/EndeavourOS with KDE Plasma. Other distros may or may not be affected.
If you have these errors on a different distro, or other errors altogether, please open an issue and let me know.

If you see this error:

    webview.errors.WebViewException: You must have either QT or GTK with
    Python extensions installed in order to use pywebview.

Install GTK bindings at the system level, then rebuild your venv to see them (one command at a time):

    sudo pacman -S python-gobject gtk3 webkit2gtk-4.1
    python -m venv venv --system-site-packages
    source venv/bin/activate
    pip install -r requirements.txt

If you're on Wayland (you can check with the terminal command `echo $XDG_SESSION_TYPE`), you may then hit this error:

    Gdk-Message: Error 71 (Protocol error) dispatching to Wayland display.

Check whether you have XWayland (check with the terminal commmand `pacman -Qs xwayland`). Install it if not:

    sudo pacman -S xorg-xwayland

Then run the app forcing the X11 backend:

    GDK_BACKEND=x11 python main.py

If you then see this error:

    Failed to create GBM buffer of size 800x600: Invalid argument

Also disable WebKit's hardware compositing:

    WEBKIT_DISABLE_COMPOSITING_MODE=1 GDK_BACKEND=x11 python main.py
