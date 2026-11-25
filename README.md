# Walmart Global Tech Advanced Software Engineering Job Simulation

Portfolio work from the Walmart Global Tech job simulation on Forage, completed November 25, 2026.

| Exercise | Portfolio work |
| --- | --- |
| Advanced data structures | [Java max heap](java/PowerOfTwoMaxHeap.java) with a configurable power-of-two branching factor |
| Software architecture | [UML class diagram](design/Walmart_Task2_Class_Diagram.pdf) for switching processor modes and database adapters at runtime |
| Relational database design | [Pet department ERD](design/Walmart_Task3_Pet_Department_ERD.pdf) covering products, animals, purchases, and shipments |
| Data munging | [Python import script](python/import_shipments.py) for transforming three CSVs and loading the results into SQLite |

## Run locally

Compile the Java heap with a JDK installed.

```sh
javac -d build java/PowerOfTwoMaxHeap.java
```

Run the Python script against a fresh local copy of the [Task 4 starter repository](https://github.com/theforage/forage-walmart-task-4). The script writes to the SQLite database in the folder you pass in.

```sh
python python/import_shipments.py /path/to/forage-walmart-task-4
```

## Verification

The Java heap was checked against a max-oriented Java `PriorityQueue` using nine exponents, including zero and the largest Java integer. The Python import produced 154 shipment product rows and 45 distinct products on the starter data. The imported rows were compared with the source CSVs, and SQLite integrity and foreign-key checks passed.
