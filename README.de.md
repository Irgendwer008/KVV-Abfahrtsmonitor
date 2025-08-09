Dies ist eine schnelle und einfache, aber bewusst sehr flexible Lösung zur Anzeige von Abfahrtsdaten aus der [TRIAS-API des KVV](https://www.kvv.de/fahrplan/fahrplaene/open-data.html) auf einem oder insbesondere mehreren Bildschirmen. Sie wurde für die Anzeige im [studentischen Kulturzentrum Z10](https://z10.info) in Karlsruhe entwickelt.

Ideen oder Hilfe sind herzlich willkommen! :)

# Funktionen
- Mehrere Displays, jeweils mit mehreren Stationen, bedarfsgerecht positionierbar
- Live-Daten direkt von der TRIAS-API
- Hohe Flexibilität im Design
- Anpassbare Farben
- Automatische Farberkennung für die Linien-Icons
- Verschiedene Icon-Formen für unterschiedliche Verkehrsmittel, aktuell im Stil der offiziellen KVV-Icons
- Einfache Konfiguration über YAML-Datei
- Relativ optimiert (z. B. durch Caching der Icons), um möglichst schnell zu laufen: Entwickelt für den Betrieb auf einem Raspberry Pi 4 mit zwei Bildschirmen
- QR-Code mit benutzerdefiniertem Inhalt (z. B. Links), Größe und Farben

# Voraussetzungen
- Python 3 (nicht sicher, welche Version genau funktioniert, aktuell läuft es mit 3.12.11)
- Zugriff auf die KVV TRIAS-API. Weitere Infos und wie du Zugang bekommst [hier](https://www.kvv.de/fahrplan/fahrplaene/open-data.html)

# Installation
- Klone das Repository in das lokale Dateisystem:
    ```sh
    git clone https://github.com/Irgendwer008/OpenDepartureDisplay.git
    cd OpenDepartureDisplay
    ```
- Erstelle und aktiviere eine virtuelle Umgebung (theoretisch optional, aber empfohlen):
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate  # Unter Windows: .env\Scripts\activate
    ```
- Bearbeite die Konfigurationsdatei (siehe [Konfiguration](#konfiguration)) nach deinen Bedürfnissen
- Installiere Pythonpakete: `pip install -r requirements.txt`
- Starte das Programm mit: `python main.py`

# Konfiguration
Die Anwendung verwendet eine YAML-Konfigurationsdatei zur Definition von Fensterlayouts, Stationen und Zugangsdaten. Eine vollständige Vorlage findest du in der Datei [config_template.yaml](https://github.com/Irgendwer008/OpenDepartureDisplay/blob/main/config_template.yaml).

Hier eine Aufschlüsselung der Abschnitte:

## Allgemein

Allgemeine Einstellungen:
- "time_zone": \
  Setze deine entsprechende Zeitzone für die korrekte Berechnung der Abfahrtszeit (siehe [Wikipedia](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) oder [IANA-Spezifikation](https://www.iana.org/time-zones) für eine Liste möglicher Werte)
- "SEV-lines use normal line icon colors": \
  Gibt an, ob Linien, die mit „SEV“ beginnen, die gleiche automatische Farbgebung wie die Linie erhalten sollen, die sie ersetzen (True), oder ob sie die in [Farben](#farben) festgelegten Standardfarben nutzen sollen (False)

  Beispiel: Wenn True: Die Linie "SEV 10" verwendet die Linienfarbe von Linie "10" anstelle der Standardfarben.
- "QR-Code-content": \
  Dein individueller QR-Code-Inhalt. Leer lassen, um keinen QR-Code anzuzeigen.
- "QR-Code-height": \
  Definiert die Höhe des QR-Codes relativ zur Kopfzeile. Muss ein Wert zwischen 0 und 1 (inklusive) sein.

## Fenster
Definiert das Layout und die Eigenschaften jedes Anzeigefensters. Jedes Fenster benötigt:

- position_x & position_y: Position des Fensters (oben links) auf dem Bildschirm
- width & height: Größe des Fensters in Pixeln
- station: Der Name der Station, die mit diesem Fenster verbunden ist. Jede Station, die hier verwendet wird, muss im Abschnitt [Stationen](#stationen) definiert sein.

Beispiel:
```yaml
windows:
  - position_x: 0
    position_y: 0
    width: 800
    height: 400
    station: Durlacher Tor / KIT-Campus Süd
  - position_x: 800
    position_y: 0
    width: 600
    height: 300
    station: Kronenplatz
  - position_x: 1920
    position_y: 0
    width: 1920
    height: 1080
    station: Hauptbahnhof
```

## Stationen
Dieser Abschnitt definiert, welche Haltepunkte (Stop-Point-Refs) zu welchem Anzeigenamen (Station) gehören.

Jeder Stationseintrag enthält einem Namen und eine oder mehrere Stop-Point-Refs, optional mit:
- prefix: Text, der dem Namen des Bahnsteigs vorangestellt wird
- suffix: Text, der angehängt wird (z. B. "(U)" für unterirdisch)

Beispiel: 

```yaml
stations:
  Durlacher Tor / KIT-Campus Süd:
    - stop_point_ref: de:08212:3
    - stop_point_ref: de:08212:1001
      suffix: "(U)"
```

Das obige Beispiel entspricht folgendem:

```yaml
stations:
  Durlacher Tor / KIT-Campus Süd:
    - stop_point_ref: de:08212:3
      prefix: ""
      suffix: ""
    - stop_point_ref: de:08212:1001
      prefix: ""
      suffix: "(U)"
```

## Farben

Hier kannst du die jeweiligen Hex-Codes für das UI-Design eintragen:
```yaml
colors:
  header_background: "#FFA500"
  header_text: "#000000"
  departure_entry_lighter: "#FFFFFF"
  departure_entry_darker: "#EEEEEE"
  departure_entry_text: "#000000"
  default_icon_background: "#006EFF"
  default_icon_text: "#FFFFFF"
  qr_code_background: "#FFFFFF"
  qr_code_foregreound: "#000000"
```

## Zugangsdaten

Beinhaltet die Zugangsdaten zur TRIAS-API des KVV.

- url: Die vollständige URL zur TRIAS-Schnittstelle (ersetze YOUR-URL)
- requestor_ref: Deine Requestor-ID (ersetze YOUR-REQUESTOR_REF)

Beides muss beim KVV beantragt werden, siehe [Voraussetzungen](#voraussetzungen)

Beispiel:

```yaml
credentials:
  url: https://projekte.kvv-efa.de/YOUR-URL/trias
  requestor_ref: YOUR-REQUESTOR_REF
```

# Beenden
Du kannst das Programm jederzeit mit `Strg`+`q` in einem der Fenster beenden.
