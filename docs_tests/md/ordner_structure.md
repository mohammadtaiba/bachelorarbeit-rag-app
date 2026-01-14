# Ordnerstruktur: 
```
rag2-app/
│
├── .gitignore
├── .env                            # Globale Variablen und Parameter (gekapselt)
├── requirements.txt                # Python-Abhängigkeiten
├── main.py                         # Startpunkt (Streamlit + RAG)
│ 
├── core/ 
│   ├── __init__        
│   ├── ingestion.py              	# Dateien nach MD-Dateien konvertieren --> bereinigen --> in VektorDB indexieren
│   ├── preprocess.py             	# Globale Variablen und Parameter
│   ├── retrieval.py              	  # Benutzeranfragen beantworten (RAG)
│   └── dnk_urls_automation/  
│          ├──  scrape_dnk_urls.py # Erster Schritt: Die gültige URL von „www.deutscher-nachhaltigkeitskodex.de” finden und in einer Datei speichern (Hauptmenüpunkt finden).
│          ├──  extract_dnk_urls.py # Zweiter Schritt: Die Untermenüpunkte aus dem Hauptmenüpunkt extrahieren.
│          └──  dnk_urls_2_md.py # Die URLs als Markdown-Datei für jedes Unternehmen separat speichern.
│ 
├── data/
│   ├──  raw						# Rohdateien hier manuell speichern
│   ├──  upload					# Neue Dateien hier schieben/kopieren
│   ├──  processing			# Die MD-Dateien hier temporär speichern
│   ├──  processed	           # Die MD-Dateien hier endgültig speichern nach der Konvertierung und Bereinigung
│   └──  url_sources/ 
│          ├──  dnk_2024_individually.txt # Die gefundene URLs aus `scrape_dnk_urls`
│          └──  dnk_2024_all.txt # Die extrahierte URLs aus `extract_dnk_urls.py`
│
├── units/
│   ├── __init__
│   ├── chunking.py                 # Chunking mit Metadaten-Erweiterung (MarkdownHeaderTextSplitter & RecursiveCharacterTextSplitter)
│   ├── ollama_embed.py             # Brückenmodul für lokale LM Studio Embeddings
│   ├── manage_files.py             # Konvertierung & Verschiebung & Bearbeitung von Dateien
│   ├── answer_meta_questions.py    # Identitätsfragen & Begrüßung automatisch beantworten ohne LLM
│   ├── loaders.py                  # Markdown-Dateien laden (Beim Ingestion)
│   ├── logger.py					# logging-Nachrichten in rag_bot.log speichern
│   └── watchdog.py					# überwacht `upload`-Ordner, ob neue Dateien gibt
|
├── logs/
│   └── rag_bot.log
│
└── db/
    └── chromadb/