# WAVV

WAVV is a song metadata editor using Flask and PyWebView.


## Current functionalities
Easily load file paths into the program, batch edit album and artist names and edit individual songs all in the same page in a clean and simple UI.

## How to test

This is a work in progress. To test, open the Windows command line and run these commands one by one:
- git clone https://github.com/metaspheres/wavv.git
- cd wavv
- pip install -r requirements.txt
- python main.py

The app will start at http://127.0.0.1:5000.

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
(Note: some systems require `python3` instead of `python`.)
Run first:

     python3 -m venv venv

Then:
     
     source venv/bin/activate

Install the dependencies on the virtual environment:

     pip install -r requirements.txt

Run the app:

     python main.py
     
If the above is not recognized on Mac/Linux:

     python3 main.py

PyWebView will automatically find an available port and open WAVV in its own window.
