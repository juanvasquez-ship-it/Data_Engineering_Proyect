# Data_Engineering_Proyect

## Proyecto Integrador - Avance

Este repositorio contiene el avance del Proyecto Integrador del curso de Ingeniería de Datos.
El objetivo de esta primera etapa es construir un pipeline de ingesta utilizando Apache Airflow, Docker y Azure Data Lake, moviendo datos desde una fuente local simulada hacia una zona Raw en la nube.

## Contexto del negocio

El dominio inicial seleccionado es Ventas / Comercial de una empresa retail tecnológica.

Actualmente, la información transaccional de ventas se genera como archivos locales, lo que dificulta su disponibilidad oportuna para análisis de negocio. Esta situación limita la visibilidad sobre ingresos, márgenes, canales de venta, sedes, segmentos de clientes y campañas comerciales.

Automatizar la carga hacia Azure permite iniciar una zona Raw confiable, trazable y reutilizable para futuros procesos de transformación y construcción de data products.

## Problema a resolver

La empresa necesita centralizar sus datos comerciales para que puedan ser utilizados posteriormente en análisis de ventas, rentabilidad, comportamiento de clientes y desempeño comercial.

En esta primera entrega no se realizan transformaciones sobre la data. El alcance se limita a la ingesta del archivo fuente hacia la zona Raw.

## Arquitectura del avance

El flujo implementado es:

```text
Carpeta local simulada
        ↓
Apache Airflow
        ↓
DAG de ingesta
        ↓
Azure Data Lake - Raw Zone
```

Componentes principales:

* Fuente local: archivo CSV ubicado en la carpeta `data/`.
* Orquestador: Apache Airflow ejecutado con Docker.
* Script auxiliar: función de carga hacia Azure mediante `WasbHook`.
* Destino: contenedor `datalake`, ruta Raw del Grupo 5.

## Dataset utilizado

Archivo fuente:

```text
data/ventas_transacciones_g5.csv
```

Este archivo representa transacciones comerciales del dominio Ventas. Incluye campos como:

* venta_id
* fecha_venta
* cliente_id
* producto_id
* campania_id
* canal_venta
* tipo_cliente
* segmento_cliente
* cantidad
* precio_unitario
* monto_total
* margen_estimado
* estado_entrega
* estado_venta

La data es sintética y fue creada para simular una fuente local de negocio que pueda ser utilizada como base para un futuro data product comercial.

## DAG implementado

Archivo del DAG:

```text
dags/g5_ingesta_raw_azure.py
```

Nombre del DAG en Airflow:

```text
g5_ingesta_raw_azure
```

Función principal:

* Leer el archivo local desde `/opt/airflow/data/ventas_transacciones_g5.csv`.
* Generar un nombre de archivo con sufijo de fecha.
* Cargar el archivo hacia Azure Data Lake.
* Almacenar el archivo en la zona Raw del Grupo 5.

Ruta destino esperada:

```text
datalake/raw/airflow/G5/ventas/
```

## Conexión a Azure

La conexión hacia Azure se configura directamente en la interfaz de Airflow:

```text
Admin → Connections
```

Connection ID utilizado:

```text
azure_blob_storage
```

Tipo de conexión:

```text
wasb
```

La connection string se configura en Airflow como variable segura y no debe ser incluida en el código fuente ni en GitHub.

## Estructura del repositorio

```text
Data_Engineering_Project/
│
├── config/
│   └── airflow.cfg
│
├── dags/
│   └── g5_ingesta_raw_azure.py
│
├── data/
│   └── ventas_transacciones_g5.csv
│
├── plugins/
│   └── .gitkeep
│
├── scripts/
│   ├── azure_upload.py
│   └── helpers.py
│
├── .gitignore
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
└── README.md
```

## Ejecución local con Docker

Inicializar Airflow:

```bash
docker compose up airflow-init
```

Levantar los servicios:

```bash
docker compose up -d
```

Validar contenedores activos:

```bash
docker ps
```

Ingresar a Airflow:

```text
http://localhost:8080
```

Credenciales utilizadas en el entorno local:

```text
Usuario: airflow
Contraseña: airflow
```

## Validación del pipeline

Para validar la ejecución:

1. Ingresar a Airflow.
2. Activar el DAG `g5_ingesta_raw_azure`.
3. Ejecutar el DAG manualmente.
4. Confirmar que la ejecución finalice correctamente.
5. Verificar que el archivo se haya cargado en Azure Data Lake dentro de la ruta Raw del Grupo 5.

## Uso de Git y GitFlow

Se utilizó una estrategia GitFlow básica:

* `main`: rama estable.
* `develop`: rama de integración del avance.
* `feature/ingesta-raw-azure`: rama de desarrollo del pipeline.

Flujo seguido:

1. Creación de rama feature desde `develop`.
2. Implementación de estructura Airflow/Docker.
3. Desarrollo del DAG del Grupo 5.
4. Ajuste de dependencias y configuración.
5. Validación del pipeline en Airflow.
6. Integración de la rama feature hacia `develop` mediante Pull Request.

## Relación con Data Mesh

Este avance representa la primera ingesta del dominio Ventas / Comercial.

A futuro, esta base Raw podrá evolucionar hacia un enfoque Data Mesh mediante la incorporación de nuevos dominios como:

* Clientes / CRM
* Productos / Inventario
* Marketing
* Postventa

El objetivo futuro será construir un data product comercial que permita analizar ingresos, márgenes, canales, sedes, campañas y comportamiento de clientes.

## Próximos pasos

* Incorporar reglas de calidad y validación en una capa Silver.
* Normalizar dimensiones como clientes, productos, campañas y sedes.
* Construir tablas agregadas en Gold para consumo analítico.
* Desarrollar dashboards en Power BI.
* Documentar el data product bajo el principio Data as a Product.
