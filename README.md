# Update Webroot Util -- U.W.U. -- (ᵕᴗ ᵕ⁎) v0.5
![version screenshot](/media/uwu.png)
## A simple script to update small html projects
### info: This script assumes that there are two directories
- A project __DEV__ directory, (where the script will live)
- An outward facing test web server __SRV__ directory set up
## How it Works
1. copy ```uwu.py``` to your __DEV__ directory, where you will be working on the code and making changes
2. run ```./uwu.py -b``` to leave U.W.U. on in the background. If it's the first time, U.W.U will ask for the __SRV__ directory
3. start working, the changes will be copied to the __SRV__ directory. __SRV__ will mirror __DEV__
4. run ```./uwu.py``` again to kill the process
## How to Use
```
(ᵘﻌᵘ)
help:
    -b to run in the background
    -h to print this screen
    -r to reset the webroot path
    -v to show which files are saved
    -vv to show hashes
    -V to print the version
```
## Requirements
None! Completely portable.  
Although not tested in Windows, it might work there.
