# Tabben-Planer (GitHub Pages)

Die Seite läuft unter `https://DEINNAME.github.io/tabben-planer/`. Eine GitHub Action holt alle 3 Stunden Dorfliste und Einheitenwerte von de258, die Seite lädt sie beim Öffnen automatisch.

## Einrichten (einmalig, ca. 5 Minuten)

1. Auf github.com ein **neues öffentliches Repository** anlegen, Name z. B. `tabben-planer`.
2. **Dateien hochladen**: „Add file“ → „Upload files“ und den *Inhalt* dieses Ordners hineinziehen (inklusive des Ordners `.github`). Commit.
   Tipp: Der Ordner `.github` ist auf manchen Rechnern versteckt. Notfalls die Datei über „Add file“ → „Create new file“ anlegen, als Name `.github/workflows/update-world.yml` eintippen und den Inhalt einfügen.
3. **Pages einschalten**: Settings → Pages → Source „Deploy from a branch“ → Branch `main`, Ordner `/ (root)` → Save.
4. **Action einmal starten**: Tab „Actions“ → „Weltdaten aktualisieren“ → „Run workflow“. Danach liegen `village.txt` und `unit_info.xml` im Repo.
5. Nach 1–2 Minuten ist die Seite online. Link an die Dualis schicken.

Klappt Schritt 4 mit einer Rechte-Fehlermeldung: Settings → Actions → General → Workflow permissions → „Read and write permissions“.

## Gut zu wissen
- Das Repo und die Seite sind öffentlich. Wer den Link kennt, kann das Tool nutzen; deine Spieldaten fügst du nur im eigenen Browser ein, sie landen nicht auf GitHub. Die eingebauten Testdaten vom 02.08. (de254) enthalten aber Spielernamen aus einer alten SOS.
- Welt wechseln: in `update-world.yml` die Zeile `WORLD: de258` ändern.
- Tool aktualisieren: neue `index.html` hochladen und alte ersetzen.
- GitHub pausiert geplante Actions nach 60 Tagen ohne Repo-Aktivität. Dann im Actions-Tab wieder aktivieren.
