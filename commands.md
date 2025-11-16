## Modelle:
- "installiere zuerst dem Modell auf dem Rechner": https://ollama.com/download
- ollama pull llama3
- - ollama pull llama3:70b
- ollama pull nomic-embed-text
- "Alle Modellen anzeigen": ollama list
- "Modell löschen": ollama rm <MODEL-NAME>

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



### others
> python docs_notes/Testing_Learning/test_chromaDB_overview.py
---
> python -m core.ingestion
---
> Remove-Item -Recurse -Force db/chromadb/*
---
> streamlit run main.py