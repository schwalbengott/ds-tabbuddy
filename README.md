# DS TabBuddy

Tabben-Planer für Die Stämme: legt kleine Deff-Pakete exakt in die Lücken zwischen eingehende Angriffe.

**Seite:** https://schwalbengott.github.io/ds-tabbuddy/
**Direktlink für eine Welt:** https://schwalbengott.github.io/ds-tabbuddy/?w=de258

## Wie es funktioniert
- `index.html` ist das ganze Tool. Es rechnet komplett im Browser; eingefügte Spieldaten verlassen den Browser nicht.
- Die Action `Weltdaten aktualisieren` läuft alle 6 Stunden und schreibt nach `worlds/`:
  - `index.json`: alle Welten von die-staemme.de mit Geschwindigkeit, Einheiten, Laufzeiten, Deffwerten, Millisekunden ja/nein
  - `<welt>/village.txt`: Dorf-IDs (gekürzt auf `id,,x,y`)
- Beim Öffnen wählt man die Welt, alles Weitere stellt sich danach ein.

## Dateien
| Datei | Zweck |
|---|---|
| `index.html` | das Tool |
| `tools/update_worlds.py` | holt Weltliste und Weltdaten |
| `.github/workflows/update-worlds.yml` | startet das Skript zeitgesteuert |
| `worlds/` | wird von der Action erzeugt, nicht von Hand bearbeiten |

## Wartung
- Tool aktualisieren: neue `index.html` hochladen.
- Weltdaten sofort holen: Actions → „Weltdaten aktualisieren“ → „Run workflow“.
- GitHub pausiert geplante Actions nach 60 Tagen ohne Aktivität im Repo; dann im Actions-Tab wieder aktivieren.
