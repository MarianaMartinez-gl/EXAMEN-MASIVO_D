#!/usr/bin/env python3
import sys
import csv
from decimal import Decimal

for linea in sys.stdin:
    try:
        fila = next(csv.reader([linea]))

        # Ignorar encabezado
        if fila[0] == "id":
            continue

        producto = fila[4]
        cantidad = Decimal(fila[5])
        precio = Decimal(fila[6])

        ingreso = cantidad * precio

        print(f"{producto}\t{ingreso}")

    except (ValueError, IndexError):
        continue
