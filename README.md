# BACHELORARBEIT

---

## Thema 
Integration eines GPT-basierten Chatbots zur Beantwortung domänenspezifischer Fragen auf Grundlage einer dynamisch aktualisierten Wissensdatenbank für die Analyse von Nachhaltigkeitsberichten

---

## Motivation

* **Bedarf**: Aktuelle KI-Tools können PDF-basierte Nachhaltigkeitsberichte nicht direkt durchsuchen und verarbeiten.
* **Bibliotheken-Check**: Untersuchung geeigneter Open-Source-Bibliotheken zur Extraktion PDF-/HTML-Dokumenten für die weitere Verarbeitung.
* **Domain-Fokus**: Automatisierte Analyse von Nachhaltigkeitsberichten von Stadtquartieren.

---

## Forschungsfragen
1. Wie kann Dokumentenmaterial wie PDF-Dateien HTML-Seiten aus externen Quellen automatisiert extrahiert, in einer Vektor-Datenbank indexiert und Aktualisierungen der Wissensbasis ohne manuellen Eingriff kontinuierlich integriert werden?
2. Welches Chunking-Konzept (Chunk-Größe und Überlappung) optimiert die Retrieval-Performance im RAG-Kontext?
3. In welchem Maße erhöht Fine-Tuning und Reranking die Qualität der generierten Antworten im Vergleich zu reinem Prompt-Engineering?

---

## Zielsetzung
* Konzeption und prototypische Implementierung einer modularen RAG-Pipeline.
* Automatisierte Transformation heterogener Dokumente in Markdown und Indexierung in einer Vektor-DB.
* Entwicklung einer Web-UI zur interaktiven Frage-Antwort-Nutzung für Nachhaltigkeitsberichte.
* Systematische Evaluation von Chunk-Parametern (Größe, Overlap) und Fine-Tuning vs. Prompt-Engineering.
* Implementierung einer Automatisierungslogik für kontinuierliche Integration neuer Dokumente.

---

## Abgrenzung
#### Nicht Teil der Arbeit sind:
* Die Entwicklung eigener Sprachmodelle; es wird bestehende GPT-Modelle genutzt.
* Es wird nicht geprüft, ob der Inhalt der Dokumente korrekt, aktuell, relevant oder qualitativ hochwertig ist.
* Eine tiefgehende Auseinandersetzung mit rechtlichen, ethischen oder sicherheitstechnischen Aspekten im Zusammenhang mit dem Einsatz generativer KI.

---

## Use Cases des Chatbots
* **Innovative Maßnahmen**: Welche interessanten und innovativen Maßnahmen und Ideen helfen, Nachhaltigkeitsziele im Stadtquartier zu erreichen?
* **Textbaustein-Generierung**: Welche Textbausteine lassen sich automatisiert für Nachhaltigkeitsberichte erstellen, um die Erstellung zu beschleunigen?

---

## Literaturrecherche
### Bücher
- [Building Intelligent Systems with RAG 2.0: Develop Next-Gen LLM Applications with LangChain, OpenAI, Pinecone, FAISS, Vector Databases, and LLMOps Tools.](https://www.amazon.de/gp/product/B0F91NZQVF/ref=ox_sc_saved_image_1?smid=A3JWKAKR8XB7XF&psc=1)
- [AI Prompt Engineering Bible (7 Books in 1): Beginner-to-Pro System to Master ChatGPT and Generative AI for Powerful Results and Real Income.](https://www.amazon.de/Prompt-Engineering-Bible-Books-Beginner/dp/B0FHFL61PB/ref=sr_1_1?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&sr=8-1)

### Wissenschaftliche Fachartikeln für die Forschungsfragen

1. Dokumententransformation & Automatisierung

    **Fachartikel 1**: 

    **Fachartikel 2**: 
 

2. Chunking-Konzept
   
    **Fachartikel 1**: [arxiv: Chunk-Größe](https://arxiv.org/pdf/2505.21700)

    **Fachartikel 2**: 
 
 
3. Fine-Tuning vs. Prompt-Engineering
   
    **Fachartikel 1**: 

    **Fachartikel 2**: [arxiv: Reranking](https://arxiv.org/pdf/2507.12378)

    **Fachartikel 3**:

### Offizielle Dokumentationen

- [**llamaindex**](https://docs.llamaindex.ai/en/stable/getting_started/concepts/)
  - [**RAG-Understanding**](https://docs.llamaindex.ai/en/stable/understanding/rag/)

### Online-Ressourcen
- [**Coursera-Project:** Generative AI Applications with RAG and LangChain](https://www.coursera.org/learn/project-generative-ai-applications-with-rag-and-langchain)



---

## Domain

### Ideen:

#### 1. Kundensupport
* Intelligente Beantwortung von Nutzerfragen zu Produkten und Services anhand von Handbüchern, FAQs und Support-Tickets

#### 2. Produktions- und Fertigungsindustrie
* Unterstützung bei technischen Fragen zu Prozessen, Maschinenwartung und Qualitätsstandards.

#### 3. Tourismus und Kultur
* Auskunft zu Sehenswürdigkeiten, Routen und kulturellen Hintergründen auf Basis von Reiseführern und Webseiten.

#### 4. Gesundheitswesen
* Beantwortung medizinischer Fachfragen auf Basis von Leitlinien, Studien und Patientenbroschüren.

#### 5. Rechtliche Fachberatung
* Automatisierte Beantwortung von Fragen zu Gesetzen, Verträgen und Urteilen mithilfe einer dynamischen Datenbank aus Rechtsdokumenten


### Entscheidung

#### Kundensupport, weil

- Praxisrelevanz
- Verfügbarkeit heterogener Dokumente
- Bewertbarkeit


---

## Folder Structure
 ```
rag2-app/
│
├── .env                 # Environment variables
├── main.py              # Entrypoint
├── ingestion.py         # Document loading and embedding
├── retrieval.py         # Vector store and query logic
├── interface.py         # Streamlit or Gradio front-end
├── utils/               # Utility functions
└── data/                # Raw documents
````


