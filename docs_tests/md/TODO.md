# TODO

* [x] "utils/answer_meta_questions.py" anpassen & korrigieren
* [x] **Benutzeroberfläche anpassen:**

> * sidebar entweder entfernen oder anderes besser tun
> * Das Fragefeld sollte immer unten fest angepinnt werden.
> * Fragefelder leeren nach jeder frage
> * Bei der Generation einer Antwort sollte es automatisch nach unter gescrollt werden

* [x] alle PDF-Dokumente laden
* **Retrieval verbessern**
  * [x] Problem: LLM antwortet von seinem Allgemeinem wissen
    * Problem gelöst, durch Verwendung bessere und größere Modell
* [x] MarkdownHeaderTextSplitter verwenden (ohne Grenze von der Tokens oder Buchstaben) + RecursiveCharacterTextSplitter
* [x] Konvertierung von html zu md
* [ ] Data-Input automatisieren
* [ ] Fine-tuning
* [ ] mehrere Modelle zur Auswahl?

* [ ] Antwortqualität messen


---
**Overview:**
- [x] Thema präzisieren und Forschungsfragen formulieren
- [x] Zielsetzung und Abgrenzung schriftlich festhalten
- [ ] Umfassende Literatur- und Technologie-Recherche
- [ ] Gliederung der Arbeit entwickeln
- [ ] Auswahl und Beschreibung der Methodik (RAG, Chunking, Vektor-DB)
- [ ] Aufbau der Pipeline zur Dokumentenkonvertierung (HTML, Word, Excel, PDF → Markdown)
- [ ] Einrichtung der Vektor-Datenbank und Festlegung von Chunk-Größe/Overlap
- [ ] Implementierung und Integration des GPT-basierten Chatbots
- [ ] Untersuchung und Durchführung von Feintuning-Optionen
- [ ] Automatisierung der Wissensbasis-Updates
- [ ] Evaluation (Qualität der Antworten, Performance, Usability)
- [ ] Schlussfolgerungen, Ausblick und fertige Manuskripterstellung