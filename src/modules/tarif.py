import datetime
import json
import pathlib


MAIN_DIR = pathlib.Path(__file__).parent.parent.parent
OUTPUT_DIR = MAIN_DIR / "output"


class Tarif:
    def __init__(self, name: str, price: float, fee: float, volume: int, speed: int, url: str, site: str, unlimited_data: bool, details: dict = None):
        self.name: str = name
        self.price: float = price
        self.fee: float = fee
        self.volume: int | str = volume
        self.speed: int = speed
        self.url: str = url
        self.site: str = site
        self.unlimited_data: bool = unlimited_data
        self.details: dict = details

        if unlimited_data:
            self.volume = 1000000

    def to_json(self):
        return {
            "name": self.name,
            "price": self.price,
            "fee": self.fee,
            "volume": self.volume,
            "speed": self.speed,
            "url": self.url,
            "site": self.site,
            "unlimited_data": self.unlimited_data,
            "details": self.details,
        }

    def __repr__(self):
        return f"€{self.price: <5} | {self.volume if not self.unlimited_data else "∞": <4}GB | {self.speed: <4} mbit/s | {self.url: <50} | {self.details}"


class TarifManager:
    def __init__(self):
        self.tarifs = []

    def add_tarif(self, tarif: Tarif):
        if not tarif:
            return
        self.tarifs.append(tarif)

    def to_json(self):
        tarifs_json = []
        for tarif in self.tarifs:
            tarifs_json.append(tarif.to_json())
        return tarifs_json

    def save(self):
        output_file = OUTPUT_DIR / f"tarifs-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        if not output_file.parent.exists():
            output_file.parent.mkdir(parents=True, exist_ok=True)

        # Generate the json data
        tarifs_data = json.dumps(self.to_json(), indent=2)

        with open(output_file, "w") as file:
            file.write(tarifs_data)

    def load(self):
        # Get the data from the newest tarif file
        tarif_files = list(OUTPUT_DIR.glob("tarifs-*.json"))
        if not tarif_files:
            return
        tarif_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        tarif_file = tarif_files[0]

        # The the data from that file
        with open(tarif_file, "r") as file:
            tarifs_data = json.load(file)

        # Load the tarifs
        for tarif_data in tarifs_data:
            tarif = Tarif(
                name=tarif_data["name"],
                price=tarif_data["price"],
                fee=tarif_data["fee"],
                volume=tarif_data["volume"],
                speed=tarif_data["speed"],
                url=tarif_data["url"],
                site=tarif_data["site"],
                unlimited_data=tarif_data["unlimited_data"],
                details=tarif_data["details"],
            )
            self.add_tarif(tarif)

    def print_pretty(self, only_no_fee=False):
        print(f"\n\n####### {len(self.tarifs)} Drillisch Verträge gefunden #######")

        # Sort by price
        tarifs = self.tarifs.copy()
        tarifs.sort(key=lambda x: (x.price, x.volume, x.speed))

        for tarif in tarifs:
            if only_no_fee and tarif.fee > 0:
                continue
            print(tarif)

    def __repr__(self):
        return json.dumps(self.to_json(), indent=2)
