# Installation

> Die Dokumentation ist nur für Linux gültig. Unter Windows kann es leicht variieren.

Zuerst muss eine virtuelle Umgebung erstellt werden:
```
python3 -m venv .venv
```

Dann aktiviert man die virtuelle Umgebung:
```
source .venv/bin/activate
``` 

Danach kann man die Abhängigkeiten installieren
```
pip install -r requirements.txt
```

# Spiel starten

Einfach die `main.py` in virtueller Umgebung ausführen:
```
python3 main.py
```
oder wenn der Pfad nicht korrekt aktualisiert wurde mit:
```
.venv/bin/python3 main.py
```

# Anleitung

Als eine Schlange, die stark auf ihre Obst-Ernährung achtet, 
navigiert man durch verschiedene Level und sammelt dabei Äpfel oder Kirschen ein, 
die die Schlange direkt auf dem Weg verzehrt.

Äpfel und Kirschen erscheinen beide zufaellig auf der Map.
Jeder Apfel und jede Kirsche lassen die Snake allerdings um eins länger werden, 
wobei Äpfel einen und Kirschen zwei Punkte geben. 

Da Kirschen zwei Punkte wert sind, sind sie besonders und erscheinen meist nur für ein paar Sekunden, 
bevor sie wieder für mehrere Sekunden verschwinden.

Ziel ist es in jedem Level genug Punkte zu sammeln, 
um ins jeweilige nächste Level aufzusteigen und schlussendlich das Spiel zu gewinnen.
Dabei darf man nicht mit dem Rand des Spielfeldes, Baumstämmen oder sich selbst kollidieren.

## Steuerung

### In Menues

- **Start:** Linksklick auf den "Spielen"-Button um fortzufahren
- **Verloren:** Linksklick zum neustarten
- **Gewonnen:** Linksklick zum neustarten
- **Level-Up:** kurz warten oder Linksklick um fortzufahren

### Im Spiel

Die Snake bewegt sich automatisch in die Richtung, in die sie guckt.
Die Steuerung in verschiedene Richtungen ist dabei nicht relativ von der Snake ausgehend, 
sondern als Himmelsrichtungen zu verstehen. Somit kann die Snake auch niemals in die entgegengesetze Richtung gelenkt werden.

- **Tastenbelegung:**
  - Linke Pfeiltaste um nach links zu lenken
  - Rechte Pfeiltaste um nach rechts zu lenken
  - Obere Pfeiltaste um nach oben zu lenken
  - Untere Pfeiltaste um nach unten zu lenken

## Level

Die Level sind in Textdateien beschrieben und bestehen aus zwei Teilen:

### Map

Sie besteht aus einem 20x20 Feld von Nullen und Einsen, die durch Kommas separiert werden:
```
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0
...
```
wobei:
- 0 - Grasflaeche, auf der die Snake sich fortbewegen kann
- 1 - Baumstamm, mit dem die Snake nicht kollidieren darf

> Man muss beachten, dass die Map im Spiel dann gespiegelt auf der linken Seite liegt, 
weshalb sich symmetrische Maps am besten anbieten.

### Parameter

Parameter werden durch ein ">" am Zeilenanfang gekennzeichnet. Sie sind optional und definieren bestimmte Eigenschaften des Levels:

- **"speed":** setzt die Geschwindigkeit der Snake
- **"next":** setzt die zu erreichende Punktzahl
- **"snake_pos":** setzt die Startposition der Snake
- **"snake_dir":** setzt die Startrichtung der Snake
- **"cherries":** aktiviert / deaktiviert Kirschen
- **"cherry_time":** gibt in Sekunden an für wie lange die Kirsche erscheint
- **"cherry_out_time":** gibt die Range in Sekunden an für wie lange die Kirsche verschwindet

Alle Parameter mit Standardwerten:
```
> speed 10              # Um eins vorwärts alle FPS(60) - 10 = 50 FPS
> next 10               # 10 Punkte fuer Level-Up
> snake_pos 10 10       # x = 10; y = 10
> snake_dir u           # u = up; d = down; l = left; r = right
> cherries 1            # 1 = aktiviert; 0 = deaktiviert
> cherry_time 6         # 6 Sekunden
> cherry_out_time 5 10  # zwischen 5 bis 10 Sekunden
```

Kommentare in der Leveldatei sind nicht unterstützt.

# Credits

Game Over Sound Effect by <a href="https://pixabay.com/de/users/freesound_community-46691455/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=6435">freesound_community</a> from <a href="https://pixabay.com/sound-effects//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=6435">Pixabay</a>

Apple Bite Sound Effect by <a href="https://pixabay.com/de/users/bunny_cube98-49455455/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=316785">bunny_cube98</a> from <a href="https://pixabay.com/sound-effects//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=316785">Pixabay</a>

Level Up Sound Effect by <a href="https://pixabay.com/de/users/delon_boomkin-32986949/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=438908">Delon_Boomkin</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=438908">Pixabay</a>

Background Music Sound Effect by <a href="https://pixabay.com/de/users/freesound_community-46691455/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=68698">freesound_community</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=68698">Pixabay</a>

Cherry Bite Sound Sound Effect by <a href="https://pixabay.com/de/users/freesound_community-46691455/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=83240">freesound_community</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=83240">Pixabay</a>
