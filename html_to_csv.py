import argparse
import csv
import sys
import dataclasses

from bs4 import BeautifulSoup



@dataclasses.dataclass
class Entry:
    date: str
    description: str
    paid_by: str
    charge: str
    payment: str


def parse(html_file):
    soup = BeautifulSoup(html_file, "html.parser")

    ledger_table = soup.find("table", class_="tenant-ledger-table")

    for row in ledger_table.tbody.find_all("tr"):
        date = row.find(class_="js-date").string.strip()
        description = row.find(class_="js-description").string.strip()
        paid_by = row.find(class_="js-paid-by").string.strip()
        charge = row.find(class_="js-charge").string.strip()
        payment = row.find(class_="js-payment").string.strip()
        yield Entry(date=date, description=description, paid_by=paid_by, charge=charge, payment=payment)


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "input_html",
        type=argparse.FileType(),
    )
    args = argument_parser.parse_args()
    input_html = args.input_html.read()

    csv_writer = csv.DictWriter(sys.stdout, fieldnames=[field.name for field in dataclasses.fields(Entry)])

    csv_writer.writeheader()
    for entry in parse(input_html):
        csv_writer.writerow(dataclasses.asdict(entry))
