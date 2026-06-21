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

## Test

#### 1.Quelle anlegen

- Titel: Kaffee-Roboter RoboBrew 3000
- Text: Das Modell RoboBrew 3000 ist unser neuester Kaffee-Roboter. Er verfügt über einen Wassertank von 5 Litern und kann bis zu 40 Espresso-Tassen pro Stunde kochen. Wichtig: Der Roboter darf NIEMALS mit Milch im Wassertank befüllt werden, da dies die internen Düsen dauerhaft verstopft. Die Reinigung erfolgt ausschließlich über das eingebaute Dampfprogramm 'CleanMax'.

#### 2.Quelle anlegen

- Titel: Garantiebestimmungen RoboBrew
- Text: Die Garantie für den RoboBrew 3000 beträgt standardmäßig 24 Monate. Sie erlischt sofort, wenn Schäden durch Fremdeflüssigkeiten (wie Sirup oder Milch) im Hauptwassertank entstehen. Für gewerbliche Nutzung in Gastronomien verkürzt sich die Garantiezeit auf 12 Monate.

#### 4. Testfragen Chat

##### Test allgemein

- Was ist 3 + 4?
- 7

##### Test Detailwissen

- Wie viel Wasser passt in den RoboBrew 3000 und wie wird er gereinigt?
- 5 Litern und mit dem 'CleanMax'-Programm

##### Test Einschränkungen

- Darf ich Mandelmilch in den Wassertank füllen?
- Die KI sollte dich anhand der Quellen direkt warnen, dass dadurch die Düsen verstopfen und die Garantie erlischt.

##### Test Halluzinationen

- Welche Farbe hat der Roboter und wie viel kostet er?
- Dazu liegen mir keine Informationen in den Quellen vor.
