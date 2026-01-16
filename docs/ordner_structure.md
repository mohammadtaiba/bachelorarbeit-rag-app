# Ordnerstruktur: 
```
rag2-app/
│
├── .gitignore
├── .env                            # Globale Variablen und Parameter (gekapselt)
├── requirements.txt                # Python-Abhängigkeiten
├── main.py                         # Startpunkt (Streamlit + RAG)
├── outputDB.py                     # Indexierte Inhalte der ChromaDB als MD-Datei ausgeben
├── automation.py                   # Hilfsdatei, um einfach und schnell Prozesse wie Ingestion oder UI zu starten
│
├── core/ 
│   ├── __init__        
│   ├── ingestion.py                # Dateien nach MD-Dateien konvertieren --> bereinigen --> in VektorDB indexieren
│   ├── config.py                   # Globale Variablen und Parameter
│   ├── retrieval.py                # Benutzeranfragen beantworten (RAG)
│   └── dnk_urls_automation/  
│          ├──  scrape_dnk_urls.py          # 1. Schritt: Gültige DNK-URL  finden und in einer Datei speichern
│          ├──  extract_dnk_urls.py         # 2. Schritt: Untermenüpunkte aus dem Hauptmenüpunkt extrahieren
│          └──  dnk_urls_2_md.py            # 3. Schritt: Inhalt der extrahierte URLs als MD-Datei speichern
│ 
├── data/
│   ├──  raw                        # Rohdateien hier manuell speichern
│   ├──  upload                     # Neue Dateien hier schieben/kopieren
│   ├──  processing                 # MD-Dateien hier temporär speichern
│   ├──  processed                  # MD-Dateien hier endgültig speichern (nach der Konvertierung & Bereinigung)
│   └──  url_sources/ 
│          ├──  dnk_2024_individually.txt   # Die gefundene URLs aus `scrape_dnk_urls`
│          └──  dnk_2024_all.txt            # Die extrahierte URLs aus `extract_dnk_urls.py`
│
├── units/
│   ├── __init__
│   ├── chunking.py                 # Chunking mit Metadaten-Erweiterung
│   ├── ollama_embed.py             # Brückenmodul für lokale LM Studio Embeddings
│   ├── manage_files.py             # Konvertierung & Verschiebung & Bearbeitung von Dateien
│   ├── answer_meta_questions.py    # Identitätsfragen & Begrüßung automatisch beantworten ohne LLM
│   ├── loaders.py                  # Markdown-Dateien laden (Beim Ingestion)
│   ├── logger.py                   # Um logging-Nachrichten in einer Logdatei zu speichern
│   └── watchdog.py                 # überwacht `upload`-Ordner, ob neue Dateien gibt
│
├── logs/
│   ├── chroma_output.md            # Ausgegebene MD-Datei für die Inhalt der ChomaDB
│   └── rag_bot.log                 # LOG-Datei (Automatisch erzeugt)
│
├── test/
│   ├── conftest.py                 # Konfigurationseinstellung für die Test-Datei
│   ├── Test Results - .html        # Test-Ergebnisse
│   └── test_llm_response.py        # Erwartete LLM-Antworten oder -Verhalten testen
│
└── db/
    └── chromadb/                   # VectorDB-Datei (Automatisch erzeugt)