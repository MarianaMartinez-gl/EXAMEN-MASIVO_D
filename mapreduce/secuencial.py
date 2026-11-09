import csv
import time
from decimal import Decimal
from collections import defaultdict

archivo = "/workspace/ventas_125052766.csv"

inicio = time.perf_counter()

totales = defaultdict(Decimal)

with open(archivo, "r", encoding="utf-8") as f:
    lector = csv.DictReader(f)

    for fila in lector:
        producto = fila["producto"]
        cantidad = Decimal(fila["cantidad"])
        precio = Decimal(fila["precio_unitario"])

        totales[producto] += cantidad * precio

top_10 = sorted(
    totales.items(),
    key=lambda x: x[1],
    reverse=True
)[:10]

fin = time.perf_counter()

print("TOP 10 PRODUCTOS POR INGRESO TOTAL")

for producto, total in top_10:
    print(f"{producto}\t{total:.2f}")

print(f"\nTiempo secuencial: {fin - inicio:.2f} segundos")
