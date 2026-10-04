# HA Sidebar Manager

![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2026.5%2B-blue.svg)
![Version](https://img.shields.io/badge/Version-0.4.2-green.svg)

Eine benutzerdefinierte Home Assistant Integration, mit der du beliebige interne HA-Seiten als eigene Einträge in der Seitenleiste anlegen kannst. Kein Editieren von YAML-Dateien nötig, alles läuft über die HA-Oberfläche.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=arnaudfeld&repository=ha-sidebar-manager&category=integration)

---

## Funktionen

- Entwicklerwerkzeuge-Unterseiten direkt in die Seitenleiste legen (Zustände, Dienste, Template, Ereignisse, YAML, Statistiken)
- Beliebige interne Home Assistant URLs als Seitenleisten-Eintrag hinzufügen
- Titel und Icon frei wählbar
- Einträge optional auf Administratoren beschränken
- Mehrere Einträge gleichzeitig möglich
- Einträge jederzeit bearbeiten oder löschen

---

## Installation via HACS

### Einfache Installation (empfohlen)
Klicke auf den Button oben und folge den Anweisungen in Home Assistant.

### Manuelle HACS-Installation
1. HACS öffnen
2. Oben rechts auf die drei Punkte klicken und "Benutzerdefinierte Repositories" auswählen
3. URL `https://github.com/arnaudfeld/ha-sidebar-manager` eintragen, Kategorie "Integration" auswählen und hinzufügen
4. Die Integration "HA Sidebar Manager" in HACS suchen und installieren
5. Home Assistant neu starten

---

## Manuelle Installation

1. Den Ordner `custom_components/hasidebarmanager` aus diesem Repository herunterladen
2. Den Ordner nach `/config/custom_components/hasidebarmanager` kopieren
3. Home Assistant neu starten

---

## Einrichtung

1. In Home Assistant zu "Einstellungen" > "Geräte und Dienste" navigieren
2. Auf "Integration hinzufügen" klicken und nach "HA Sidebar Manager" suchen
3. Eintragstyp auswählen: Entwicklerwerkzeuge oder Benutzerdefiniert
4. Titel, Icon und Ziel-URL festlegen
5. Speichern

Jeder Eintrag wird sofort in der Seitenleiste sichtbar. Zum Bearbeiten einfach auf "Konfigurieren" beim jeweiligen Eintrag klicken.

---

## Hinweise

- Funktioniert nur mit internen Home Assistant URLs (z.B. `/lovelace/0`, `/developer-tools/state`)
- Externe URLs werden nicht unterstützt
- Getestet mit Home Assistant 2026.5 und 2026.6
- Die Übersetzungen der Auswahlfelder im Konfigurationsdialog basieren auf der Arbeit von [DemonIOI/ha-sidebar-manager](https://github.com/DemonIOI/ha-sidebar-manager). Danke für die Vorlage.

---

## Lizenz

MIT License. Siehe [LICENSE](LICENSE) für Details.

---
---

# HA Sidebar Manager

![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2026.5%2B-blue.svg)
![Version](https://img.shields.io/badge/Version-0.4.2-green.svg)

A custom Home Assistant integration that lets you add any internal HA page as its own entry in the sidebar. No YAML editing required, everything is configured through the HA interface.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=arnaudfeld&repository=ha-sidebar-manager&category=integration)

---

## Features

- Add Developer Tools subpages directly to the sidebar (States, Services, Template, Events, YAML, Statistics)
- Add any internal Home Assistant URL as a sidebar entry
- Freely choose title and icon
- Optionally restrict entries to administrators only
- Multiple entries supported simultaneously
- Entries can be edited or deleted at any time

---

## Installation via HACS

### Easy installation (recommended)
Click the button above and follow the instructions in Home Assistant.

### Manual HACS installation
1. Open HACS
2. Click the three dots in the top right and select "Custom repositories"
3. Enter `https://github.com/arnaudfeld/ha-sidebar-manager`, select category "Integration" and add it
4. Search for "HA Sidebar Manager" in HACS and install it
5. Restart Home Assistant

---

## Manual Installation

1. Download the folder `custom_components/hasidebarmanager` from this repository
2. Copy the folder to `/config/custom_components/hasidebarmanager`
3. Restart Home Assistant

---

## Setup

1. In Home Assistant go to "Settings" > "Devices and Services"
2. Click "Add Integration" and search for "HA Sidebar Manager"
3. Select entry type: Developer Tools or Custom
4. Set title, icon and target URL
5. Save

Each entry will appear in the sidebar immediately. To edit, click "Configure" on the respective entry.

---

## Notes

- Only works with internal Home Assistant URLs (e.g. `/lovelace/0`, `/developer-tools/state`)
- External URLs are not supported
- Tested with Home Assistant 2026.5 and 2026.6
- The config flow selector translations are based on the work of [DemonIOI/ha-sidebar-manager](https://github.com/DemonIOI/ha-sidebar-manager). Thanks for the groundwork.

---

## License

MIT License. See [LICENSE](LICENSE) for details.