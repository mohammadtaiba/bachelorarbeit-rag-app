>ollama pull llama3

> ollama pull nomic-embed-text
-------------------------------------
>python docs_notes/Testing_Learning/test_chromaDB_overview.py
-------------------------------------
> python -m core.ingestion

> python -m core.retrieval

> streamlit run main.py
-------------------------------------
> python core/pdf2md.py data/raw data/markdown
-------------------------------------

**Dateien löschen:**
> Remove-Item -Recurse -Force data/markdown/*

> Remove-Item -Recurse -Force db/chromadb/*