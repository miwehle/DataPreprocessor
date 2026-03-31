# AGENTS.md

Fuer dieses Repository gelten auch die Regeln aus `../translator/AGENTS.md`.

Kurzfassung der Regeln:
- Vor nicht-trivialen Production-Aenderungen kurz Aenderungsplan nennen und Go einholen.
- Keine stillschweigende Code-Duplizierung; Hilfslogik nur bei echter Wiederverwendung.
- Python kompakt schreiben: positionale Parameter bevorzugen, nicht vorschnell umbrechen.
- Ruff-Konfiguration in pyproject.toml beachten, insbesondere line-length und Stilregeln.
- Tests klar benennen; Fokus auf oeffentliche API, Integrationstests getrennt halten.
- Temp-Dateien und Test-Artefakte nur unter `.local_tmp/` im Repo-Root anlegen.