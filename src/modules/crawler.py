import ast
import requests
from bs4 import BeautifulSoup
from pprint import pprint

from src.modules.tarif import Tarif, TarifManager

tarif_manager = TarifManager()


def crawl_sites(urls, clean=False):
    if clean:
        for url in urls:
            crawl_url(url)
        tarif_manager.save()
    else:
        tarif_manager.load()

    tarif_manager.print_pretty(only_no_fee=True)


def crawl_url(url):
    print(f"Visiting {url} ...")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup.prettify())

    # Find all tarif elements
    tarif_urls = set()
    tarif_elements = soup.select("a[data-tooltip-tarif-id]")
    for tarif_element in tarif_elements:
        tarif_id = tarif_element["data-tooltip-tarif-id"]
        tarif_url = f"{url}/details/{tarif_id}"
        print(f"Found tarif: {tarif_url}")
        tarif_urls.add(tarif_url)

    # Crawl all tarif details
    for tarif_url in tarif_urls:
        tarif = crawl_details_url(tarif_url)
        tarif_manager.add_tarif(tarif)


def crawl_details_url(url) -> Tarif | None:
    print(f"\nVisiting {url} ...")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup.prettify())

    # Find script page data
    product_data = {}
    detail_elements = soup.select("script[nonce]")
    for detail_element in detail_elements:
        script_str = detail_element.text.strip()
        if not script_str.startswith("var digitalData = "):
            continue
        script_str = script_str.strip("var digitalData = ").strip(";")
        product_data = ast.literal_eval(script_str)
    # pprint(product_data)

    # Extract tarif data
    category = product_data["product.category"]
    print(f"Category: {category}")
    if not category or category[0] in ["DSL", "Bundle Kauf"]:
        return None

    name = product_data["product.productName"][0]
    price = float(product_data["product.price.monthlyPayment"][0])
    fee = float(product_data["product.price.oneTimePayment"][0])
    volume = int(product_data["product.dataVolume"][0].lower().strip(" gb"))
    speed = int(product_data["product.dataSpeed"][0].lower().strip(" mbit/s"))
    url = url
    site = product_data["page.domain"].strip(".")
    unlimited_data = product_data["product.eppixPackageName"][0].split("|")[3] == "LU"

    tarif = Tarif(name, price, fee, volume, speed, url, site, unlimited_data, product_data)
    return tarif


