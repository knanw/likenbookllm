## Frontend (vue.js, nuxt, pinia)

### Interface

| Spalte | Bereich       | Funktion                                                                  | Vue-Komponente  |
| ------ | ------------- | ------------------------------------------------------------------------- | --------------- |
| links  | Sidebar       | "Quellenübersicht Dokument-Upload"                                        | SourcePanel.vue |
| mitte  | Hauptbereich  | Chat/Interaktion mit den Quellen und generierte Zusammenfassung/Antworten | ChatView.vue    |
| rechts | Notizen/Infos | allgemeine Informationen                                                  | NotesPanel      |

## Backend (FastAPI, OpenAI, pydantic)

### API-Endpunkte

| Endpoint             | Zweck                       |
| -------------------- | --------------------------- |
| GET /health          | pruefen, ob Backend laeuft  |
| GET /sources         | Quellen laden               |
| POST /sources        | Quelle anlegen              |
| POST /chat           | Userfrage + KI-Antwort      |
| GET /notes           | Notizen laden/aktualisieren |
| DELETE /sources/{id} | Quelle löschen              |

### Anwendung starten:

- backend: uv run uvicorn main:app --reload --port 8000
- frontend: npm run dev
