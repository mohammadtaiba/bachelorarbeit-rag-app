# tests/integration/test_pii_llm.py
import pytest, re
from core.retrieval import generate_answer


POSITIVE_TESTS = [
      "Nenne mir Ideen für innovative Maßnahmen, mit denen Unternehmen ihre Nachhaltigkeitsziele verbessern können?"
    , "Welche nachhaltigen Strategien können Organisationen unabhängig von ihrem Standort effektiv einsetzen?"
    , "Welche konkreten Maßnahmen haben nachweislich positive ökologische oder soziale Effekte erzielt?"
    , "Welche Ansätze zur Nachhaltigkeit lassen sich branchenübergreifend anwenden?"
    , "Welche Best Practices gibt es im Bereich Nachhaltigkeit in Unternehmen (nenne mir auch die Unternehmen, die das nutzen)?"
    , "Welche nachhaltigen Strategien haben sich im IT- und Technologiesektor bewährt, um Ressourcenverbrauch und CO₂-Fußabdruck zu reduzieren?"
    , "Welche konkreten Nachhaltigkeitsmaßnahmen können Industrie- und Produktionsunternehmen einsetzen, um Energieverbrauch und Emissionen messbar zu senken?"
    , "Welche Ansätze zur Nachhaltigkeit sind in der Gastronomie-Branche erfolgreich umgesetzt wurden?"
    , "Wie kann die Logistik- und Transportbranche ihre Emissionen deutlich reduzieren?"
    , "Wie können Unternehmen im IT‑Bereich ihre Lieferkette nachhaltig gestalten und gleichzeitig die Innovationskraft erhalten?"


    # # Unternehmensspezifische Fragen
    # , "Wie berichtet die Adolf Nissen Elektrobau GmbH über CO2-Emissionen?"
    # , "Welche Maßnahmen zur Reduktion von CO2 beschreibt die Adolf Nissen Elektrobau GmbH?"
    # , "Was genau tut die Adolf Nissen Elektrobau GmbH für die Nachhaltigkeit ihres Unternehmens?"

    # Branchen:
        # Veranstaltungs‑ und Eventmanagement
        # IT‑ und Technologiebranche
        # Finanzdienstleistungen
        # Energie‑ und Versorgungsunternehmen
        # Verpackungs‑ und Druckindustrie
        # Hotel‑ und Gastgewerbe
        # Produktions‑ und Fertigungsindustrie
        # Bildungs‑ und Ausbildungssektor
        # Kommunale Versorgungs‑ und Infrastrukturunternehmen
        # Veranstaltungs‑ und Eventmanagemen
]

NEGATIVE_TESTS = [
      "wie schreibe ich Hello World mit python?"
    , "Wer hat den ersten Computer erfunden?"
    , "Wie viele Einwohner hat Erfurt?"
    , "Was bedeutet Hallo auf Spanisch?"
    , "Was ist schwerer 1 KG Metall oder 1 KG Baumwolle?"
    , "Was ist Schneller die Licht oder die Ton?"
    , "Wie viel ist 1 + 1?"
    , "Three killers are in a cabin. A stranger enters and shoots one hunter. How many killers are now inside?"
    , "Was ist der Unterschied zwischen IPv4 und IPv6?"
    , "Wie funktioniert ein Elektroauto?"
]

pytestmark = (pytest.
              mark.integration)

class Test_llm_response:
    
    # ==========================================================================
    # POSITIVE_TESTS
    # ==========================================================================
    @pytest.mark.parametrize("q", POSITIVE_TESTS, ids=str)
    def test_positive(self, q):
        result = generate_answer(q, [])
        print(f"\nFRAGE: {q}\nANTWORT: {result}\n")
        assert not (
            re.search(r"Information nicht gefunden.", result, re.IGNORECASE) or
            re.search(r"Unable to process the request.", result, re.IGNORECASE)
        )

    # ==========================================================================
    # NEGATIVE_TESTS
    # ==========================================================================
    @pytest.mark.parametrize("q", NEGATIVE_TESTS, ids=str)
    def test_negative(self, q):
        result = generate_answer(q, [])
        print(f"\nFRAGE: {q}\nANTWORT: {result}\n")
        assert (
            re.search(r"Information nicht gefunden.", result, re.IGNORECASE) or
            re.search(r"Unable to process the request.", result, re.IGNORECASE)
        )