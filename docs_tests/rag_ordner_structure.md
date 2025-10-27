# Ordnerstruktur: 
```
rag2-app/
│
├── .gitignore
├── .env
├── requirements.txt         # Python-Abhängigkeiten
├── main.py                  # Startpunkt (Streamlit + RAG)
│
├── core/
│   ├── __init__
│   ├── ingestion.py         # md-Dateien laden + indexieren
│   ├── config.py            # Globale Variablen
│   └── retrieval.py         # Anfrage beantworten
│
├── data/
│   ├── raw/                 # enthält alle Dateien
│   ├── upload/              # enthält alle neue Dateien
│   └── markdown/            # enthält die konvertierte markdown-dateien (automatisch generiert)            
│
├── units/
│   ├── __init__
│   ├── chunking.py
│   ├── lmstudio_embed.py
│   ├── loaders.py
│   ├── cleanup_md.py
│   └── raw2markdown.py
│
└── db/
    └── chromadb/            # Vektor-Datenbank (automatisch generiert)
