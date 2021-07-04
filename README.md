
# Vauban.Deauth - Deauthenticate everything, everyone and everywhere.

Vauban.deauth is a part of Vauban, my cybersecurity project. Vauban is using scapy to generate cyber-attacks to test routers and equipments.

This is the first version of a python-tool used to deauthenticate all clients in all network to capture handshake. 

Use it alongside airodump-ng.

All reamrks are wellcome !


# Features : 

- Puts your desired wireless card in monitor mode
- Gather informations about networks & clients around you
- Deauthenticate everyone until you stop the script

# Installation & dependencies :

## Dependencies : 

- Aircrack-ng
- A wireless card capable of monitor mode & injection
- python 3.5+ (tested in 3.9)
- installing all librairies in requirements.txt
- Modified version of pyrcrack (https://github.com/XayOn/pyrcrack | Included ) 

## Installation

- Clone the github repo : 
```
git clone https://github.com/Victorhin0/Vauban.Deauth.git
```


- Install all librairies with requirements.txt : 
```
pip install -r requirements.txt
```
- Run the script 

```
python3 main.py
```

# Bugs and problems : 

If you have any problem about the script, let me know, i'll be happy to correct it!

# How it works : 

Vauban.Deauth is using pyrcrack to gather any informations about networks and clients in the area, and scapy 'creates' the deauth packet.

Everything is explained line-to-line in main.py

## License
[MIT](https://choosealicense.com/licenses/mit/)
