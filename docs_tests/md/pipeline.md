# Gesamtablauf

---

### **1️⃣ Dokumentenverarbeitung**

**Dokumente laden, bereinigen und in Markdown (MK) umwandeln**
→ *Quellformate:* pdf, html, docx, xlsx
→ *Tool:* LangChain

---

### **2️⃣ Chunking (LangChain)**

* Alle **800 Tokens mit 100 Token Overlap**

---

### **3️⃣ vor Embedding, Metadaten in DB hinzufügen:**

* Chunk-ID
* Dokument-ID
* Upload-Datum
* Vektor
* Typ
* Dokumentname
* Jahr
* Anzahl der Seiten
* Seitenbereich

---

### **4️⃣ Embedding (OpenAI)**

→ Vektorisierung der Chunks

---

### **5️⃣ Indexierung (ChromaDB)**

→ Speicherung: *Text + Embedding + Metadaten*

---

### **6️⃣ Query-Rewriting (OpenAI)**

**Zwei Arten:**

1. **Multi-Query:** Das LLM erzeugt mehrere alternative Formulierungen derselben Frage.
2. **HyDE (Hypothetical Document Embeddings):**
   Das LLM simuliert eine hypothetische Antwort auf die Frage
   und verwendet diese Antwort als Suchtext für das Retrieval.

---

### **7️⃣ Hybrid-Retrieval (LangChain)**

* Kombination aus **BM25 + Vektor**
* **Ranking** (im Retriever)
* **Re-Ranking** (mit OpenAI)

---

### **8️⃣ RAG-Backend (OpenAI)**

* Prompt-Engineering
* Antwort generieren

---

### **9️⃣ Frontend (Streamlit)**

* Registrierung, Login, Chatverlauf
* *Admin-Rolle für Verwaltung der Dokumente*

---

### **10 Finetuning**

* Auf spezifische Fragen trainieren
* *Automatisch extrahieren mit OpenAI*
* Danach *manuelle Qualitätskontrolle durchführen*

---

### **11 Automatische Aktualisierung der Dokumente**

* Mit *watchdog (Python-Bibliothek)*

---

### **12 Evaluation & Antwortqualität**

#### 12.1. **Antwortqualität messen**

→ *Evaluation-Seite mit Streamlit entwickeln*
→ *Messen bei:*

* Query-Rewriting
* Kombination im Hybrid-Retrieval
* Prompt-Engineering
* Chunking
* Geschwindigkeit bei mehreren Anfragen


#### 12.2. **Testliste als CSV anlegen**

* Enthält *Fragen + Quelle/Antwort*


#### 12.3. **Automatisierte Datensammlung**

Die Daten werden automatisiert tabellarisch gesammelt + mit Bewertungsbuttons:

* Antwortdauer (ms)
* Richtige Dokumente gefunden?
* Richtige Antwort gegeben?
* Anzahl der Tokens
* Manuelle Bewertung (1–5 Sterne)


#### 12.4. **Am Ende erhalten wir eine Statistik:**

* **Trefferquote (Hit@k):** wie oft das richtige Dokument unter den besten 5 war
* **Durchschnittliche Antwortzeit**
* **Gesamtbewertung**
* **CSV-Export** → für Vergleich *vor/nach Update*