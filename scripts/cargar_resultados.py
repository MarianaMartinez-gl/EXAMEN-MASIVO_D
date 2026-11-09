import subprocess
import json
import urllib.request

# Leer los resultados guardados en HDFS
comando = [
    "hdfs", "dfs", "-cat",
    "/resultados/ventas/part-00000"
]

salida = subprocess.check_output(comando, text=True)

# Enviar cada producto a la API
url = "http://api:8000/resultados"

for linea in salida.strip().split("\n"):
    producto, ingreso = linea.split("\t")

    datos = {
        "producto": producto,
        "ingreso_total": float(ingreso)
    }

    contenido = json.dumps(datos).encode("utf-8")

    solicitud = urllib.request.Request(
        url,
        data=contenido,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    respuesta = urllib.request.urlopen(solicitud)

    print(producto, "-", respuesta.status)

print("Carga de resultados terminada.")
