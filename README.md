# Examen Segundo Parcial: Pipeline de Datos Contenerizado

## 1. Datos del proyecto

- **Matrícula:** 125052766
- **Pregunta asignada:** Top 10 productos por ingreso total en todo el año.
- **Año analizado:** 2025
- **Registros procesados:** 5,000,000

## 2. Objetivo

Desarrollar un pipeline de datos contenerizado utilizando Hadoop, MapReduce, PostgreSQL y FastAPI para procesar cinco millones de registros de ventas y obtener los diez productos que generaron mayores ingresos durante el año.

La fórmula utilizada es:

`ingreso = cantidad * precio_unitario`

## 3. Tecnologías utilizadas

- Docker y Docker Compose.
- Hadoop 3.3.6.
- Python 3.
- PostgreSQL 16.
- FastAPI.
- Git y GitHub.

## 4. Estructura del proyecto

```text
examen-p2/
├── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
├── generar_dataset.py
├── hadoop/
│   └── Dockerfile
├── mapreduce/
│   ├── mapper.py
│   ├── reducer.py
│   └── secuencial.py
├── api/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── scripts/
│   └── cargar_resultados.py
└── evidencias/
```

## 5. Generación del dataset

El dataset contiene cinco millones de registros. Se genera usando la matrícula como semilla para reproducir los mismos datos.

```bash
python3 generar_dataset.py 125052766
```

El archivo generado es `ventas_125052766.csv`.

## 6. Levantar los contenedores

```bash
docker compose up -d --build
docker compose ps
```

## 7. Verificar Hadoop y SSH

```bash
docker compose exec hadoop hadoop version
docker compose exec hadoop ssh localhost "echo SSH funcionando"
docker compose exec hadoop jps
```

## 8. Cargar datos en HDFS

```bash
docker compose exec hadoop hdfs dfs -mkdir -p /datos/ventas
docker compose exec hadoop hdfs dfs -put /workspace/ventas_125052766.csv /datos/ventas/
docker compose exec hadoop hdfs dfs -ls /datos/ventas
```

## 9. Procesamiento MapReduce

El Mapper calcula el ingreso de cada venta. El Reducer suma los ingresos por producto y obtiene los diez productos con mayor ingreso total.

El trabajo se ejecuta con Hadoop Streaming y un solo Reducer para obtener el Top 10 global.

## 10. Procesamiento secuencial

También se realizó el procesamiento con Python para comparar los resultados y los tiempos.

```bash
docker compose exec hadoop python3 /workspace/mapreduce/secuencial.py
```

## 11. Resultados

| Posición | Producto | Ingreso total |
|---:|---|---:|
| 1 | PAP-0014 | 138180935.44 |
| 2 | PAP-0005 | 137986736.93 |
| 3 | PAP-0024 | 137897198.43 |
| 4 | PAP-0004 | 137349293.11 |
| 5 | PAP-0001 | 137249077.79 |
| 6 | PAP-0007 | 136845454.27 |
| 7 | PAP-0015 | 136740247.03 |
| 8 | PAP-0012 | 136623893.23 |
| 9 | PAP-0009 | 136540624.20 |
| 10 | PAP-0026 | 136223410.24 |

## 12. Comparación de tiempos

| Método | Tiempo |
|---|---:|
| Secuencial | 14.06 segundos |
| Hadoop MapReduce | 34.640 segundos |

MapReduce tardó más en esta ejecución porque se trabajó en un entorno de un solo nodo y Hadoop necesita tiempo adicional para coordinar sus procesos. Ambos métodos obtuvieron los mismos resultados.

## 13. API y PostgreSQL

La API permite guardar y consultar los resultados mediante FastAPI y PostgreSQL.

Para cargar los diez resultados desde HDFS:

```bash
docker compose exec hadoop python3 /workspace/scripts/cargar_resultados.py
```

Para comprobar el estado de la API:

```bash
docker compose exec hadoop curl http://api:8000/health
```

Para consultar los resultados:

```bash
docker compose exec hadoop curl http://api:8000/resultados
```

Endpoints:

- `GET /health`: verifica el funcionamiento.
- `GET /resultados`: consulta los resultados.
- `POST /resultados`: guarda o actualiza un producto.

## 14. Prueba de eliminación del volumen

Se eliminó el volumen de PostgreSQL, se creó nuevamente la base de datos y se cargaron otra vez los resultados desde HDFS.

```bash
docker compose stop api db
docker compose rm -f api db
docker volume rm examen-p2_datos_postgres
docker compose up -d db api
docker compose exec hadoop python3 /workspace/scripts/cargar_resultados.py
```

La prueba permitió comprobar que los resultados podían recuperarse desde HDFS después de eliminar la base de datos.

## 15. Explicación de Docker Compose

El servicio `db` utiliza PostgreSQL 16. La configuración de variables de entorno permite definir el nombre de la base de datos, usuario y contraseña.

El volumen `datos_postgres` conserva la información aunque el contenedor se detenga. La red `examen-red` permite la comunicación entre los servicios. El `healthcheck` verifica que PostgreSQL esté listo antes de que la API intente conectarse.

## 16. Evidencias

Se agregarán capturas de:

1. Versión de Hadoop.
2. Conexión SSH sin contraseña.
3. Procesos de Hadoop.
4. Ejecución MapReduce.
5. Resultado del Top 10.
6. Tiempo secuencial.
7. Respuesta de la API.
8. Eliminación y recreación del volumen.
9. Recarga de los resultados.

## 17. Conclusión

Se desarrolló un pipeline de datos contenerizado capaz de procesar cinco millones de ventas y obtener los diez productos con mayor ingreso total. Los resultados de MapReduce coincidieron con los del procesamiento secuencial. También se comprobó la integración entre Hadoop, PostgreSQL y FastAPI, así como la recuperación de los resultados después de recrear el volumen de la base de datos.

