# Installation

> Die Dokumentation ist nur fuer Linux gueltig. Unter Windows kann es leicht variieren.

Zuerst muss eine virtuelle Umgebung erstellt werden:
```
python3 -m venv .venv
```

Dann aktiviert man die virtuelle Umgebung:
```
    source .venv/bin/activate
``` 

Danach kann man die Abhaengigkeiten installieren
```
pip install -r requirements.txt
```

# Spiel starten

Einfach die `main.py` in virtueller Umgebung ausfuehren:
```
python3 main.py
```
oder wenn der Pfad nicht korrekt aktualisiert wurde mit:
```
.venv/bin/python3 main.py
```
