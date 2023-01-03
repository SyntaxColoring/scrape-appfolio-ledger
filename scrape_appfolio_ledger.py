#!/usr/bin/env python3


import argparse
import csv
import sys
import dataclasses

from bs4 import BeautifulSoup


@dataclasses.dataclass
class Row:
    date: str
    description: str
    paid_by: str
    charge: str
    payment: str


def scrape_rows(html_file):
    soup = BeautifulSoup(html_file, "html.parser")

    ledger_table = soup.find("table", class_="tenant-ledger-table")
    if ledger_table is None:
        raise RuntimeError(
            "Couldn't find the ledger table."
            " Is this a correctly saved HTML file?"
            " Has the page's HTML been updated?"
        )

    def extract_cell_string(row, cell_class):
        cell = row.find(class_=cell_class)
        if cell is None:
            raise RuntimeError(
                f"Couldn't find a cell with class {repr(cell_class)}."
                f" Is this a correctly saved HTML file?"
                f" Has the page's HTML been updated?"
                f"\n\nLooked in row:\n\n"
                f"{row}"
            )
        cell_string = cell.string
        if cell_string is None:
            raise runtimeError(
                f"Unexpectedly found multiple strings inside cell."
                f" Is this a correctly saved HTML file?"
                f" Has the page's HTML been updated?"
                f"\n\nCell:\n\n"
                f"{cell}"
            )
        return cell_string.strip()

    rows = ledger_table.tbody.find_all("tr")
    for row in rows:
        date = extract_cell_string(row, cell_class="js-date")
        description = extract_cell_string(row, cell_class="js-description")
        paid_by = extract_cell_string(row, cell_class="js-paid-by")
        charge = extract_cell_string(row, cell_class="js-charge")
        payment = extract_cell_string(row, cell_class="js-payment")
        yield Row(
            date=date,
            description=description,
            paid_by=paid_by,
            charge=charge,
            payment=payment,
        )


def main(input_file, output_file):
    csv_writer = csv.DictWriter(
        output_file, fieldnames=[field.name for field in dataclasses.fields(Row)]
    )

    csv_writer.writeheader()
    for row in scrape_rows(input_file):
        csv_writer.writerow(dataclasses.asdict(row))


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "input_html_file",
        metavar="input_html_path",
        type=argparse.FileType(mode="r"),
        help=(
            "The path to an HTML file of the AppFolio ledger page."
            " Use a hyphen (-) for standard input."
        ),
    )
    argument_parser.add_argument(
        "output_csv_file",
        metavar="output_csv_path",
        type=argparse.FileType(mode="w"),
        help=(
            "Where to save the output CSV file."
            " Use a hyphen (-) for standard output."
        ),
    )

    args = argument_parser.parse_args()
    main(args.input_html_file, args.output_csv_file)
