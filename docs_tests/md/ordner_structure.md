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
│   ├── ingestion.py                # md-Dateien laden + indexieren
│   ├── preprocess.py               # Globale Variablen und Parameter
│   └── retrieval.py                # Benutzeranfragen beantworten (RAG)
│ 
├── data/ 
│   ├── raw/                        # Originaldokumente
│   ├── upload/                     # Neu hochgeladene Dokumente
│   ├── temp_markdown/              # speichert die konvertierte markdown-dateien (temporär)
│   └── markdown/                   # speichert die konvertierte markdown-dateien (automatisch generiert)            
│
├── units/
│   ├── __init__
│   ├── chunking.py                 # Chunking mit Metadaten-Erweiterung
│   ├── lmstudio_embed.py           # Brückenmodul für lokale LM Studio Embeddings
│   ├── cleanup_md.py               # Markdown-Bereinigung
│   ├── file_operation.py           # Verschiebung & Bearbeitung von Dateien
│   ├── answer_meta_questions.py    # Lokale Antworten auf triviale Fragen (ohne LLM)
│   ├── next_neighbor_retriever.py  # Rückgabe benachbarter Chunks im Retrieval
│   ├── loaders.py                  # Markdown-Dateien laden
│   └── raw2markdown.py             # Konvertierung von Rohdaten zu Markdown
│
└── db/
    └── chromadb/                   # Vektor-Datenbank (automatisch generiert)
