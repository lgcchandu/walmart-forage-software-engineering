"""Run with: python import_shipments.py PATH_TO_STARTER_REPO."""

import argparse
import csv
import sqlite3
from collections import Counter
from contextlib import closing
from pathlib import Path


def read_rows(data_dir, sheet):
    path = data_dir / f"shipping_data_{sheet}.csv"
    with path.open(encoding="utf-8-sig", newline="") as source:
        yield from csv.DictReader(source)


def shipment_rows(data_dir):
    for row in read_rows(data_dir, 0):
        yield (
            row["product"], int(row["product_quantity"]),
            row["origin_warehouse"], row["destination_store"],
        )

    routes = {
        row["shipment_identifier"]: (
            row["origin_warehouse"], row["destination_store"]
        )
        for row in read_rows(data_dir, 2)
    }
    counts = Counter(
        (row["shipment_identifier"], row["product"])
        for row in read_rows(data_dir, 1)
    )
    for (shipment_id, product), quantity in counts.items():
        origin, destination = routes[shipment_id]
        yield product, quantity, origin, destination


def import_shipments(repo):
    rows = list(shipment_rows(repo / "data"))
    database = (repo / "shipment_database.db").resolve().as_uri()
    with closing(sqlite3.connect(database + "?mode=rw", uri=True)) as db:
        db.execute("PRAGMA foreign_keys = ON")
        with db:
            db.execute("BEGIN IMMEDIATE")
            # The target schema has no source shipment identifier for deduplication.
            if db.execute("SELECT 1 FROM shipment LIMIT 1").fetchone():
                raise ValueError("Use a fresh copy of the starter shipment database.")

            db.executemany(
                "INSERT INTO product (name) VALUES (?) "
                "ON CONFLICT(name) DO NOTHING",
                ((name,) for name in sorted({row[0] for row in rows})),
            )
            db.executemany(
                "INSERT INTO shipment (product_id, quantity, origin, destination) "
                "VALUES ((SELECT id FROM product WHERE name = ?), ?, ?, ?)",
                rows,
            )
    return len(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path, help="Folder with data/ and the starter DB")
    args = parser.parse_args()
    print(f"Imported {import_shipments(args.repo)} shipment product rows.")
