# Recurring Reminders für Home Assistant

Eine Custom Integration für wiederkehrende Erinnerungen und Aufgaben.

## 🚀 Installation über HACS

### Schritt 1: Repository hinzufügen
1. Öffnen Sie HACS in Home Assistant
2. Gehen Sie zu "Integrationen" 
3. Klicken Sie auf die drei Punkte oben rechts → "Benutzerdefinierte Repositories"
4. Fügen Sie diese Repository-URL hinzu: `https://github.com/IhrUsername/recurring_reminders`
5. Wählen Sie "Integration" als Kategorie
6. Klicken Sie auf "Hinzufügen"

### Schritt 2: Integration installieren
1. Suchen Sie nach "Recurring Reminders" in HACS
2. Klicken Sie auf "Installieren"
3. Starten Sie Home Assistant neu

### Schritt 3: Integration konfigurieren
1. Gehen Sie zu Einstellungen → Geräte & Services
2. Klicken Sie auf "Integration hinzufügen"
3. Suchen Sie nach "Recurring Reminders"
4. Folgen Sie den Konfigurationsschritten

## 📋 Für GitHub Repository

Um dieses Projekt auf GitHub zu veröffentlichen:

1. **Repository erstellen**:
   - Erstellen Sie ein neues Repository auf GitHub
   - Name: z.B. `recurring_reminders`
   - Öffentlich machen (für HACS erforderlich)

2. **Dateien hochladen**:
   - Laden Sie alle erstellten Dateien in das Repository hoch
   - Stellen Sie sicher, dass die Ordnerstruktur korrekt ist

3. **README anpassen**:
   - Ersetzen Sie `yourusername` in allen Dateien mit Ihrem GitHub-Benutzernamen
   - Aktualisieren Sie die URLs in der README.md

4. **Release erstellen**:
   - Gehen Sie zu "Releases" in Ihrem GitHub Repository
   - Klicken Sie auf "Create a new release"
   - Tag: `v1.0.0`
   - Titel: `Version 1.0.0`
   - Beschreibung: Initial release

## 📁 Repository-Struktur

```
recurring_reminders/
├── .github/
│   └── workflows/
│       ├── release.yml
│       └── validate.yml
├── custom_components/
│   └── recurring_reminders/
│       ├── __init__.py
│       ├── config_flow.py
│       ├── const.py
│       ├── manifest.json
│       ├── sensor.py
│       └── services.yaml
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── hacs.json
├── LICENSE
└── README.md
```

## 🔧 Nach der GitHub-Veröffentlichung

Benutzer können dann die Integration über HACS installieren:

1. **HACS → Integrationen → Benutzerdefinierte Repositories**
2. **URL**: `https://github.com/IhrUsername/recurring_reminders`
3. **Kategorie**: Integration
4. **Installation** über HACS GUI

## ✨ Features der Integration

- ✅ Konfigurierbare Erinnerungsintervalle
- ✅ Zwei Sensoren pro Erinnerung (Intervall + Countdown)
- ✅ Services zum Zurücksetzen und manuellen Setzen
- ✅ Automatische tägliche Updates
- ✅ HACS-kompatibel
- ✅ Deutsche Lokalisierung
- ✅ Persistent Storage
- ✅ GitHub Actions für Validierung

Die Integration ist jetzt vollständig HACS-kompatibel und bereit für die Veröffentlichung auf GitHub!