# Recurring Reminders Integration

Eine Custom Home Assistant Integration für wiederkehrende Erinnerungen und Aufgaben.

## Funktionen

- **Konfigurierbare Erinnerungen**: Erstellen Sie Erinnerungen mit individuellen Intervallen (in Tagen)
- **Zwei Sensoren pro Erinnerung**:
  - **Intervall-Sensor**: Zeigt das eingestellte Intervall in Tagen
  - **Countdown-Sensor**: Zählt die Tage bis zur nächsten Erinnerung runter
- **Services für Interaktion**:
  - `recurring_reminders.reset_reminder`: Setzt den Countdown zurück
  - `recurring_reminders.set_reminder_days`: Setzt den Countdown auf einen benutzerdefinierten Wert

## Installation

1. Kopieren Sie den Ordner `custom_components/recurring_reminders` in Ihr Home Assistant `custom_components` Verzeichnis
2. Starten Sie Home Assistant neu
3. Gehen Sie zu Einstellungen → Geräte & Services → Integration hinzufügen
4. Suchen Sie nach "Recurring Reminders"

## Konfiguration

Beim Hinzufügen einer neuen Erinnerung werden Sie nach folgenden Informationen gefragt:

- **Name der Erinnerung**: z.B. "Flur saugen"
- **Intervall in Tagen**: z.B. 7 für wöchentlich

## Verwendung

### Sensoren

Für jede Erinnerung werden zwei Sensoren erstellt:

1. `sensor.recurring_reminders_[name]_interval` - Zeigt das Intervall
2. `sensor.recurring_reminders_[name]_countdown` - Zeigt die verbleibenden Tage

### Services

#### reset_reminder
Setzt den Countdown einer Erinnerung zurück auf das ursprüngliche Intervall.

```yaml
service: recurring_reminders.reset_reminder
data:
  entity_id: sensor.recurring_reminders_flur_saugen_countdown
```

#### set_reminder_days
Setzt den Countdown auf einen benutzerdefinierten Wert.

```yaml
service: recurring_reminders.set_reminder_days
data:
  entity_id: sensor.recurring_reminders_flur_saugen_countdown
  days: 3
```

### Automatisierungen

Sie können Automatisierungen basierend auf den Sensoren erstellen:

```yaml
automation:
  - alias: "Erinnerung Flur saugen"
    trigger:
      - platform: state
        entity_id: sensor.recurring_reminders_flur_saugen_countdown
        to: "0"
    action:
      - service: notify.mobile_app_your_phone
        data:
          message: "Zeit zum Flur saugen!"
          title: "Haushalts-Erinnerung"
```

## Beispiel Dashboard Card

```yaml
type: entities
title: Haushalts-Erinnerungen
entities:
  - entity: sensor.recurring_reminders_flur_saugen_countdown
    name: Flur saugen
    icon: mdi:vacuum
  - entity: sensor.recurring_reminders_bad_putzen_countdown
    name: Bad putzen
    icon: mdi:spray-bottle
```

## Funktionsweise

- Der Countdown wird täglich automatisch um 1 reduziert
- Bei 0 angekommen, bleibt der Wert bei 0 stehen
- Der Service `reset_reminder` setzt den Wert zurück auf das ursprüngliche Intervall
- Der Service `set_reminder_days` erlaubt manuelle Anpassungen für Ausnahmen