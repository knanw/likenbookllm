import os
from datetime import datetime, UTC
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel
from contextlib import asynccontextmanager

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_sources()  # Befüllt die Testdaten beim Start
    yield

# Hier wird der Lifespan-Handler registriert:
app = FastAPI(title="Notebook Lite API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False, 
    allow_methods=["*"],      
    allow_headers=["*"],      
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


class SourceCreate(BaseModel):
    title: str
    content: str


class Source(BaseModel):
    id: str
    title: str
    content: str
    created_at: str


class ChatRequest(BaseModel):
    message: str
    source_ids: list[str]


class ChatResponse(BaseModel):
    answer: str
    notes: list[str]


SOURCES: list[Source] = []


def seed_sources():
    if SOURCES:
        return

    SOURCES.extend([
        Source(
            id=str(uuid4()),
            title="Kaffee-Roboter RoboBrew 3000",
            content=(
                "Das Modell RoboBrew 3000 ist unser neuester Kaffee-Roboter. "
                "Er verfügt über einen Wassertank von 5 Litern und kann bis zu 40 Espresso-Tassen pro Stunde kochen. "
                "Wichtig: Der Roboter darf NIEMALS mit Milch im Wassertank befüllt werden, da dies die internen Düsen dauerhaft verstopft. "
                "Die Reinigung erfolgt ausschließlich über das eingebaute Dampfprogramm 'CleanMax'."
            ),
            created_at=datetime.now(UTC).isoformat(),
        ),
        Source(
            id=str(uuid4()),
            title="Garantiebestimmungen RoboBrew",
            content=(
                "Die Garantie für den RoboBrew 3000 beträgt standardmäßig 24 Monate. "
                "Sie erlischt sofort, wenn Schäden durch Fremdeflüssigkeiten (wie Sirup oder Milch) im Hauptwassertank entstehen. "
                "Für gewerbliche Nutzung in Gastronomien verkürzt sich die Garantiezeit auf 12 Monate."
            ),
            created_at=datetime.now(UTC).isoformat(),
        ),
    ])


def get_sources_by_ids(source_ids: list[str]):
    return [source for source in SOURCES if source.id in source_ids]


def build_context(source_texts: list[dict]) -> str:
    if not source_texts:
        return "Keine Quellen ausgewaehlt."

    parts = []
    for source in source_texts:
        parts.append(f"Quelle: {source['title']}\nInhalt: {source['content']}")
    return "\n\n".join(parts)


def generate_answer(message: str, sources: list[dict]) -> tuple[str, list[str]]:
    if client is None:
        raise ValueError("OPENAI_API_KEY fehlt. Bitte in der .env setzen.")

    context = build_context(sources)

    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": (
                    "Du bist ein hilfreicher Assistent fuer eine Recherche-App. "
                    "Antworte klar und moeglichst nur auf Basis der gegebenen Quellen. "
                    "Wenn Informationen fehlen, sage das offen."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Quellenkontext:\n{context}\n\n"
                    f"Frage:\n{message}\n\n"
                    "Strukturiere die Antwort klar und verstaendlich."
                ),
            },
        ],
    )

    answer = completion.choices[0].message.content or "Keine Antwort erhalten."

    notes = [
        "Antwort basiert auf den aktuell ausgewaehlten Quellen.",
        f"Verwendete Quellen: {len(sources)}",
        "MVP ohne semantisches Retrieval.",
    ]

    return answer, notes


# @app.on_event("startup")
# def startup_event():
#     seed_sources()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "openai_configured": bool(OPENAI_API_KEY),
    }


@app.get("/sources")
def get_sources():
    return SOURCES


@app.post("/sources")
def post_source(payload: SourceCreate):
    if not payload.title.strip():
        raise HTTPException(status_code=400, detail="Titel darf nicht leer sein.")

    if not payload.content.strip():
        raise HTTPException(status_code=400, detail="Inhalt darf nicht leer sein.")

    source = Source(
        id=str(uuid4()),
        title=payload.title.strip(),
        content=payload.content.strip(),
        created_at=datetime.now(UTC).isoformat(),
    )
    SOURCES.append(source)
    return source


@app.delete("/sources/{source_id}")
def remove_source(source_id: str):
    global SOURCES
    before = len(SOURCES)
    SOURCES = [source for source in SOURCES if source.id != source_id]

    if len(SOURCES) == before:
        raise HTTPException(status_code=404, detail="Quelle nicht gefunden.")

    return {"success": True}


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Nachricht darf nicht leer sein.")

    sources = get_sources_by_ids(payload.source_ids)

    try:
        answer, notes = generate_answer(
            message=payload.message.strip(),
            sources=[source.model_dump() for source in sources],
        )
        return ChatResponse(answer=answer, notes=notes)
    except Exception as exc:

        # HIER: Das zwingt Python, den echten Fehler ins Terminal zu schreiben!
        import traceback
        print("\n" + "="*50)
        print("DER ECHTE FEHLER IM BACKEND:")
        traceback.print_exc()
        print("="*50 + "\n")

        raise HTTPException(
            status_code=500,
            detail=f"Fehler bei der Modellanfrage: {str(exc)}",
        )
