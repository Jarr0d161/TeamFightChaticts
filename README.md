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
  * Eingabe: **python3 coding/TFTwitch.py**)
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



