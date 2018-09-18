# Tulix

```tulix``` is short for 'TUnnel LInk eXtractor'.

```tulix``` is a small python script that generates an html page with links that it extracts from the tunnel information in ```tlp``` (Bitvise SSH Client configuration) files.

## What is it

### Background info: Bitvise SSH Client

The [Bitvise SSH Client](https://www.bitvise.com/ssh-client) ([downloadlink](https://www.bitvise.com/ssh-client-download)) is started with a configuration file (that has a name ending on ```.tlp```). The configuration file contains the definition of a list of ssh tunnels (port forwardings) that are established along with the ssh connection.

### What does tulix do

tulix starts in the current working directory and recursively searches all folders for ```tlp``` files.
It extracts the tunnel definitions from those files and generates the file ```tulix.html``` which it puts into the current working directory.

```tulix.html``` contains links to the local forwarded ports and to the remote targets of those ports.

The following rules are applied:

- A link is only generated if the tunnels comment contains the string ```HTTP``` or ```HTTPS```.
- If the tunnels comment contains the string ```path=somepath``` then the path ```/somepath``` is added to the links URLs.

## Run

### Call interpreter

```python tulix.py```

### Call executable (Windows)

- Create an executable with PyInstaller (documented later)
- Put the executable in a folder that is in the 'path' variable
- Go to the folder where the ```tulix.html``` file shall be put.
- Open a command prompt
- Execute ```tulix```

## Create an executable with PyInstaller

### Install PyInstaller

Run ```pip install PyInstaller```

### Run PyInstaller

Run ```pyinstaller --onefile tulix.py```

### Get the exe file

The exe is to be found in the ```dist``` folder.

## Code quality and status

For me tulix does it's job.

tulix is my second python script ever so the code is ugly and a _lot_ of improvements would be needed to make it good python.

tulix is only tested with very few configuration files. So it might be that my reverse engineering does not cover all possible configurations and tulix might fail to process with yours. If it does, please send me your configuration file so that I can improve the script!

You are very much invited to improve the script yourself and send a pull request.