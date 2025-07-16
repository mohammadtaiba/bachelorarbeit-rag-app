# Bahelorarbeit

---

## Thema 
Integration eines GPT-basierten Chatbots zur Beantwortung domänenspezifischer Fragen auf Grundlage einer dynamisch aktualisierten Wissensdatenbank

## Forschungsfragen
* Wie kann heterogenes Dokumentenmaterial (HTML, Word, Excel, PDF) automatisiert in ein einheitliches Markdown-Format überführt und in einer Vektor-Datenbank indexiert werden?
* Welches Chunking-Konzept (Chunk-Größe und Überlappung) optimiert die Retrieval-Performance im RAG-Kontext?
* In welchem Maße erhöht Fine-Tuning die Qualität der generierten Antworten im Vergleich zu reinem Prompt-Engineering?
* Wie kann die Pipeline so automatisiert werden, dass Aktualisierungen der Wissensbasis ohne manuellen Eingriff kontinuierlich integriert werden?

## Zielsetzung & Abgrenzung

### Zielsetzung
* Konzeption und prototypische Implementierung einer modularen RAG-Pipeline.
* Automatisierte Transformation heterogener Dokumente in Markdown und Indexierung in einer Vektor-DB.
* Entwicklung einer Web-UI zur interaktiven Frage-Antwort-Nutzung.
* Systematische Evaluation von Chunk-Parametern (Größe, Overlap) und Fine-Tuning vs. Prompt-Engineering.
* Implementierung einer Automatisierungslogik für kontinuierliche Integration neuer Dokumente.

### Abgrenzung
#### Nicht Teil der Arbeit sind:
* Die Entwicklung eigener Sprachmodelle; es wird bestehende GPT-Modelle genutzt.
* Es wird nicht geprüft, ob der Inhalt der Dokumente korrekt, aktuell, relevant oder qualitativ hochwertig ist.
* Eine tiefgehende Auseinandersetzung mit rechtlichen, ethischen oder sicherheitstechnischen Aspekten im Zusammenhang mit dem Einsatz generativer KI.


## Literaturrecherche
1. [**Amazon-Buch**: Building Intelligent Systems with RAG 2.0](https://www.amazon.de/gp/product/B0F91NZQVF/ref=ox_sc_saved_image_1?smid=A3JWKAKR8XB7XF&psc=1)

## Online-Ressourcen
1. [**Coursera-Project:** Generative AI Applications with RAG and LangChain](https://www.coursera.org/learn/project-generative-ai-applications-with-rag-and-langchain)

---

## Domain-Ideen

### 1. Kundensupport
* Intelligente Beantwortung von Nutzerfragen zu Produkten und Services anhand von Handbüchern, FAQs und Support-Tickets

### 2. Produktions- und Fertigungsindustrie
* Unterstützung bei technischen Fragen zu Prozessen, Maschinenwartung und Qualitätsstandards.

### 3. Tourismus und Kultur
* Auskunft zu Sehenswürdigkeiten, Routen und kulturellen Hintergründen auf Basis von Reiseführern und Webseiten.

### 4. Gesundheitswesen
* Beantwortung medizinischer Fachfragen auf Basis von Leitlinien, Studien und Patientenbroschüren.

### 5. Rechtliche Fachberatung
* Automatisierte Beantwortung von Fragen zu Gesetzen, Verträgen und Urteilen mithilfe einer dynamischen Datenbank aus Rechtsdokumenten



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


