In the jupiter notebook the whole process from loging in in the GSI network over taking data to looking at nice plots of the acquired data are described.

## 2. Powering

If the chip is not operating, all power supplies have to be turned off and be turned on, if you want to use the detector.
- ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) `Warning!!!`
Before running any command here, check again and know what you are about to turn on/off. Wrong usage of the powersupply can irreversibly damage the detectors.

From the Homedirectory ($\color{green}{\text{curved@alipc006:~$ \$ $}}$, if you are not there type $\color{blue}{\text{cd}}$) the status of the power supply can be printed by:

`\color{blue}{\text{python3 ~/eudaq2/user/ITS3/python/HMP4040.py}}$

To turn on/off channel 1 (other channels analogously), write:

$\color{blue}{\text{python3 ~/eudaq2/user/ITS3/python/HMP4040.py --off -c 1 }}$

$\color{blue}{\text{python3 ~/eudaq2/user/ITS3/python/HMP4040.py --on -c 1}}$

For doing a complete power cycle (turn off and off again), use the following command:

$\color{blue}{\text{python3 ~/eudaq2/user/ITS3/python/HMP4040.py --off -c 1 && sleep 1 && python3 ~/eudaq2/user/ITS3/python/HMP4040.py --off -c 2 && python3 ~/eudaq2/user/ITS3/python/HMP4040.py --off -c 3 && python3 ~/eudaq2/user/ITS3/python/HMP4040.py --off -c 4 && sleep 2 && python3 ~/eudaq2/user/ITS3/python/HMP4040.py --on -c 1 && sleep 1 && python3 ~/eudaq2/user/ITS3/python/HMP4040.py --on -c 2 && python3 ~/eudaq2/user/ITS3/python/HMP4040.py --on -c 3 && python3 ~/eudaq2/user/ITS3/python/HMP4040.py --on -c 4}}$

In normal operation, the Powersupply should be used in the following manner:

