# TeamFightChaticts

Das GIT-Repository beinhaltet einen Twitch-Chat-Bot, welcher Chatnachrichten in Maus- und Tastatur-Befehle umwandelt. Der Python3-Code ist aktuell für das Spiel Team Fight Tactics (TFT) von Riot Games ausgelegt. Kann durch Anpassungen, aber auch auf andere Spiele übertragen werden. 

## Vorbereitung

* Download Python3 - https://www.python.org/downloads/
* Download Tesseract - https://tesseract-ocr.github.io/tessdoc/Home.html
* Tesseract installieren (Installationspfad kopieren)
* Clone/Download Repository
* Benötigte Python-Packages installieren (requirements.txt)
* config/config.txt anpassen
  * Tesseract-Installationspfad eintragen
  * Authentifizierungsnummer für Twitchaccount (Chatbot) eintragen
  * Twitch-Channelname eintragen

## Programm ausführen

* coding/TFTwitch.py ausführen 
  * Eingabeaufforderung (Terminal, cmd) im root-git-Ordner öffnen
  * Eingabe: **python3 coding/TFTwitch.py**
* Pool-Größe (Anzahl gleicher Nachrichten) eintragen und Start drücken
* Stop trennt die Verbindung zum TwitchChat
* Hinweis: Viele Werte sind aktuell noch "hardcoded" auf 1900x1080p, beim Starten von TFT beachten!

## Befehle im Chat

* Im Shop kaufen: shop(1-5) --- z.B. *shop1*
* Einheit setzen: [Feld1][Feld2] --- z.B. *w1r5*
* Von Bank verkaufen: sellw(1-9) --- z.B. *sellw3*
* Shop neu würfeln: *roll* / *reroll*
* Aufleveln: *lvl* / *lvlup*
* Items einsammeln: *collect*
* Augment auswählen: aug(1-3) --- z.B. *aug2*
* Loslaufen (nach oben) im Karussell: *now*
* Horizontales Laufen: row(1-8) --- z.B. *row4*
* Items verteilen: [Itemfeld][Feld] --- z.B. *bw3*
* Shop sperren/entsperren: *lock* / *unlock*

## EN
This repository includes a twicht chat bot that allows you to play Team Fight Tactics (TFT) von Riot Games with your chat.
This bot converts twitch chat messages into mouse and keyboard commands.
Feel free to convert the keymappings to play other games with it!
## Prerequisits

* Download Python3 - https://www.python.org/downloads/
* Download Tesseract - https://tesseract-ocr.github.io/tessdoc/Home.html
* Install Tesseract (Copy the installation path)
* Clone or download this repository
* Open the commandline _(using ⊞ Win + R and enter `cmd`)_
* Run `cd <local/path/to/the/git/repository>`
* Run `pip install -r requirements.txt` or `python -m pip install -r requirements.txt`
* adjust the (config)[config/config.txt]
  tesseract=C:\Program Files\Tesseract-OCR
auth=oauth:ZahlenUndBuchstaben
channel=ChannelName
  * Adjust the Tesseract installation path _(`tesseract=<path/>to/your/tesseract/installation`)_
  * Adjust the authentication to match the twitch account of your bot _(`auth=oauth:yourRetrievedCode`)_, which can be retrieved (here)[https://dev.twitch.tv/docs/authentication/getting-tokens-oauth]
  * Adjust the channel name to match the streamers twitch channel name _(`channel=theStreamersChannelName`)_

## Execution

* Make sure your commandline is still in the repository directory
* Execute `python coding/TFTwitch.py`
* Enter the Pool-Größe = Pool-size _(Amount of messages that will be treated as equal)_
* Hitting *Stop* will disconnect the connection to the twitch chat.
* Many of the parameters are still hardcoded _(e.g. the resolution 1900x1080p)_, please consider that when running TFT.
## Chat commands

* Buy in the shop: shop(1-5) --- e.g. *shop1*
* Place units: [Field1][Field2] --- e.g. *w1r5*
* Sell from substitutes bench: sellw(1-9) --- e.g. *sellw3*
* Reroll the buyable units: *roll* / *reroll*
* Level up: *lvl* / *lvlup*
* Collect items: *collect*
* Select augment: aug(1-3) --- e.g. *aug2*
* Start walking during carousell stage (upwards): *now*
* Walk horizontal: row(1-8) --- e.g. *row4*
* Distribute items: [Itemfield][Field] --- e.g. *bw3*
* Lock or unlock the shop: *lock* / *unlock*




