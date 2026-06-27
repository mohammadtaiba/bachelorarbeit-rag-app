# RAG-Bot für Nachhaltigkeitsberichte

![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20DB-13B5EA)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-000000?logo=ollama&logoColor=white)
![Bachelorarbeit](https://img.shields.io/badge/Bachelorarbeit-RAG--System-4A90E2)

Interaktive Streamlit-Anwendung zur Analyse von Nachhaltigkeitsberichten auf Basis von Retrieval-Augmented Generation (RAG). Die App kombiniert Dokumentenverarbeitung, semantische Suche und eine Chat-Oberfläche mit Quellenbezug.

Das Projekt wurde im Rahmen einer Bachelorarbeit entwickelt und untersucht, wie RAG-Ansätze die Auswertung und Verbesserung von Nachhaltigkeitsberichten unterstützen können.

## Projektziel

Ziel ist es, Nachhaltigkeitsberichte schnell, nachvollziehbar und strukturiert auszuwerten. Die Anwendung soll nicht nur Antworten liefern, sondern den Analyseprozess transparent machen: Welche Quelle wurde verwendet? Welche Informationen sind relevant? Welche nächsten Fragen lohnen sich?

## Funktionsumfang

- Chatbasierte Frage-Antwort-Oberfläche für Nachhaltigkeitsberichte
- Automatische Verarbeitung neuer Dateien im Upload-Ordner
- Dokumentenimport, Extraktion, Chunking und Vektorisierung
- Retrieval mit Kontext aus der lokalen ChromaDB
- Antworten mit Quellenbezug und Markdown-Ausgabe
- Vorschläge für ähnliche Folgefragen
- Logging und Fehlerbehandlung für den laufenden Betrieb
- Klare Trennung von UI, Core-Logik und Hilfsfunktionen

## Screenshots

### Chat-Oberfläche

<img src="docs/screenshots/input-output-example.png" alt="Chat-Oberfläche mit Antwort und Quellenbezug" width="900">

Die Ansicht zeigt eine typische Frage mit tabellarisch aufbereiteter Antwort, Quellenhinweisen und einem Vorschlag für eine ähnliche Folgefrage.

### Systemarchitektur

<img src="docs/screenshots/bachelor_architektur.png" alt="Systemarchitektur des RAG-Bots" width="900">

Die Grafik zeigt den Ablauf von der Dokumentenverarbeitung über Embeddings und Vektordatenbank bis zur Antwortgenerierung mit Quellenbezug.

## Tech Stack

| Bereich | Technologie |
|---|---|
| Oberfläche | Streamlit |
| Sprache | Python 3.11 |
| RAG / LLM | LangChain, LangChain-Ollama, Ollama |
| Vektor-Datenbank | ChromaDB |
| Dokumentenverarbeitung | pandas, beautifulsoup4, markdownify, markitdown |
| Konfiguration | python-dotenv |
| Automatisierung | watchdog |
| Tests | pytest |

## Projektstruktur

```text
bachelorarbeit-rag-app/
├── core/
├── utils/
├── data/
├── docs/
├── test/
├── main.py
├── automation.py
└── README.md
```

## Voraussetzungen

- Windows oder ein kompatibles Python-Setup
- Python 3.11
- Ollama installiert und gestartet
- Eine `.env`-Datei mit den lokalen Pfaden und Modellnamen
- Die vorbereitete DB-Struktur im Projektordner

## Lokaler Start

### 1) Virtuelle Umgebung erstellen

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2) Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 3) Datenbasis bereitstellen

Die vorbereitete DB-ZIP-Datei entpacken und den Ordner als `db` im Projektverzeichnis ablegen.

### 4) Ollama-Modelle prüfen

Die genauen Modellnamen stehen in `.env`. Beispiel:

```bash
ollama signin
ollama pull gpt-oss:120b-cloud
ollama pull nomic-embed-text
ollama pull qwen3-embedding:8b
ollama list
```

### 5) App starten

```bash
streamlit run main.py
```


## Hinweise

- Die konkrete Modell- und Pfadkonfiguration wird über `.env` gesteuert.
- Die Anwendung ist für lokale Ausführung und Demonstration ausgelegt.
