# Ordnerstruktur: 
```
mini_lusd_bot/
│
├── .gitignore
├── .env
├── requirements.txt         # Python-Abhängigkeiten
├── main.py                  # Startpunkt (Streamlit + RAG)
│
├── core/
│   ├── __init__
│   ├── ingestion.py         # Doku laden + indexieren
│   ├── config.py
│   └── retrieval.py         # Anfrage beantworten
│
├── data/
│   ├── raw/                # enthält alle Dateien
│   └── markdown/           # enthält die konvertierte markdown-dateien                
│
├── units/
│   ├── __init__
│   ├── chunking.py
│   ├── lmstudio_embed.py
│   ├── loaders.py
│   └── ...
│
└── db/
    └── chromadb/            # Vektor-Datenbank (automatisch generiert)
