# Globale Variable (außerhalb aller Klassen/Funktionen)
# Wird im ganzen Programm benutzt — z. B. für Mehrwertsteuer
VAT_RATE = 0.19


# 🔧 Funktion (arbeitet mit der Klasse unten zusammen)
def format_invoice(order: "Order") -> str:
    """Erstellt eine Text-Rechnung aus einem Order-Objekt."""
    lines = [f"Kunde: {order.customer}", f"Positionen ({len(order)}):"]

    # Durch alle Positionen iterieren (Name, Preis, Menge)
    for name, price, qty in order:
        lines.append(f"  - {name} x{qty}: {price:.2f} €")

    # Zusätzliche Rechnungsinfos
    lines.append(f"Rabatt: {order.discount*100:.0f}%")
    lines.append(f"Zwischensumme: {order.total(with_tax=False):.2f} €")
    lines.append(f"MwSt ({int(VAT_RATE*100)}%): {(order.total(with_tax=True) - order.total(with_tax=False)):.2f} €")
    lines.append(f"Gesamt: {order.total(with_tax=True):.2f} €")
    lines.append(f"Erstellt am: {order.created_at.isoformat(timespec='seconds')}")

    return "\n".join(lines)  # Rückgabe als String


# --------------------------------------------------------------
# 🧱 Klasse (mit Konstruktor, Methoden, Vererbung usw.)
# --------------------------------------------------------------
from datetime import datetime

class Order(list):  # Die Klasse erbt von der eingebauten list-Klasse (Vererbung)
    """Bestellung mit öffentlichen, geschützten und privaten Methoden."""

    # 🔹 Klassenattribut (für ALLE Instanzen gleich)
    default_fee = 0.99

    # 🔹 Konstruktor (wird beim Erzeugen eines Objekts ausgeführt)
    def __init__(self, customer: str, discount: float = 0.0):
        super().__init__()                   # ruft den Konstruktor der Basisklasse (list) auf
        self.customer = customer             # öffentliches Attribut (von außen zugänglich)
        self._currency = "EUR"               # geschütztes Attribut (Konvention: intern)
        self.__created_at = datetime.now()   # privates Attribut (nicht direkt von außen)
        self._discount = 0.0
        self.discount = discount             # ruft Setter auf → prüft Gültigkeit

    # 🔹 Property (Getter) — gibt den Rabatt zurück
    @property
    def discount(self) -> float:
        return self._discount

    # 🔹 Property (Setter) — überprüft Eingaben, bevor sie gespeichert werden
    @discount.setter
    def discount(self, value: float) -> None:
        if not (0.0 <= value <= 0.9):
            raise ValueError("discount muss zwischen 0.0 und 0.9 liegen")
        self._discount = value

    # 🔹 Read-only Property (nur Getter) — kein Setter, daher unveränderbar
    @property
    def created_at(self) -> datetime:
        return self.__created_at

    # 🔹 Öffentliche Methode — kann von außen aufgerufen werden
    def add_item(self, name: str, price: float, qty: int = 1) -> None:
        # nutzt geschützte Hilfsmethode zur Namensbereinigung
        name = self._normalize_name(name)

        # nutzt statische Methode zur Preisprüfung
        if not self.is_valid_price(price):
            raise ValueError("Preis muss >= 0 sein")

        if qty < 1:
            raise ValueError("Menge muss >= 1 sein")

        # fügt das Element über die Basisklasse (list) hinzu
        super().append((name, float(price), int(qty)))

    # 🔹 Öffentliche Methode — berechnet Gesamtsumme der Bestellung
    def total(self, with_tax: bool = True) -> float:
        # Summe aller Positionen (Preis * Menge)
        subtotal = sum(price * qty for _, price, qty in self)
        # Rabatt abziehen
        subtotal *= (1 - self.discount)
        # interne (private) Zusatzgebühr addieren
        subtotal += self.__secret_fee()

        # Mehrwertsteuer hinzufügen, wenn gewünscht
        if with_tax:
            subtotal *= (1 + VAT_RATE)

        return round(subtotal, 2)

    # 🔹 Geschützte Methode (intern, darf aber von Unterklassen benutzt werden)
    def _normalize_name(self, name: str) -> str:
        # Entfernt doppelte Leerzeichen und macht Großbuchstaben am Anfang
        return " ".join(name.strip().split()).title()

    # 🔹 Private Methode (durch Name-Mangling geschützt)
    def __secret_fee(self) -> float:
        # Zugriff nur innerhalb der Klasse (Name-Mangling: _Order__secret_fee)
        return self.default_fee

    # 🔹 Klassenmethode — kann neue Instanzen erzeugen
    @classmethod
    def from_dicts(cls, customer: str, items: list[dict], discount: float = 0.0) -> "Order":
        # cls = Verweis auf die Klasse selbst
        order = cls(customer, discount=discount)
        for it in items:
            order.add_item(it["name"], it["price"], it.get("qty", 1))
        return order

    # 🔹 Statische Methode — gehört logisch zur Klasse, nutzt aber kein self/cls
    @staticmethod
    def is_valid_price(price: float) -> bool:
        return price >= 0

    # 🔹 Magic/Dunder-Methode — wie das Objekt angezeigt wird (für Entwickler)
    def __repr__(self) -> str:
        return f"Order(customer={self.customer!r}, items={list(self)!r}, discount={self.discount!r})"

    # 🔹 Magic/Dunder-Methode — wie das Objekt als String angezeigt wird (für Nutzer)
    def __str__(self) -> str:
        return f"Order für {self.customer} ({len(self)} Positionen, Gesamt {self.total():.2f} {self._currency})"


# --------------------------------------------------------------
# 🔄 Anwendung: Funktion + Klasse arbeiten zusammen
# --------------------------------------------------------------

# 1️⃣ Direkte Nutzung
order = Order("Ali", discount=0.10)  # Objekt erzeugen (ruft __init__ auf)
order.add_item("   usb   kabel  ", 7.5, qty=2)
order.add_item("Maus", 15.0)

# Funktion benutzt die Daten aus der Klasse → Rechnung ausgeben
print(format_invoice(order))


# 2️⃣ Nutzung über Klassenmethode (alternative Erzeugung)
order2 = Order.from_dicts(
    "Sara",
    items=[{"name": "Headset", "price": 29.9}, {"name": "Webcam", "price": 39.0, "qty": 2}],
    discount=0.05,
)

# Ausgabe der formatierten Rechnung
print()
print(format_invoice(order2))
