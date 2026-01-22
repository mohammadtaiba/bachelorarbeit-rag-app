# RAG-Chatbot

---

## Beschreibung
Ein prototypischer, GPT-basierter Chatbot zur dokumentenbasierten Analyse von Nachhaltigkeitsberichten unter Verwendung eines Retrieval-Augmented-Generation-(RAG)-Ansatzes.

**Fähigkeiten:**

* Verbesserung und Vorschläge von Nachhaltigkeitsstrategien
* Analyse der Inhalte von Nachhaltigkeitsberichten
* Identifikation von Verbesserungspotenzialen
* Entwicklung von Maßnahmen und KPIs
* Branchenbeispiele und Best Practices
* Unterstützung bei Struktur, Sprache und Transparenz

---

## Installationshinweise:

### 1) Systemvoraussetzungen
* Python-Version == 3.11 
* Betriebssystem: Windows
* Ollama-App lokal installieren
* Hinweis: Das Modell `gpt-oss:120b-cloud` wird über Ollama als Cloud-Variante ausgeführt.
  * Es ist keine lokale GPU erforderlich. 


### 2) Modelle lokal installieren & testen
* **Installiere** zuerst Ollama-App auf dem Rechner: https://ollama.com/download

* Um das `gpt-oss:120b-cloud` nutzen zu können, **loge dich zuerst ein**:
````shell
ollama signin
````

* LLM- und Embedding-Modelle **herunterladen**:
````shell
ollama pull gpt-oss:120b-cloud; ollama pull nomic-embed-text
````

* Alle Modelle **anzeigen** (überprüfe, ob beide Modellen installiert wurden):
````shell
ollama list
````

* Ollama starten (falls der Dienst noch nicht gestartet ist oder im Hintergrund minimiert ist)
````shell
ollama serve
````

* Embedding-Modell **testen**:
````shell
Invoke-RestMethod -Uri "http://localhost:11434/api/embeddings" -Method Post -ContentType "application/json" -Body '{"model":"nomic-embed-text","prompt":"Dies ist ein Embedding-Test."}'
````

* LLM-Modell **testen**:
````shell
Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -ContentType "application/json" -Body '{"model":"gpt-oss:120b-cloud","prompt":"Sag Hallo auf Deutsch","stream":false}'
````

---

### 3) Virtuelle Umgebung erstellen und aktivieren
````shell
python -m venv .venv; .venv\Scripts\activate
````

### 4) Packages installieren:
````shell
pip install -r requirements.txt
````

---

### 5) Chatbot (UI) starten:
````shell
streamlit run main.py
````

---

### 6) Hilfsbefehle
* Ingestion starten:
````shell
python -m core.ingestion
````

* ChromaDB löschen:
````shell
Remove-Item -Recurse -Force db/chromadb/*
````

* Packages aktualisieren:
````shell
pip install -r requirements.txt --upgrade --force-reinstall
````

* Modell löschen: 
````shell
ollama rm <MODEL-NAME>
````
