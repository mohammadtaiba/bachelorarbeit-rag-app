## Modelle:
- installiere zuerst Ollama-App auf dem Rechner: 
> https://ollama.com/download
- Um das `gpt-oss:120b-cloud` nutzen zu können, loge dich zuerst ein:
> ollama signin
- Modell herunterladen:
> ollama pull gpt-oss:120b-cloud
- Alle Modellen anzeigen:
> ollama list
- Modell löschen: 
> ollama rm <MODEL-NAME>

### Test Embedding, führe das im terminal:
Invoke-RestMethod `
  -Uri "http://localhost:11434/api/embeddings" `
  -Method POST `
  -Body '{"model":"nomic-embed-text","prompt":"Dies ist ein Embedding-Test."}' `
  -ContentType "application/json"

### Test LLM, führe das im terminal:
Invoke-RestMethod `
  -Uri "http://localhost:11434/api/generate" `
  -Method POST `
  -Body '{"model":"llama3","prompt":"Sag Hallo auf Deutsch","stream":false}' `
  -ContentType "application/json"

---

## Andere Befehlen
> python docs_notes/Testing_Learning/test_chromaDB_overview.py
---
> python -m core.ingestion
---
> Remove-Item -Recurse -Force db/chromadb/*
---
> streamlit run main.py

---

## venv erstellen & aktivieren
> python -m venv .venv
---
> .venv\Scripts\activate

---
## installiere packeges:
> pip install -r requirements.txt
---
> pip install -r requirements.txt --upgrade --force-reinstall
