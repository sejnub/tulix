# Bitmark

Bitmark is a small python script that generates an html page with links that it extracts from the tunnel information in ```tlp``` (Bitvise SSH Client configuration) files.

## What is it

### Background info: Bitvise SSH Client

The [Bitvise SSH Client](https://www.bitvise.com/ssh-client) ([downloadlink](https://www.bitvise.com/ssh-client-download)) is started with a configuration file (that has a name ending on ```.tlp```). The configuration file contains the definition of a list of ssh tunnels (port forwardings) that are established along with the ssh connection.

### What does bitmark do

bitmark starts in the current working directory and recursively searches all folders for ```tlp``` files.
It extracts the tunnel definitions from those files and generates the file ```bitmark.html``` which it puts into the current working directory.

```bitmark.html``` contains links to the local forwarded ports and to the remote targets of those ports.

The following rules are applied:

- A link is only generated if the tunnels comment contains the string ```HTTP``` or ```HTTPS```.
- If the tunnels comment contains the string ```path=somepath``` then the path ```/somepath``` is added to the links URLs.

## Run

### Call interpreter

```python bitmark.py```

### Call executable (Windows)

- Create an executable with PyInstaller (documented later)
- Put the executable in a folder that is in the 'path' variable
- Go to the folder where the ```bitmark.html``` file shall be put.
- Open a command prompt
- Execute ```bitmark```

## Create an executable with PyInstaller

### Install PyInstaller

Run ```pip install PyInstaller```

### Run PyInstaller

Run ```pyinstaller --onefile bitmark.py```

### Get the exe file

The exe is to be found in the ```dist``` folder.
