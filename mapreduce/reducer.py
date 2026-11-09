#!/usr/bin/env python3
import sys
from decimal import Decimal

totales = {}

for linea in sys.stdin:
    linea = linea.strip()

    if not linea:
        continue

    producto, ingreso = linea.split("\t", 1)
    ingreso = Decimal(ingreso)

    if producto in totales:
        totales[producto] += ingreso
    else:
        totales[producto] = ingreso

# Ordenar de mayor a menor y conservar los primeros 10
top_10 = sorted(
    totales.items(),
    key=lambda x: x[1],
    reverse=True
)[:10]

for producto, total in top_10:
    print(f"{producto}\t{total:.2f}")
