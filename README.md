This is quick and easy, but by design very flexible Solution for displaying departure data from the [KVV's TRIAS-API](https://www.kvv.de/fahrplan/fahrplaene/open-data.html) on or especially several displays. It was developed for display at the students culture club ["Z10"](https://z10.info) in Karlsruhe.

Any ideas or help by you is warmely welcome! :)

# Features
- Multiple displays with each multiple stations, simultaneously and precisely placeable
- Live train data directly from the TRIAS API
- Designed to be highly flexible
- Custom colors
- autmoatic line icon color detection
- simple configuration via YAML file
- Rather optimized, e.g. by caching icon images, to be as fast as possible: Intended to run on Raspberry Pi 4 with dual displays

# Requirements
- Python 3 (not shure which exactly works, currently on 3.12.11)
- Access to the KVV Trias API. Read more on that and how to get acces [here](https://www.kvv.de/fahrplan/fahrplaene/open-data.html)

# Installation
- clone this repo to your local machine:
    ```sh
    git clone https://github.com/Irgendwer008/OpenDepartureDisplay.git
    cd OpenDepartureDisplay
    ```
- create and activate virtual environment (technically optional, though recommended):
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .env\Scripts\activate
    ```
- Edit the configuration file (see [Configuration](#configuration)) to your needs
- Install python packages: `pip install -r requirements.txt`
- Run: `python`

# Configuration
The application uses a YAML configuration file to define window layouts, stations, and credentials. A complete template configuration file can be found in the [config_template.yaml](https://github.com/Irgendwer008/OpenDepartureDisplay/blob/main/config_template.yaml).

Below is a breakdown of each section:

## General

General settings are:
- "SEV-lines use normal line icon colors": \
    whether lines starting with "SEV" should use the automatic line numbering as the line they are replacing (True) or if they should use the "default_icon_text" and "-background" configured in [Colors](#colors) (False)

    Example: if True: line "SEV 10" uses the icon line color corresponding to line "10" instead of default icon colors

## Windows
Defines the layout and properties of each display window. Each entry has to include

- position_x & position_y: Top-left screen coordinates of the window
- width & height: Dimensions of the window in pixels
- station: The name of the station associated with this window. Every station referenced by a window has to exist in the [station config](#stations)

Example:
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

## Stations
This section defines which stop points (platforms) belong to which station name.

Each station entry maps a display name to one or more 
- stop_point_refs, each with a optional:
    - prefix: A string to prepend to the platform label
    - suffix: A string to append (e.g. "(U)" for underground)

Example: 

```yaml
stations:
  Durlacher Tor / KIT-Campus Süd:
    - stop_point_ref: de:08212:3
    - stop_point_ref: de:08212:1001
      suffix: "(U)"
```

the config above works identically to

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


## Colors

Here you can enter the respective hex codes used to draw the GUI:
```yaml
colors:
  header_background: "#FFA500"
  header_text: "#000000"
  departure_entry_lighter: "#FFFFFF"
  departure_entry_darker: "#EEEEEE"
  departure_entry_text: "#000000"
  default_icon_background: "#006EFF"
  default_icon_text: "#FFFFFF"
```
## Credentials

Contains the credentials required to access the KVV Trias API.

- url: The full endpoint URL for your TRIAs server (replace YOUR-URL)
- requestor_ref: Your requestor ID (replace YOUR-REQUESTOR_REF)

Both need to be requested from KVV, see [Requirements](#requirements)

Example:

```yaml
credentials:
  url: https://projekte.kvv-efa.de/YOUR-URL/trias
  requestor_ref: YOUR-REQUESTOR_REF
```

# Exit
You can exit the programm at any time by pressing `Ctrl`+`q` in any of the windows.
